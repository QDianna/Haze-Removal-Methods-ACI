import cv2
import numpy as np

def load_image(path):
    # citesc imaginea si o dau in rgb uint8 (H, W, 3)
    # imread da None daca nu gaseste fisierul, nu da eroare singur
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Cant read image: {path}")

    # opencv citeste in bgr, eu lucrez peste tot in rgb
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def save_image(path, image):
    # salvez imagine rgb uint8, formatul e ales dupa extensie (png, jpg)
    # imwrite vrea bgr asa ca intorc canalele inapoi
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # imwrite da False daca nu poate salva (de ex folderul nu exista), nu da eroare singur
    if not cv2.imwrite(path, img_bgr):
        raise IOError(f"Cant save image: {path}")

def to_float(image):
    # uint8 0-255 -> float 0-1, ca sa pot face calcule fara overflow
    return image.astype(np.float32) / 255.0

def to_uint8(image):
    # float 0-1 -> uint8 0-255
    # clip ca valorile sub 0 sau peste 1 sa nu se dea peste cap la conversie
    # round inainte de astype ca altfel taie zecimalele
    image = np.clip(image, 0.0, 1.0)
    return np.round(image * 255.0).astype(np.uint8)