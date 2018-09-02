# -*- coding: UTF-8 -*-
import sys

import api

printPrefix = '[consumer]'
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


def callback(ch, method, properties, body):
    print(printPrefix, " [x] Received %r" % body)


try:
    print(printPrefix, 'connecting...')
    connection = api.do_connect(rabbitMqHost, rabbitMqPort)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    print(printPrefix, 'declaring queue', rabbitMqQueueName)
    channel.queue_declare(queue=rabbitMqQueueName)
    print(printPrefix, 'consuming messages from queue', rabbitMqQueueName)
    channel.basic_consume(callback, queue=rabbitMqQueueName, no_ack=True)
    print(printPrefix, ' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except RuntimeError:
    print(printPrefix, 'failed connecting')
finally:
    print(printPrefix, 'consumer is consuming')
