import sys
import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('topic_logs', exchange_type='topic')
queue_declare_result = channel.queue_declare('', exclusive=True)
queue_name = queue_declare_result.method.queue

routing_keys = sys.argv[1:]
if not routing_keys:
    sys.stderr.write('Usage: python %s [routing keys]\n' % sys.argv[0])
    sys.exit(1)

for routing_key in routing_keys:
    channel.queue_bind(
        queue=queue_name,
        exchange='topic_logs',
        routing_key=routing_key,
    )

def callback(ch, method, properties, body):
    print('%s: %s' % (method.routing_key, body.decode()))

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
