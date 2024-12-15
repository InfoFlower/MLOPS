Write-Host "Activation de l'environnement virtuel..."
& .\.env\Scripts\Activate.ps1

Write-Host "Demarage MLFLOW server"
mlflow server --host 127.0.0.1 --port 8080