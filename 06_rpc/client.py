import sys
import uuid

import pika


class FibClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        queue_declare_result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = queue_declare_result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.correlation_id = None

    def on_response(self, ch, method, properties, body):
        if properties.correlation_id == self.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.correlation_id = uuid.uuid4().hex

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=str(n),
        )

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


number = int(sys.argv[1]) if len(sys.argv) >= 2 else 5

client = FibClient()
result = client.call(number)
print('Fibonacci number of %d is: %d' % (number, result))
