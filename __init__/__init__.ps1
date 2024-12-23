$requirementsFilePath = "requirements.txt"

Write-Host "Création de l'environnement virtuel Python..."
python -m venv .env

Write-Host "Activation de l'environnement virtuel..."
.env\Scripts\Activate.ps1

function Get-InstalledPythonPackages {
    $pipListOutput = pip list
    $lines = $pipListOutput -split "`n"
    $packages = $lines | Select-Object -Skip 2
    $packageNames = $packages | ForEach-Object {
        $_.Split()[0]
    }
    return $packageNames
}

Write-Host "Mise à jour de pip..."
C:\Users\lenovo\Desktop\Cours\034_MLOPS\.env\Scripts\python.exe -m pip install -U pip
$Installed_Packages = Get-InstalledPythonPackages
$requirements = Get-Content $requirementsFilePath
foreach ($package in $requirements ) {
    Write-Host "Installation de $package..."
    if($package -notin $Installed_Packages){
    pip install $package}
    else{
        Write-Host "Package $package already installed"
    }
}

Write-Host "Démarrage du serveur MLFLOW"
mlflow server --host 127.0.0.1 --port 8080