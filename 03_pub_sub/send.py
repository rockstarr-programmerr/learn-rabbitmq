import sys

import pika

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'ĐCSVN MN!'

channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
)

connection.close()
