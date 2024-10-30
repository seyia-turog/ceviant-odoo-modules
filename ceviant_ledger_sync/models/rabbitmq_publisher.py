import pika
import json
import random
import string
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.DEBUG)
load_dotenv('myenv.env')

def generate_batch_reference(length=6):
    """Generate a unique alphanumeric batch reference starting with 'resp-' followed by 6 random digits."""
    characters = string.digits  # Only digits for the random part
    random_digits = ''.join(random.choice(characters) for _ in range(length))
    return f'resp-{random_digits}'


import os
import pika
import logging

def get_rabbitmq_connection():
    """Retrieve RabbitMQ connection parameters from environment variables."""
    host = os.getenv("RABBITMQ_HOST", 'rabbitmq')
    port = os.getenv("RABBITMQ_PORT", 5672)
    virtual_host = os.getenv("RABBITMQ_VHOST", '/')
    username = os.getenv("RABBITMQ_USERNAME", 'guest')
    password = os.getenv("RABBITMQ_PASSWORD", 'guest')

    if host is None:
        logging.error("RABBITMQ_HOST environment variable is not set.")
        raise ValueError("RABBITMQ_HOST is not set in the environment variables.")

    try:
        port = int(port)
    except ValueError:
        logging.error(f"Invalid port value: {port}. Must be an integer.")
        raise

    return pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host,
                                     credentials=pika.PlainCredentials(username, password))



def publish_journal_entry_to_rabbitmq(payload):
    """Publish the validated payload to RabbitMQ with a batch reference."""
    try:
        logging.info("Trying to connect to RabbitMQ...")
        connection_parameters = get_rabbitmq_connection()
        connection = pika.BlockingConnection(connection_parameters)

        channel = connection.channel()
        logging.info("Connected to RabbitMQ")

        channel.queue_declare(queue='transaction_queue')

        batch_ref = generate_batch_reference()
        message = {
            'batch_ref': batch_ref,
            'payload': payload
        }

        channel.basic_publish(exchange='', routing_key='transaction_queue', body=json.dumps(message))
        logging.info(f"Message published with batch reference: {batch_ref}")

        connection.close()
        return batch_ref

    except Exception as e:
        logging.error(f"Failed to publish to RabbitMQ: {str(e)}")
        return None


def publish_account_entry_to_rabbitmq(payload):
    try:
        logging.info("Trying to connect to RabbitMQ for account entry...")
        connection_parameters = get_rabbitmq_connection()
        connection = pika.BlockingConnection(connection_parameters)

        channel = connection.channel()
        logging.info("Connected to RabbitMQ for account entry")

        channel.queue_declare(queue='account_queue')

        batch_ref = generate_batch_reference()
        message = {
            'batch_ref': batch_ref,
            'payload': payload
        }

        channel.basic_publish(exchange='', routing_key='account_queue', body=json.dumps(message))
        logging.info(f"Account entry published with batch reference: {batch_ref}")

        connection.close()
        return batch_ref

    except Exception as e:
        logging.error(f"Failed to publish account entry to RabbitMQ: {str(e)}")
        return None


def publish_journal_entry_update_to_rabbitmq(payload):
    """Publish the validated payload to RabbitMQ with a batch reference."""
    try:
        logging.info("Trying to connect to RabbitMQ...")
        connection_parameters = get_rabbitmq_connection()
        connection = pika.BlockingConnection(connection_parameters)

        channel = connection.channel()
        logging.info("Connected to RabbitMQ")

        channel.queue_declare(queue='update_journal_queue')

        batch_ref = generate_batch_reference()
        message = {
            'batch_ref': batch_ref,
            'payload': payload
        }

        channel.basic_publish(exchange='', routing_key='update_journal_queue', body=json.dumps(message))
        logging.info(f"Message published with batch reference: {batch_ref}")

        connection.close()
        return batch_ref

    except Exception as e:
        logging.error(f"Failed to publish to RabbitMQ: {str(e)}")
        return None