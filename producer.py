# -*- coding: UTF-8 -*-
import pika

creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
connectionString = 'amqp://rabbitmq:rabbitmq@localhost:5672/%2F'
try:
    print('[producer] connecting with ', connectionString)
    urlConnection = pika.BlockingConnection(pika.connection.URLParameters(connectionString))
except RuntimeError:
    print('[producer] failed connecting with ', connectionString)
finally:
    print('[producer] closing connection ', connectionString)
    urlConnection.close()

parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=creds)
try:
    print('[producer] connecting with', parameters.host, parameters.port)
    connection = pika.BlockingConnection(parameters)
    print('[producer] opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print('[producer] declaring queue', queueName)
    channel.queue_declare(queue=queueName)
except RuntimeError:
    print('[producer] failed connecting with parameters', parameters.host, parameters.port)
finally:
    print('[producer] closing connection', parameters.host, parameters.port)
