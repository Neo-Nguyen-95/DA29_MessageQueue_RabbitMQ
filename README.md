# MINI PROJECT

## Flow
1. POST request containing payload through API (FastAPI)
2. Publish to RabbitMQ & return a submit_id
3. Workers process the payload & save result to Redis (SETEX submit_id ttl result_value)
4. GET request to Redis for result

