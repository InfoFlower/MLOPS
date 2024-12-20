requirementsFilePath="requirements.txt"

echo "Création de l'environnement virtuel Python..."
python -m venv .env

echo "Activation de l'environnement virtuel..."
source .env/bin/activate

function get_installed_python_packages {
    pipListOutput=$(pip list)
    lines=$(echo "$pipListOutput" | tail -n +3)
    packageNames=$(echo "$lines" | awk '{print $1}')
    echo "$packageNames"
}

echo "Mise à jour de pip..."
.env/bin/python -m pip install -U pip
installed_packages=$(get_installed_python_packages)
requirements=$(cat $requirementsFilePath)

for package in $requirements; do
    echo "Installation de $package..."
    if ! echo "$installed_packages" | grep -q "^$package$"; then
        pip install $package
    else
        echo "Package $package already installed"
    fi
done

echo "Démarrage du serveur MLFLOW"
mlflow server --host 127.0.0.1 --port 8080