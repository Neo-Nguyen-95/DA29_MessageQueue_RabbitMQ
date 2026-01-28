#%% LIB
from fastapi import FastAPI
from pydantic import BaseModel
import json
import time
import uuid
import pika
import redis

#%% PREP CLIENT
# REDIS
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)


#%% WORKING FUNCTION
def slow_recommendaiotion(user_id: str):
    time.sleep(3)
    return [f"question_{i}" for i in range(5)]



#%% API GATEWAY
app = FastAPI()

# Sample post request
""" 
curl \
    -X POST "http://127.0.0.1:8000/recommend2student" \
    -H "Content-Type: application/json" \
    -d '{"student_code":"HL1", "topic_lv4":"2"}'
"""
class StudentRequest(BaseModel):
    student_code: str
    topic_lv4: str

@app.post("/recommend2student")
def get_queue(request: StudentRequest):
    
    submit_id = str(uuid.uuid4())

    # RABBITMQ
    # 1. Create connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
        )

    # 2. Create channel
    channel = connection.channel()

    # 3. Tell which queue to use
    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps({
        "submit_id": submit_id,
            **request.dict()
            }),
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
            )
        )

    print("Sent something!")

    # 5. Close connection
    connection.close()


    return {
        'status': 'success',
        'submit_id': submit_id
        }

"""
curl http://127.0.0.1:8000/result/...
"""

@app.get("/result/{submit_id}")
def get_result(submit_id: str):
    result = redis_client.get(f"result:{submit_id}")

    if not result:
        return {"status": "pending"}
    
    return {
        "status": "done",
        "result": json.loads(result)
    }