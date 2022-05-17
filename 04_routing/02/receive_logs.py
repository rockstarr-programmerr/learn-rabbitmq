import sys
import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('logs_direct_2', exchange_type='direct')
queue_declare_result = channel.queue_declare('', exclusive=True)
queue_name = queue_declare_result.method.queue

destination = sys.argv[1] if len(sys.argv) >= 2 else 'console'
levels = sys.argv[2:]
if not levels:
    sys.stderr.write('Usage: %s [console|file] [info] [warning] [error]\n' % sys.argv[0])
    sys.exit(1)

for level in levels:
    channel.queue_bind(
        queue=queue_name,
        exchange='logs_direct_2',
        routing_key=level,
    )

def log_to_console(ch, method, properties, body):
    print('%s: %s' % (method.routing_key, body.decode()))

def log_to_file(ch, method, properties, body):
    with open('logging.log', 'ab') as f:
        f.write(body)
        f.write('\n'.encode())

channel.basic_consume(
    queue=queue_name,
    on_message_callback=(log_to_file if destination == 'file' else log_to_console),
    auto_ack=True,
)

channel.start_consuming()
