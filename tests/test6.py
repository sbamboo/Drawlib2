from PIL import Image

import os
_img = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test2.png")

image = Image.open(_img)

if image.mode != "RGB":
    image = image.convert("RGB")

for y in range(image.height):
    for x in range(image.width):
        pixel = image.getpixel((x,y))

        if image.mode == "RGB":
            # For RGB images, pixel is already in tuple format
            print(pixel)
        elif image.mode == "L":
            # For grayscale images, convert the single integer to an RGB tuple
            pixel = (pixel, pixel, pixel)
            print(pixel)
        else:
            # Handle other color modes as needed
            print(f"Unhandled color mode: {image.mode}")

        print(pixel)