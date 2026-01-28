# MINI PROJECT

## Flow
FastAPI → RabbitMQ → Worker → Redis

1. POST request containing payload through API (FastAPI)
2. Publish to RabbitMQ & return a submit_id
3. Workers process the payload & save result to Redis (SETEX submit_id ttl result_value)

FastAPI → Redis → Client

4. GET request to Redis for result

