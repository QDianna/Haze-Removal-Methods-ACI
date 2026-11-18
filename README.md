# Haze-Removal-Methods-ACI

Proiectul analizeaza problema eliminarii cetii dintr-o singura imagine, 
relevanta pentru fotografie, supraveghere video si aplicatii bazate pe computer vision. 
Sunt comparate mai multe abordari: egalizarea histogramei, metoda Dark Channel Prior 
si varianta sa cu guided filter, precum si o metoda bazata pe retele neuronale (AOD-Net). 
Evaluarea se realizeaza pe seturi de date publice care contin perechi de imagini cu 
si fara ceata (RESIDE, O-HAZE). Finalitatea consta intr-o aplicatie demonstrator.

## Instalare

    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Rulare

Momentan metodele se ruleaza din scripturi, urmand a fi realizata o interfata grafica 
in urmatoarele sprinturi.

Pentru a aplica metodele pe subsetul de imagini de test (metoda se alege din variabila METHOD) 
se ruleaza:

    python run_methods.py

Rezultatele se salveaza in outputs/'metoda'/.

## Work in progress

### Sprint 1

- alegerea temei: eliminarea cetii dintr-o singura imagine
- studiul modelului de imprastiere atmosferica
- selectarea metodelor de comparat: HE, DCP, DCP + guided filter, AOD-Net
- alegerea seturilor de date (RESIDE, O-HAZE) si a metricilor (PSNR, SSIM)

### Sprint 2

- configurarea mediului de lucru
- implementarea histogram equalization
- implementarea dark channel prior
- implementarea guided filter si a variantei DCP + guided filter
- pregatirea unui subset de test (HSTS) din RESIDE
(https://sites.google.com/view/reside-dehaze-datasets/reside-standard)
- rularea celor 3 metode pe subsetul de test si salvarea rezultatelor