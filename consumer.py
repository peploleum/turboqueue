# -*- coding: UTF-8 -*-
import pika
import sys

printPrefix = '[consumer]'
try:
    rabbitMqHost = sys.argv[1]
    print(printPrefix, 'running with parameter:', rabbitMqHost)
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'

creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
parameters = pika.ConnectionParameters(host=rabbitMqHost, port=5672, virtual_host='/', credentials=creds,
                                       connection_attempts=10, retry_delay=5)


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
