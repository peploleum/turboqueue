# -*- coding: UTF-8 -*-
import sys

import api

printPrefix = '[consumer]'
try:
    rabbitMqHost = sys.argv[1]
    print(printPrefix, 'running with parameter:', rabbitMqHost)
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'


def callback(ch, method, properties, body):
    print(printPrefix, " [x] Received %r" % body)


try:
    print(printPrefix, 'connecting...')
    connection = api.do_connect(rabbitMqHost)
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
    print(printPrefix, 'failed connecting')
finally:
    print(printPrefix, 'consumer is consuming')
