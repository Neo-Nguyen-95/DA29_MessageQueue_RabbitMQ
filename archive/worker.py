import pika
import time

# 1. Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
    )
channel = connection.channel()

# 2. Declare the same queue
channel.queue_declare(queue='task_queue', durable=True)

# 3. Tell RabbitMQ to send message (prefetch=…)
channel.basic_qos(prefetch_count=1)  # Only accept 1 message / time

# 4. Receive and process messages
# 5. Send an ACK
def callback(ch, method, properties, body):
    print(" Received:", body.decode())
    
    time.sleep(1)  # Similate work
    
    print (" Done!")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(
    queue='task_queue',
    on_message_callback=callback
    )

print(" Waiting for messages. Press Control+C to exit!")
channel.start_consuming()


