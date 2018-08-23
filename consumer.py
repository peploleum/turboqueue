# -*- coding: UTF-8 -*-
import pika

printPrefix = '[consumer]'
creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=creds)


def callback(ch, method, properties, body):
    print(printPrefix, " [x] Received %r" % body)


try:
    print(printPrefix, 'connecting with', parameters.host, parameters.port)
    connection = pika.BlockingConnection(parameters)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print(printPrefix, 'declaring queue', queueName)
    channel.queue_declare(queue=queueName)
    print(printPrefix, 'consuming messages from queue', queueName)
    channel.basic_consume(callback, queue=queueName, no_ack=True)
    print(printPrefix, ' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except RuntimeError:
    print(printPrefix, 'failed connecting with parameters', parameters.host, parameters.port)
finally:
    print(printPrefix, 'closing connection', parameters.host, parameters.port)
