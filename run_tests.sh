#!/bin/bash
set -e  # Lopettaa skriptin, jos jokin komento epäonnistuu

echo "Käynnistetään sovellus..."
poetry run python app.py &
APP_PID=$!

echo "Odotetaan, että sovellus käynnistyy..."
while ! nc -z 127.0.0.1 5000; do
    sleep 0.1
done
echo "Sovellus käynnissä!"

echo "Ajetaan Robot Framework -testit..."
poetry run robot tests/

echo "Pysäytetään sovellus..."
kill $APP_PID || echo "Prosessi $APP_PID ei ollut käynnissä."

echo "Testit suoritettu."
