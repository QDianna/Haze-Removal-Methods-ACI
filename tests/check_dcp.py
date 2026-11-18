import os
import cv2
from methods.utils import load_image, save_image, to_float, to_uint8
from methods.dcp import dark_channel, atmospheric_light, transmission, dcp

# testez dcp pe o imagine si salvez si pasii intermediari ca sa vad ce face

os.makedirs("test_outputs", exist_ok=True)

image = load_image("test_img01.jpg")

# pasii dcp
img = to_float(image)
dark = dark_channel(img)
A = atmospheric_light(img, dark)
t = transmission(img, A)

# A ar trebui sa fie in jur de 0.7-1 pe fiecare canal (ceata deschisa la culoare)
print("A =", A, " t min/max =", t.min(), t.max())

# dark si t sunt alb-negru (H, W) asa ca le salvez direct cu imwrite, fara conversie bgr
# dark: luminos unde e ceata multa
# t: invers, alb aproape, negru departe
cv2.imwrite("test_outputs/dcp_dark.png", to_uint8(dark))
cv2.imwrite("test_outputs/dcp_transmission.png", to_uint8(t))

# rezultatul final
save_image("test_outputs/dcp_out.png", dcp(image))
print("salvat in test_outputs/")