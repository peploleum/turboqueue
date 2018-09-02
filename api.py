# -*- coding: UTF-8 -*-
import pika


def do_connect(hostname, port):
    creds = pika.PlainCredentials(username='rabbitmq', password='rabbitmq')
    parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host='/', credentials=creds,
                                           connection_attempts=10, retry_delay=5)
    try:
        print('connecting with', parameters.host, parameters.port)
        connection = pika.BlockingConnection(parameters)
        return connection
    except RuntimeError:
        print('failed connecting with parameters', parameters.host, parameters.port)
        raise
