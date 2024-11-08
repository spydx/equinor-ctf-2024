# Writeup

author: .spydx @ bwnfools

## Shadows of the past :baby:

Got an `.7z` file that revealed a PDF.
Challenge hints that we are looking for remenants of its earlier author.

Viewed the file with the following tools to get an overview of the PDF file.

- `pdfid`
- `pdf-parser`

Lastly used the `exiftool` to view the file metadata, and it had a missing author as expected.

```shell
┌───(.spydx㉿kali)-[~/equinor-ctf-2024/shadows_of_the_past]
└─$ exiftool 'Economics Report.pdf' 
ExifTool Version Number         : 12.76
File Name                       : Economics Report.pdf
Directory                       : .
File Size                       : 77 kB
File Modification Date/Time     : 2024:09:18 13:26:45+02:00
File Access Date/Time           : 2024:11:02 12:45:42+01:00
File Inode Change Date/Time     : 2024:11:02 12:45:42+01:00
File Permissions                : -rw-rw-r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
Linearized                      : No
Page Count                      : 1
Page Layout                     : OneColumn
PDF Version                     : 1.6
XMP Toolkit                     : Image::ExifTool 12.40
Author                          :  # <-- missing author
Producer                        : PyFPDF 1.7.2 http://pyfpdf.googlecode.com/
Title                           : Economic Trends Report - Q3 2024
Subject                         : Economics Report
Keywords                        : Economics, GDP, Inflation, Q3 2024
Create Date                     : 2024:09:18 11:20:03
Creator                         : PDF24
```

Quick google search shows that one can recover metadata that exiftool has removed by updating the document.

```shell
┌───(.spydx㉿kali)-[~/equinor-ctf-2024/shadows_of_the_past]
└─$ exiftool 'Economics Report.pdf' -pdf-update:all=
    1 image files updated
```

Then exif again to view the data

```shell
┌───(.spydx㉿kali)-[~/equinor-ctf-2024/shadows_of_the_past]
└─$ exiftool 'Economics Report.pdf' 
ExifTool Version Number         : 12.76
File Name                       : report.pdf
Directory                       : .
File Size                       : 73 kB
File Modification Date/Time     : 2024:11:02 12:46:26+01:00
File Access Date/Time           : 2024:11:02 12:46:26+01:00
File Inode Change Date/Time     : 2024:11:02 12:46:26+01:00
File Permissions                : -rw-rw-r--
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
Linearized                      : No
Page Count                      : 1
Page Layout                     : OneColumn
PDF Version                     : 1.6
Producer                        : PyFPDF 1.7.2 http://pyfpdf.googlecode.com/
Title                           : Economic Trends Report - Q3 2024
Subject                         : Economics Report
Author                          : EPT{1_am_h1dd3n_n0w_r1ght??} # success
Keywords                        : Economics, GDP, Inflation, Q3 2024
Create Date                     : 2024:09:18 11:20:03
Creator                         : PDF24
```

Success, we found the flag in the `Author` field.

```shell
Author                          : EPT{1_am_h1dd3n_n0w_r1ght??}
```
