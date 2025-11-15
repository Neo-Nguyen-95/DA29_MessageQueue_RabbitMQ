import pika
import time

BATCH_SIZE = 50
BATCH_TIMEOUT = 2  # seconds

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)

batch = []
last_message_time = time.time()

def process_batch():
    global batch, last_message_time
    if not batch:
        return
    
    print(f"\n[🔥] Processing batch of size {len(batch)}...")
    time.sleep(1)  # simulate ML model work
    print("[✔] Batch completed.\n")
    
    # Ack all messages
    for ch, method in batch:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    batch = []
    last_message_time = time.time()

print(" [*] Waiting for messages. Batch worker started.\n")

while True:
    # Try to get a message without blocking
    method_frame, properties, body = channel.basic_get(queue='task_queue', auto_ack=False)

    if method_frame:
        # A message was received
        print(f"[x] Received: {body.decode()}")
        batch.append((channel, method_frame))
        last_message_time = time.time()

        # If batch full → process immediately
        if len(batch) >= BATCH_SIZE:
            process_batch()

    else:
        # No message received → check timeout
        if batch and (time.time() - last_message_time >= BATCH_TIMEOUT):
            process_batch()

        # Avoid burning CPU
        time.sleep(0.05)
