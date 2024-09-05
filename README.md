# flask-pub-sub-poc

POC Flask with pub sub

Para ejecutar el proyecto es necesario creaar estas dos variables de entorno:

```
export PUBSUB_EMULATOR_HOST="localhost:8120"
export PUBSUB_PROJECT_ID="abcall"
```

1. Instalar dependencias
2. Iniciar y ejecutar el emulador de Pub/Sub

`docker compose up -d pubsub`

3. Crear topico `message` y subscripción `message.gestor-llamadas-principal` en el emulador de PubSub
4. Ejecutar applicacion

`flask run`

5. Ejecutar peticiones (POC Flask PubSub.postman_collection.json) y validar respuestas
