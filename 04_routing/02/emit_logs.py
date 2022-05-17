import sys
import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs_direct_2', exchange_type='direct')

level = sys.argv[1] if len(sys.argv) >= 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'ĐCSVN MN!'

channel.basic_publish(
    exchange='logs_direct_2',
    routing_key=level,
    body=message,
)

connection.close()
