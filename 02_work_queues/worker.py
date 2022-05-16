import pika
import time


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare('tasks_queue', durable=True)

def callback(ch, method, properties, body):
    body = body.decode()
    print('Received %s' % body)
    time.sleep(body.count('.'))
    print('Done!')
    print()
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    'tasks_queue',
    on_message_callback=callback,
)

channel.start_consuming()
