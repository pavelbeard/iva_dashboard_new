import aioredis
import redis


class RedisClient:
    @staticmethod
    async def client(redis_conn_data: tuple | list):
        host, port, username, password = redis_conn_data
        connection = redis.Redis(host=host, port=int(port),
                                 username=username, password=password,
                                 decode_responses=True)
        return await connection.ping()

