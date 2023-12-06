from celery import shared_task
import redis
from random import randint

redis_instance = redis.StrictRedis(host='redis', port=6379, db=0)


@shared_task
def send_otp_sms(phone):
    otp = randint(100000, 999999)
    print(otp)
    redis_instance.setex(phone, 60, otp)
