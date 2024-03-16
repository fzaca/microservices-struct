#!/bin/sh

MAX_ATTEMPTS=10
ATTEMPT=0


# Comprueba si los volúmenes están presentes
if [ ! "$(docker volume ls -q -f name=kong_data)" ]; then
    # Los volúmenes no están presentes, ejecuta la inicialización
    echo "Running the initialization for the first time..."

    apk --no-cache add curl

    # Espera a que Kong esté disponible
    while ! curl -s http://kong:8001 > /dev/null; do
        echo "Waiting for Kong to be available..."
        sleep 5
    done

    # Carga los servicios y rutas...

    # Test Servicue
    curl -i -X POST http://kong:8001/services/ \
        --data "name=example-service" \
        --data "url=http://httpbin.org/headers"
fi