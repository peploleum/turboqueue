# -*- coding: UTF-8 -*-
import sys
import time
import uuid
import random
import api

producerId = str(uuid.uuid1())
printPrefix = '[producer ' + producerId + ']'
try:
    rabbitMqHost = sys.argv[1]
    rabbitMqPort = sys.argv[2]
    rabbitMqQueueName = sys.argv[3]
    print(printPrefix, 'running with parameter:', rabbitMqHost)
    print(printPrefix, 'running with parameter:', rabbitMqPort)
    print(printPrefix, 'running with parameter:', rabbitMqPort)
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'
    rabbitMqPort = 5672
    rabbitMqQueueName = 'hello'
try:
    print(printPrefix, 'connecting')
    connection = api.do_connect(rabbitMqHost, rabbitMqPort)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    print(printPrefix, 'declaring queue', rabbitMqQueueName)
    channel.queue_declare(queue=rabbitMqQueueName)
    while True:
        messageBody = str(random.randint(1, 3))
        print(printPrefix, 'publishing message', messageBody)
        channel.basic_publish(exchange='', routing_key=rabbitMqQueueName, body=messageBody)
        print(printPrefix, '[x] Sent', messageBody)
        time.sleep(3)
except RuntimeError:
    print(printPrefix, 'failed connecting with parameters')
finally:
    print(printPrefix, 'closing connection')
    connection.close()
