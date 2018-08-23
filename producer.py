# -*- coding: UTF-8 -*-
import pika

printPrefix = '[producer]'

creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
connectionString = 'amqp://rabbitmq:rabbitmq@localhost:5672/%2F'
try:
    print(printPrefix, 'connecting with ', connectionString)
    urlConnection = pika.BlockingConnection(pika.connection.URLParameters(connectionString))
except RuntimeError:
    print(printPrefix, 'failed connecting with ', connectionString)
finally:
    print(printPrefix, 'closing connection ', connectionString)
    urlConnection.close()

parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=creds)
try:
    print(printPrefix, 'connecting with', parameters.host, parameters.port)
    connection = pika.BlockingConnection(parameters)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print(printPrefix, 'declaring queue', queueName)
    channel.queue_declare(queue=queueName)
    messageBody = 'Hello Dude'
    print(printPrefix, 'publishing message', messageBody)
    channel.basic_publish(exchange='', routing_key=queueName, body=messageBody)
    print(printPrefix, '[x] Sent', messageBody)
except RuntimeError:
    print(printPrefix, 'failed connecting with parameters', parameters.host, parameters.port)
finally:
    print(printPrefix, 'closing connection', parameters.host, parameters.port)
