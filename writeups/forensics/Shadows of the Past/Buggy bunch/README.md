# Shadows of the past
GtHoo @ Buggy bunch
## Writeup

Challenge gives you a `.7z` file, so I just use `7z e economicsreport.7z`. That gives us a .pdf file.

From the challange description we are looking for an auther that will be hidden.
As i dont know so much about how pds i just try my luck with `binwalk -e Economics\ Report.pdf` and just grep in the directory with `grep -r EPT`which gives:

```
_Economics Report.pdf.extracted/11A5F:1 0 2 73 3 180 5 301 6 387 9 468 <</Type /Pages /Kids [3 0 R ] /Count 1 /MediaBox [0 0 595.28 841.89 ] >> <</ProcSet [/PDF /Text /ImageB /ImageC /ImageI ] /Font <</F1 5 0 R /F2 6 0 R >> /XObject <</I1 7 0 R >> >> <</Type /Page /Parent 1 0 R /Resources 2 0 R /Group <</Type /Group /S /Transparency /CS /DeviceRGB >> /Contents 4 0 R >> <</Type /Font /BaseFont /Helvetica-Bold /Subtype /Type1 /Encoding /WinAnsiEncoding >> <</Type /Font /BaseFont /Helvetica /Subtype /Type1 /Encoding /WinAnsiEncoding >> <</Producer (PyFPDF 1.7.2 http://pyfpdf.googlecode.com/) /Title (Economic Trends Report - Q3 2024) /Subject (Economics Report) /Author (EPT{1_am_h1dd3n_n0w_r1ght??}) /Keywords (Economics, GDP, Inflation, Q3 2024) /CreationDate (D:20240918112003) /Creator (PDF24) >> 

```

So the flag is `EPT{1_am_h1dd3n_n0w_r1ght??}`

