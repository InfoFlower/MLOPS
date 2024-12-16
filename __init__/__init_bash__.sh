#!/bin/bash

requirementsFilePath="requirements.txt"

echo "Création de l'environnement virtuel Python..."
python3 -m venv .env

echo "Activation de l'environnement virtuel..."
source .env/bin/activate

echo "Mise à jour de pip..."
python -m pip install -U pip

echo "Installation des packages depuis $requirementsFilePath..."
while IFS= read -r package; do
    echo "Installation de $package..."
    pip install $package
done < "$requirementsFilePath"

echo "Installation terminée."