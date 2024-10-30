import pika
import json
import logging
from odoo import models, api
from .journal_utils import process_transaction, update_journal_entry_in_database
from .account_utils import create_account

logging.basicConfig(level=logging.DEBUG)


class BatchProcessor(models.Model):
    _name = 'custom_journal_entry.batch_processor'

    def send_notification(self, message):
        """Send notification about the transaction or account processing status."""
        logging.info(f"Notification: {message}")

    def process_message(self, ch, method, properties, body):
        """Process a single message from RabbitMQ and route it to the appropriate handler."""
        batch_ref = None
        try:
            message = json.loads(body)
            batch_ref = message.get('batch_ref')
            payload = message.get('payload')
            queue_type = method.routing_key

            if queue_type == 'transaction_queue':
                logging.info(f"Processing transaction for batch {batch_ref} --")
                success = process_transaction(payload)
                if success:
                    self.send_notification(f"Journal batch {batch_ref} processed and updated successfully.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    self.send_notification(f"Failed to process and update journal batch {batch_ref}.")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            elif queue_type == 'account_queue':
                success = create_account(payload)
                if success:
                    self.send_notification(f"Account batch {batch_ref} processed successfully.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    self.send_notification(f"Failed to process account batch {batch_ref}.")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            elif queue_type == 'update_journal_queue':
                logging.info(f"Updating journal entry for batch {batch_ref} --")
                success = update_journal_entry_in_database(payload)
                if success:
                    self.send_notification(f"Journal entry batch {batch_ref} updated successfully.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    self.send_notification(f"Failed to update journal entry batch {batch_ref}.")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        except json.JSONDecodeError as e:
            self.send_notification(f"JSON decode error processing batch {batch_ref}: {str(e)}")
            logging.error(f"JSON decode error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        except pika.exceptions.AMQPChannelError as e:
            self.send_notification(f"AMQP error processing batch {batch_ref}: {str(e)}")
            logging.error(f"AMQP error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        except Exception as e:
            self.send_notification(f"Unexpected error processing batch {batch_ref}: {str(e)}")
            logging.error(f"Unexpected error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        finally:
            pass

    def fetch_and_process_messages(self):
        """Fetch messages from RabbitMQ (both queues) and process them."""
        connection_parameters = pika.ConnectionParameters(
            host='rabbitmq', port=5672, virtual_host='/',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        channel.queue_declare(queue='transaction_queue')
        channel.queue_declare(queue='account_queue')
        channel.queue_declare(queue='update_journal_queue')

        batch_messages = {}

        method_frame, header_frame, body = channel.basic_get(queue='transaction_queue')
        while method_frame:
            message = json.loads(body)
            batch_ref = message.get('batch_ref')

            if batch_ref not in batch_messages:
                batch_messages[batch_ref] = []

            batch_messages[batch_ref].append((method_frame, body, 'transaction_queue'))
            method_frame, header_frame, body = channel.basic_get(queue='transaction_queue')

        method_frame, header_frame, body = channel.basic_get(queue='account_queue')
        while method_frame:
            message = json.loads(body)
            batch_ref = message.get('batch_ref')

            if batch_ref not in batch_messages:
                batch_messages[batch_ref] = []

            batch_messages[batch_ref].append((method_frame, body, 'account_queue'))
            method_frame, header_frame, body = channel.basic_get(queue='account_queue')

        method_frame, header_frame, body = channel.basic_get(queue='update_journal_queue')
        while method_frame:
            message = json.loads(body)
            batch_ref = message.get('batch_ref')

            if batch_ref not in batch_messages:
                batch_messages[batch_ref] = []

            batch_messages[batch_ref].append((method_frame, body, 'update_journal_queue'))
            method_frame, header_frame, body = channel.basic_get(queue='update_journal_queue')

        for batch_ref, messages in batch_messages.items():
            for method_frame, body, queue_type in messages:
                self.process_message(channel, method_frame, None, body)

        connection.close()

    @api.model
    def run_batch_processor(self):
        """Run the batch processor as a cron job."""
        self.fetch_and_process_messages()
