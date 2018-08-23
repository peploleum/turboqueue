# -*- coding: UTF-8 -*-
import sys
import time
import uuid

import pika

producerId = str(uuid.uuid1())
printPrefix = '[producer ' + producerId + ']'
try:
    rabbitMqHost = sys.argv[1]
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'

creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
parameters = pika.ConnectionParameters(host=rabbitMqHost, port=5672, virtual_host='/', credentials=creds,
                                       connection_attempts=10, retry_delay=5)
try:
    print(printPrefix, 'connecting with', parameters.host, parameters.port)
    connection = pika.BlockingConnection(parameters)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print(printPrefix, 'declaring queue', queueName)
    channel.queue_declare(queue=queueName)
    messageBody = 'Hello Dude from ' + producerId
    while True:
        print(printPrefix, 'publishing message', messageBody)
        channel.basic_publish(exchange='', routing_key=queueName, body=messageBody)
        print(printPrefix, '[x] Sent', messageBody)
        time.sleep(3)
except RuntimeError:
    print(printPrefix, 'failed connecting with parameters', parameters.host, parameters.port)
finally:
    print(printPrefix, 'closing connection', parameters.host, parameters.port)
