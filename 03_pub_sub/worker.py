import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('logs', exchange_type='fanout')
queue_declare_result = channel.queue_declare('', exclusive=True)
channel.queue_bind(queue_declare_result.method.queue, 'logs')

def callback(ch, method, properties, body):
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue_declare_result.method.queue,
    on_message_callback=callback,
)

channel.start_consuming()
