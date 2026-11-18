import os
import time
from methods.utils import load_image, save_image
from methods.he import histogram_equalization
from methods.dcp import dcp, dcp_guided

# iau toate imaginile cu ceata din input, aplic metodele pe ele
# si pun rezultatele in outputs/<metoda>/
# ruleaza din radacina proiectului, de acolo sunt caile

# imaginile cu ceata din hsts (in original/ sunt cele fara ceata, pentru comparatie)
INPUT_DIR = "inputs/HSTS/synthetic/synthetic"
OUTPUT_DIR = "outputs"
# aici aleg ce rulez
METHOD = "all"   # "he", "dcp", "dcp_guided" sau "all"

# nume -> functie, toate primesc si dau rgb uint8 asa ca le pot apela la fel
# metoda noua = o linie noua aici
METHODS = {
    "he": histogram_equalization,
    "dcp": dcp,
    "dcp_guided": dcp_guided,
}


def run_method(name, method):
    # aplic o metoda pe toate imaginile din INPUT_DIR
    # fiecare metoda are folderul ei in outputs
    out_dir = os.path.join(OUTPUT_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    # doar imaginile, in ordine alfabetica
    files = sorted(f for f in os.listdir(INPUT_DIR)
                   if f.lower().endswith((".jpg", ".jpeg", ".png")))

    for file in files:
        image = load_image(os.path.join(INPUT_DIR, file))

        # masor doar cat dureaza metoda, fara citire si salvare
        start = time.perf_counter()
        result = method(image)
        elapsed = time.perf_counter() - start

        # salvez in png ca sa nu adaug artefacte de compresie jpg
        out_name = os.path.splitext(file)[0] + ".png"
        save_image(os.path.join(out_dir, out_name), result)
        print(f"[{name}] {file} -> {out_name} ({elapsed:.2f} s)")


# all = toate metodele, altfel doar cea aleasa
if METHOD == "all":
    selected = METHODS
else:
    selected = {METHOD: METHODS[METHOD]}

for name, method in selected.items():
    run_method(name, method)