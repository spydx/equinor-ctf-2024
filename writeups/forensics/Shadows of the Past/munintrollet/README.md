**Author: Zukane**

*A document has been redacted to hide sensitive metadata, or so they thought. Hidden traces of past authors still lurk in the shadows of the file. Can you recover the ghostly remnants and reveal the true identity of the author?*

##### Challenge overview

In this forensics challenge, we are given a pdf file named `Economics Report.pdf`. 

By running the tool `pdfid` we can get an overview of what the PDF contains

```
└─$ pdfid Economics\ Report.pdf  
PDFiD 0.2.8 Economics Report.pdf
 PDF Header: %PDF-1.6
 obj                   10
 endobj                10
 stream                 7
 endstream              7
 xref                   0
 trailer                0
 startxref              2
 /Page                  0
 /Encrypt               0
 /ObjStm                1
 /JS                    0
 /JavaScript            0
 /AA                    0
 /OpenAction            2
 /AcroForm              0
 /JBIG2Decode           0
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          0
 /XFA                   0
 /Colors > 2^24         0
```

##### Solution

Interestingly, there is one instance of an object-stream: `/ObjStm`

By running the tool `pdf-parser`, we can get a more detailed overview of what the pdf contains. We are interested in finding out which object contains the object-stream:

```
└─$ pdf-parser Economics\ Report.pdf | grep -C 1 -i objstm 
obj 11 0
 Type: /ObjStm
 Referencing: 
```

We see it is object 11. We can dump the contents to a file using the following command:

```
pdf-parser Economics\ Report.pdf -o 11 -f -d out.bin
```

By examining the contents, we can find the flag in the author field:

```
└─$ cat out.bin 
1 0 2 73 3 180 5 301 6 387 9 468 <</Type /Pages /Kids [3 0 R ] /Count 1 /MediaBox [0 0 595.28 841.89 ] >> <</ProcSet [/PDF /Text /ImageB /ImageC /ImageI ] /Font <</F1 5 0 R /F2 6 0 R >> /XObject <</I1 7 0 R >> >> <</Type /Page /Parent 1 0 R /Resources 2 0 R /Group <</Type /Group /S /Transparency /CS /DeviceRGB >> /Contents 4 0 R >> <</Type /Font /BaseFont /Helvetica-Bold /Subtype /Type1 /Encoding /WinAnsiEncoding >> <</Type /Font /BaseFont /Helvetica /Subtype /Type1 /Encoding /WinAnsiEncoding >> <</Producer (PyFPDF 1.7.2 http://pyfpdf.googlecode.com/) /Title (Economic Trends Report - Q3 2024) /Subject (Economics Report) /Author (EPT{1_am_h1dd3n_n0w_r1ght??}) /Keywords (Economics, GDP, Inflation, Q3 2024) /CreationDate (D:20240918112003) /Creator (PDF24) >>    
```

flag: `EPT{1_am_h1dd3n_n0w_r1ght??}`