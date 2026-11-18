import os
from methods.utils import load_image, save_image
from methods.he import histogram_equalization

# testez histogram equalization pe o imagine

os.makedirs("test_outputs", exist_ok=True)

img = load_image("test_img01.jpg")
out = histogram_equalization(img)

save_image("test_outputs/he_out.png", out)
print("salvat in test_outputs/he_out.png")