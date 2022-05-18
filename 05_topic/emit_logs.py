import sys
import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) >= 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'ĐCSVN MN!'

channel.basic_publish(
    exchange='topic_logs',
    routing_key=routing_key,
    body=message,
)

connection.close()
