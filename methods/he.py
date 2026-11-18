import cv2

def histogram_equalization(image):
    # cresc contrastul intinzand intensitatile pe tot intervalul 0-255
    # nu stie nimic de ceata, doar face imaginea mai contrastata
    # primeste si da imagine rgb uint8

    # trec in ycrcb ca sa separ luminozitatea (y) de culoare (cr, cb)
    # daca egalizez r, g, b separat se strica culorile
    ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    y, cr, cb = cv2.split(ycrcb)

    # egalizez doar luminozitatea
    # se face cu histograma + cdf, fiecare nivel de gri e mapat dupa cati pixeli sunt sub el
    y_equalized = cv2.equalizeHist(y)

    # pun la loc y-ul nou cu culorile originale
    ycrcb_equalized = cv2.merge([y_equalized, cr, cb])

    # inapoi in rgb
    return cv2.cvtColor(ycrcb_equalized, cv2.COLOR_YCrCb2RGB)