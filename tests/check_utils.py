import os
from methods.utils import load_image, save_image, to_float, to_uint8

# testez functiile din utils: citire, conversii float/uint8 si salvare

os.makedirs("test_outputs", exist_ok=True)

# astept (H, W, 3) uint8 cu valori 0-255
img = load_image("test_img01.jpg")
print("original (uint8):", img.shape, img.dtype, img.min(), img.max())

# astept float32 cu valori 0-1, aceeasi forma
img_float = to_float(img)
print("to float:        ", img_float.shape, img_float.dtype, img_float.min(), img_float.max())

# inapoi la uint8 0-255
img_uint8 = to_uint8(img_float)
print("back to uint8:   ", img_uint8.shape, img_uint8.dtype, img_uint8.min(), img_uint8.max())

save_image("test_outputs/utils_out.png", img_uint8)
print("salvat in test_outputs/utils_out.png")