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
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'

try:
    print(printPrefix, 'connecting')
    connection = api.do_connect(rabbitMqHost)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print(printPrefix, 'declaring queue', queueName)
    channel.queue_declare(queue=queueName)
    while True:
        messageBody = str(random.randint(1, 9))
        print(printPrefix, 'publishing message', messageBody)
        channel.basic_publish(exchange='', routing_key=queueName, body=messageBody)
        print(printPrefix, '[x] Sent', messageBody)
        time.sleep(3)
except RuntimeError:
    print(printPrefix, 'failed connecting with parameters')
finally:
    print(printPrefix, 'closing connection')
    connection.close()
