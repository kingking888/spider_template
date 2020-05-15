# encoding: utf-8
import redis
import json
import hashlib
import random
from spider_template.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PARAMS


# redis-cli -h 10.174.97.43 -p 8801 -n 0 -a e65f63bb02d3


class RedisAction(object):

    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS["password"])

    def add_set(self, queue_name, *args):
        self.redis.sadd(queue_name, *args)

    def get_random_set(self, queue_name, number):
        return self.redis.srandmember(queue_name, number=number)

    def pop_set(self, queue_name, *args):
        return self.redis.srem(queue_name, *args)

    def members_set(self, queue_name):
        for member in self.redis.smembers(queue_name):
            yield member.decode()

    def push(self, queue_name, data):
        self.redis.rpush(queue_name, data)

    def task_push(self, queue_name, data):
        self.redis.rpush(queue_name, json.dumps(data, default=lambda x: x.__dict__))

    def pop(self, queue_name):
        data = self.redis.lpop(queue_name)
        if data:
            return json.loads(data)
        return ""

    def batch_pop(self, queue_name, nums):

        def filter_node(node):
            return node

        with self.redis.pipeline() as pipe:
            for _ in range(nums):
                pipe.lpop(queue_name)
            pipe_list = pipe.execute()
            for data in filter(filter_node, pipe_list):
                yield data

    def priority_queue_pop(self, queue_name, num):
        """
        优先级队列pop出第一个元素
        :param queue_name: 优先级队列名字
        :param num: pop的数量,
        :param table_name: url进度表名字,不修改状态就不用提供
        :param status_change: 是否更改hbase的状态, 一般不需要修改
        :return: (value, scores) or []
        """
        with self.redis.pipeline() as pipe:
            pipe.zrange(queue_name, 0, num, withscores=True)
            pipe.zremrangebyrank(queue_name, 0, num)
            pipe_list = pipe.execute()[0]
            if not pipe_list:
                return []
            result_list = []
            for data in pipe_list:
                info = json.loads(data[0])
                info.update({"info:priority": data[1]})
                result_list.append(info)
            return result_list

    def make_url_hot(self, url, hot=7200):
        if not url:
            return True
        url = url.split("#")[0]
        url_key = hashlib.md5(url.encode()).hexdigest()
        with self.redis.pipeline() as pipe:
            pipe.get(url_key)
            pipe.setex(url_key, url, hot + random.randint(1, 150))
            return pipe.execute()[0]

    def priority_queue_push(self, queue_name, *args, **kwargs):
        """
        优先级队列插入元素
        :param queue_name: 优先级队列名字
        :param value: 插入值
        :param priority: 优先级(整型)
        :return: None
        """
        if any(args):
            self.redis.zadd(queue_name, *args, **kwargs)

    def priority_queue_len(self, queue_name):
        return self.redis.zcount(queue_name, 0, 10)

    def priority_queue_zrem(self, queue_name, members):
        return self.redis.zrem(queue_name, members)

    def priority_queue_exists(self, queue_name, member):
        if isinstance(member, dict):
            member = json.dumps(member)
        return self.redis.zrank(queue_name, member)

    def priority_queue_range(self, queue_name, start, end, withscores=False):
        return self.redis.zrange(queue_name, start, end, False, withscores=withscores)

    def hset(self, name, key, value):
        return self.redis.hset(name, key, value)

    def hexists(self, name, key):
        return self.redis.hexists(name, key)
