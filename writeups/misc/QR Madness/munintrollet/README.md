**Author: Zukane**

*A wall of QR codes stands in your way. What lies behind?

##### Challenge overview

In this misc challenge, we are given a large png image consisting of numerous QR codes. By scanning a random one, we get a link like `https://127.0.0.1/e`. This probably means all the QR codes will spell out a single character each, with the flag being spelt out by some of them.

The given png image in question consists of 10x50 QR codes. This is too much to scan by hand, so we do it programmatically.

##### Solution

My general idea was to use the python library ``Pillow`` to split the image into individual QR codes. Since we know the number of QR codes per row, we can use the width of the image to determine the size of the QR codes. After splitting up all the images, we can run the command-line tool ``Zbarimg`` to get the content (by running subprocesses in python). Since we are only interested in the final character of the output, we can save it to a string variable and print it at the end.

```python
import os
import subprocess
from PIL import Image

def split_image(image_path, output_dir, qr_per_row=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(image_path)
    width, height = img.size

    qr_width = int(width / qr_per_row)
    qr_height = qr_width 

    qr_per_column = height // qr_height

    qr_images = []
    count = 0
    for row in range(qr_per_column):
        for col in range(qr_per_row):
            x = col * qr_width
            y = row * qr_height
            box = (x, y, x + qr_width, y + qr_height)
            qr = img.crop(box)

            qr_filename = os.path.join(output_dir, f"qr_{count}.png")
            qr.save(qr_filename)
            qr_images.append(qr_filename)
            count += 1

    print(f"Total QR codes extracted: {count}")
    return qr_images

def read_qr_with_zbarimg(qr_image_path):
    try:
        result = subprocess.run(
            ['zbarimg', '--quiet', qr_image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error reading {qr_image_path}: {result.stderr.strip()}")
            return None

        output = result.stdout.strip()
        if output:
            # zbarimg outputs in the format: "QR-Code:content"
            _, content = output.split(':', 1)
            return content
        else:
            return None
    except Exception as e:
        print(f"Exception while reading {qr_image_path}: {e}")
        return None

large_image_path = 'qr.png' 
split_output_dir = 'split_qr_codes'
qr_per_row = 10 

qr_images = split_image(large_image_path, split_output_dir, qr_per_row)

qr_contents = {}
last_chars = [] 

for qr_image in qr_images:
    content = read_qr_with_zbarimg(qr_image)
    if content:
        qr_contents[qr_image] = content
        print(f"{qr_image}: {content}")

        last_char = content.strip()[-1] 
        last_chars.append(last_char)
    else:
        print(f"{qr_image}: Unable to read QR code.")

final_string = ''.join(last_chars)
print(f"\nFinal String from Last Characters: {final_string}")
```

By running this script, we get the entire text:

```
Final String from Last Characters: AQRcodeisatypeoftwo-dimensionalmatrixbarcode,inventedin1994,byJapanesecompanyDensoWaveforlabellingautomobileparts.Itfeaturesblacksquaresonawhitebackgroundwithfiducialmarkers,readablebyimagingdeviceslikecameras,andprocessedusingReed–Solomonerrorcorrectionuntiltheimagecanbeappropriatelyinterpreted.TherequireddataarethenextractedfrompatternsthatarepresentinboththehorizontalandtheverticalcomponentsoftheQRimageWhereasabarcodeisamachine-readableopticalimagethatcontainsinformationspecifictothelabeleditem,theQRcodecontainsthedataforalocator,anidentifier,andweb-tracking.Tostoredataefficiently,QRcodesusefourstandardizedmodesofencoding:(I)numeric,(ii)alphanumeric,(iii)byteorbinary,and(iv)kanji.ComparedtostandardUPCbarcodes,theQRlabelingsystemwasappliedbeyondtheautomobileindustrybecauseoffasterreadingEPT{QR_qu3st_0wn3d_2024}oftheopticalimageandgreaterdata-storagecapacityinapplicationssuchasproducttracking,itemidentification,timetracking,documentmanagement,andgeneralmarketing.it
```

And the flag is hidden amongst the fluff:

`EPT{QR_qu3st_0wn3d_2024}`