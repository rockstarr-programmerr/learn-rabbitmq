import sys
import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('logs_direct', exchange_type='direct')

try:
    message = sys.argv[1]
except IndexError:
    message = 'ĐCSVN MN!'

try:
    level = sys.argv[2]
except IndexError:
    level = 'info'

channel.basic_publish(
    exchange='logs_direct',
    routing_key=level,
    body=message,
)

connection.close()
