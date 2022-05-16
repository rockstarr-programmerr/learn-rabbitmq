import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare('hello')

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='ĐCSVN MN!',
)
print('Sent!')

connection.close()
