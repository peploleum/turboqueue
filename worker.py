# -*- coding: UTF-8 -*-
import sys
import time
import uuid

import api

workerId = str(uuid.uuid1())
printPrefix = '[worker ' + workerId + ']'
try:
    rabbitMqHost = sys.argv[1]
    print(printPrefix, 'running with parameter:', rabbitMqHost)
except IndexError:
    print('rabbitMq hostname must be the first parameter falling back on localhost')
    rabbitMqHost = 'localhost'


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
    connection = api.do_connect(rabbitMqHost)
    print(printPrefix, 'opening channel')
    channel = connection.channel()
    queueName = 'hello'
    print(printPrefix, 'declaring queue', queueName)
    channel.queue_declare(queue=queueName)
    print(printPrefix, 'consuming messages from queue', queueName)
    channel.basic_consume(callback, queue=queueName)
    print(printPrefix, ' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except RuntimeError:
    print(printPrefix, 'failed connecting')
finally:
    print(printPrefix, 'worker working')
