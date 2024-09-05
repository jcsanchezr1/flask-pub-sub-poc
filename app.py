import json

from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

app = Flask(__name__)

# Cargar configuración desde http-client.env.json
with open('http-client.env.json') as config_file:
    config = json.load(config_file)['local']

project_id = config['id-proyecto']
topic_id = "message"
subscription_id = "message.gestor-llamadas-principal"

publisher_client = pubsub_v1.PublisherClient()
topic_path = publisher_client.topic_path(project_id, topic_id)
subscriber_client = pubsub_v1.SubscriberClient()
subscription_path = subscriber_client.subscription_path(project_id, subscription_id)


def pull_messages_from_subscription(subscription_path_param):
    subscriber = pubsub_v1.SubscriberClient()
    messages = []

    pull_request = pubsub_v1.types.PullRequest(
        subscription=subscription_path_param,
        max_messages=1
    )

    # Obtener mensajes
    try:
        response = subscriber.pull(request=pull_request, timeout=5)  # Timeout de 5 segundos
    except Exception as e:
        print(f"Error pulling messages: {e}")
        return messages

    # Reconocer mensajes
    ack_ids = []
    for msg in response.received_messages:
        messages.append(msg.message.data.decode('utf-8'))
        ack_ids.append(msg.ack_id)

    # Reconocer mensajes en una sola llamada
    if ack_ids:
        acknowledge_request = pubsub_v1.types.AcknowledgeRequest(
            subscription=subscription_path_param,
            ack_ids=ack_ids
        )
        try:
            subscriber.acknowledge(request=acknowledge_request)
        except Exception as e:
            print(f"Error acknowledging messages: {e}")

    return messages


@app.route('/publish', methods=['POST'])
def publish_message():
    message = request.json.get('message', '')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Publicar el mensaje en el tópico
        future = publisher_client.publish(topic_path, message.encode('utf-8'))
        message_id = future.result()  # Esperar a que la publicación se complete
        return jsonify({'message_id': message_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/consume', methods=['GET'])
def consume_messages():
    messages = pull_messages_from_subscription(subscription_path)
    return jsonify({'messages': messages}), 200


if __name__ == '__main__':
    app.run(debug=True)
