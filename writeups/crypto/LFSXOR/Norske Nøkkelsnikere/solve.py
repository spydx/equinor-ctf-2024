import sys
import numpy
import matplotlib.pyplot as plt
from PIL import Image
from enc import get_rand
import time

def decrypt(in_img, key):
    in_img = plt.imread(in_img)[:, :, 0]
    height, width = in_img.shape
    
    imarr = numpy.zeros((height, width, 3), dtype='uint8')
    rand = get_rand(key)
    
    random_values = numpy.array([rand() for _ in range(height * width)], dtype='uint8').reshape(height, width)
    
    # xor but vectorized  efficiency and speed
    imarr[:, :, 0] = (in_img ^ random_values)  # just edit first channel
    imarr[:, :, 1] = imarr[:, :, 0]  # copy to other channels for RGB
    imarr[:, :, 2] = imarr[:, :, 0]
    return Image.fromarray(imarr.astype('uint8')).convert('RGB')

if len(sys.argv) != 2:
    print("Usage: python main.py <input_image>")
    sys.exit(1)

IN_IMG = sys.argv[1]

start_time = time.time()
for key in range(1, 255):
    decrypted_image = decrypt(IN_IMG, key)
    out_img = f"{key}.png"
    decrypted_image.save(out_img)
    print(f"Saved: {out_img}")
    
    if key % 5 == 0:
        elapsed_time = time.time() - start_time
        print(f"Time taken for {key} images: {elapsed_time:.2f} seconds")
        estimated_total_time = (elapsed_time / key) * 255
        print(f"Estimated total time for 255 images: {estimated_total_time:.2f} seconds")