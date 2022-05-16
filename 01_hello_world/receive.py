import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare('hello')

def callback(ch, method, properties, body):
    print('Channel:', ch)
    print('Method:', method)
    print('Properties:', properties)
    print('Body:', body.decode())

channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
