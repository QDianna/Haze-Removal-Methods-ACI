import cv2


def box(x, r):
    # media pe o fereastra (2r+1) x (2r+1) in jurul fiecarui pixel
    # opencv o face rapid indiferent cat de mare e r
    return cv2.blur(x, (2 * r + 1, 2 * r + 1))


def guided_filter(guide, p, r=60, eps=1e-3):
    # netezesc p (transmisia) dar pastrez marginile din guide (imaginea in gri)
    # presupun ca in fiecare fereastra rezultatul e q = a * guide + b
    # deci unde guide are margini are si q

    # mediile de care am nevoie pe fiecare fereastra
    mean_I = box(guide, r)
    mean_p = box(p, r)
    corr_I = box(guide * guide, r)
    corr_Ip = box(guide * p, r)

    # varianta guide-ului si covarianta guide cu p
    # var = medie(I^2) - medie(I)^2, cov = medie(I*p) - medie(I)*medie(p)
    var_I = corr_I - mean_I * mean_I
    cov_Ip = corr_Ip - mean_I * mean_p

    # coeficientii modelului liniar pentru fiecare fereastra
    # pe margini var e mare -> a mare -> q urmareste guide
    # in zone uniforme var e mic fata de eps -> a aproape 0 -> q e doar media lui p (netezit)
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    # un pixel e in mai multe ferestre, asa ca fac media lui a si b din toate
    mean_a = box(a, r)
    mean_b = box(b, r)

    # rezultatul final q = a * guide + b
    return mean_a * guide + mean_b