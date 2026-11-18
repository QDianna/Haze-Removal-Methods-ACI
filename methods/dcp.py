import cv2
import numpy as np
from methods.utils import to_float, to_uint8
from methods.guided_filter import guided_filter


def dark_channel(image, patch_size=15):
    # iau canalul minim (r, g sau b) pentru fiecare pixel
    # apoi minimul din fereastra 15x15 din jurul lui (erode face asta)
    # unde nu e ceata iese aproape negru, unde e ceata iese luminos
    min_rgb = np.min(image, axis=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (patch_size, patch_size))
    return cv2.erode(min_rgb, kernel)


def atmospheric_light(image, dark, top_percent=0.001):
    # caut culoarea cetii (A)
    # iau cei mai luminosi 0.1% pixeli din dark channel, acolo e cea mai multa ceata
    # din ei il aleg pe cel mai luminos din imaginea originala
    h, w = dark.shape
    num_pixels = max(int(h * w * top_percent), 1)

    # fac imaginile liste de pixeli ca sa pot lua aceiasi pixeli din ambele
    dark_flat = dark.reshape(-1)
    image_flat = image.reshape(-1, 3)

    # pozitiile celor mai mari valori din dark channel
    indices = np.argpartition(dark_flat, -num_pixels)[-num_pixels:]
    candidates = image_flat[indices]

    # candidatul cu r+g+b maxim
    brightest = np.argmax(candidates.sum(axis=1))
    # alternativa: media candidatilor, mai stabila la zgomot
    # return candidates.mean(axis=0)
    return candidates[brightest]


def transmission(image, A, omega=0.95, patch_size=15):
    # cat din lumina obiectului ajunge la camera, t = 1 - omega * dark(I / A)
    # impart la A ca ceata sa fie 1 pe fiecare canal
    # omega 0.95 lasa putina ceata ca sa arate natural
    normalized = image / A
    return 1.0 - omega * dark_channel(normalized, patch_size)


def recover(image, t, A, t0=0.1):
    # scot ceata din formula J = (I - A) / t + A
    # t0 ca sa nu impart la ceva aproape de 0 (pe cer de exemplu)
    t = np.maximum(t, t0)
    # t devine (H, W, 1) ca sa se imparta toate cele 3 canale la acelasi t
    t = t[:, :, np.newaxis]
    return (image - A) / t + A


def dcp(image, patch_size=15, omega=0.95, t0=0.1):
    # dcp complet: dark channel -> A -> t -> imaginea fara ceata
    # primeste si da imagine rgb uint8, in rest lucrez in float
    img = to_float(image)
    dark = dark_channel(img, patch_size)
    A = atmospheric_light(img, dark)
    t = transmission(img, A, omega, patch_size)
    J = recover(img, t, A, t0)
    return to_uint8(J)


def dcp_guided(image, patch_size=15, omega=0.95, t0=0.1, r=60, eps=1e-3):
    # la fel ca dcp dar netezesc t cu guided filter
    # ghidul e imaginea in gri, asa t are marginile unde le are si imaginea
    # scap de halourile din jurul obiectelor
    img = to_float(image)
    dark = dark_channel(img, patch_size)
    A = atmospheric_light(img, dark)
    t = transmission(img, A, omega, patch_size)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    t = guided_filter(gray, t, r, eps)

    J = recover(img, t, A, t0)
    return to_uint8(J)