# -*- coding: UTF-8 -*-
import sys
import time
import uuid

import api

workerId = str(uuid.uuid1())
printPrefix = '[worker ' + workerId + ']'
try:
    rabbitMqHost = sys.argv[1]
    rabbitMqPort = sys.argv[2]
    rabbitMqQueueName = sys.argv[3]
    print(printPrefix, 'running with parameter:', rabbitMqHost)
    print(printPrefix, 'running with parameter:', rabbitMqPort)
    print(printPrefix, 'running with parameter:', rabbitMqQueueName)
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'
    rabbitMqPort = 5672
    rabbitMqQueueName = 'hello'


def callback(ch, method, properties, body):
    print(printPrefix, " [x] Received %r" % body)
    try:
        sleepytime = int(body)
    except ValueError:
        print(printPrefix, 'falling back on default sleeping time')
        sleepytime = 3
        pass
    time.sleep(sleepytime)
    print(printPrefix, ' [x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    print(printPrefix, 'connecting...')
    connection = api.do_connect(rabbitMqHost, rabbitMqPort)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    print(printPrefix, 'declaring queue', rabbitMqQueueName)
    channel.queue_declare(queue=rabbitMqQueueName)
    print(printPrefix, 'consuming messages from queue', rabbitMqQueueName)
    channel.basic_consume(callback, queue=rabbitMqQueueName)
    print(printPrefix, ' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except RuntimeError:
    print(printPrefix, 'failed connecting')
finally:
    print(printPrefix, 'worker working')
