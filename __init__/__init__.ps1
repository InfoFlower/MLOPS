$requirementsFilePath = "requirements.txt"

Write-Host "Création de l'environnement virtuel Python..."
python -m venv .env

Write-Host "Activation de l'environnement virtuel..."
& ..\.env\Scripts\Activate

Write-Host "Mise à jour de pip..."
C:\Users\lenovo\Desktop\Cours\034_MLOPS\.env\Scripts\python.exe -m pip install -U pip
$requirements = Get-Content $requirementsFilePath
foreach ($package in $requirements) {
    Write-Host "Installation de $package..."
    pip install $package
}

Write-Host "Installation terminée."
deactivate