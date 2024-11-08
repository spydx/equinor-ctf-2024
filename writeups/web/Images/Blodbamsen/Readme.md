# 👶 Images 👶
Author: iLoop

Flag: `EPT{This_was_one_way_to_solve_this}`
## Description
```
To assist @nordbo with his graphical workload, we've developed an amazing image converter that allows the upload of images to be converted.

However, I think we made a mistake by uploading a image file with a secret message in it. Can you locate it?
```


---
### Challenge Description

This beginner-level challenge show us the IDOR (Insecure Direct Object References) vulnerability and was pretty straightforward, requiring us to identify an image containing a secret message. We were provided a link to a webpage with an image upload feature, hinting at a potential mistake in an uploaded file that held a secret message.

### Solution Walkthrough

1. **Exploring the Upload Interface**:
   - Upon accessing the provided link, we found a simple interface that allowed users to upload an image file for conversion. We followed the instructions and uploaded an image, then pressed "Convert."
     
![Pasted image 20241105205701](https://github.com/user-attachments/assets/4496ef7e-f665-4a9a-bc82-b8794da91362)


2. **Redirected Download Page**:
   - After initiating the conversion, we were redirected to a download page. While hovering over the download button, we observed a URL at the bottom left corner pointing to `/static/images/`, revealing where the converted images were stored.
     
![staticimages2](https://github.com/user-attachments/assets/ffe535fc-36d2-4e8a-a125-b1a5ab71f100)


3. **Inspecting the Image Directory**:
   - Navigating to `/static/images/`, we located a file named `flag.JPEG`, which seemed out of place.
     
![Pasted image 20241105211059](https://github.com/user-attachments/assets/f5d23b55-52b0-4d93-8803-1f6bef4a8c51)

4. **Retrieving the Flag**:
   - Opening `flag.JPEG`, we discovered the hidden flag embedded in the image, successfully solving the challenge.
     
![Screenshot at 2024-11-05 20-33-36](https://github.com/user-attachments/assets/b355ab8b-6c73-4124-9073-05a406eaa9cd)
