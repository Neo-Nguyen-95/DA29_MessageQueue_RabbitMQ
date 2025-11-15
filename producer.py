import pika

# 1. Create connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
    )

# 2. Create channel
channel = connection.channel()

# 3. Tell which queue to use
channel.queue_declare(queue="task_queue", durable=True)

# 4. Publish the message
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body='Hello RabbitMQ!',
    properties=pika.BasicProperties(
        delivery_mode=2  # Make message persistent
        )
    )

print(" Sent 'Hello RabbitMQ!'")

# 5. Close connection
connection.close()