import sys

import pika

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare('tasks_queue', durable=True)

body = ' '.join(sys.argv[1:]) or 'Hello...'
channel.basic_publish(
    exchange='',
    routing_key='tasks_queue',
    body=body,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
    ),
)

connection.close()
