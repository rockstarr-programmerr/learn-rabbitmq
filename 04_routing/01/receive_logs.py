import pika


connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare('logs_direct', exchange_type='direct')

levels = ('debug', 'info', 'warning', 'error')

# Log to console
console_log_queue = channel.queue_declare('', exclusive=True)

def console_log_callback(ch, method, properties, body):
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

for level in levels:
    channel.queue_bind(
        queue=console_log_queue.method.queue,
        exchange='logs_direct',
        routing_key=level,
    )

channel.basic_consume(
    queue=console_log_queue.method.queue,
    on_message_callback=console_log_callback,
)

# Log to file
file_log_queue = channel.queue_declare('', exclusive=True)

def file_log_callback(ch, method, properties, body):
    with open('error.log', mode='ab') as f:
        f.write(body)
        f.write('\n'.encode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.queue_bind(
    queue=file_log_queue.method.queue,
    exchange='logs_direct',
    routing_key='error',
)
channel.basic_consume(
    queue=file_log_queue.method.queue,
    on_message_callback=file_log_callback,
)

channel.start_consuming()
