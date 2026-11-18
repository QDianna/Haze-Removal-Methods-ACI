import os
import cv2
import numpy as np
from methods.utils import load_image, save_image, to_float, to_uint8
from methods.dcp import dark_channel, atmospheric_light, transmission, recover
from methods.guided_filter import guided_filter

# verific daca guided filter-ul meu da acelasi rezultat ca cel din opencv
# si salvez t si imaginea finala inainte si dupa filtrare ca sa vad diferenta

os.makedirs("test_outputs", exist_ok=True)

# calculez transmisia bruta ca in dcp
img = to_float(load_image("test_img01.jpg"))
dark = dark_channel(img)
A = atmospheric_light(img, dark)
t = transmission(img, A)

# ghidul e imaginea in gri
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# varianta mea si varianta gata facuta din opencv contrib, cu aceiasi parametri
t_mine = guided_filter(gray, t, 60, 1e-3)
t_cv = cv2.ximgproc.guidedFilter(gray, t, 60, 1e-3)

# ma astept sa fie mica
print("diferenta maxima:", np.abs(t_mine - t_cv).max())

# t_raw are patratele de la fereastra 15x15
# t_guided e neted si are marginile obiectelor clare
cv2.imwrite("test_outputs/t_raw.png", to_uint8(t))
cv2.imwrite("test_outputs/t_guided.png", to_uint8(t_mine))

# scot ceata cu fiecare t ca sa compar rezultatele
# cu t brut ar trebui sa apara halouri in jurul obiectelor, cu t_mine nu
J_raw = recover(img, t, A)
J_guided = recover(img, t_mine, A)

save_image("test_outputs/dcp_raw_out.png", to_uint8(J_raw))
save_image("test_outputs/dcp_guided_out.png", to_uint8(J_guided))