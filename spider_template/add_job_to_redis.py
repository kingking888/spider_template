import pickle
import time
from itertools import chain
from datetime import datetime
from spider_template.items import TemplateItem
from spider_template.db_actions.redis_action import RedisAction
from spider_template.db_actions.mongo_action import TemplateInfo
from spider_template.settings import REDIS_KEY


# from project.utils.logger import logger


class Rules(object):

    @staticmethod
    def is_run(record: TemplateItem) -> bool:
        return record.is_run

    @staticmethod
    def is_valid(record: TemplateItem) -> bool:
        return record.is_valid

    @staticmethod
    def job_need_run(record: TemplateItem) -> bool:
        return record.job_next_time <= datetime.now()


class BaseSource(object):
    query = {}

    def __init__(self, db_action):
        self.db_action = db_action
        self.rules = Rules()

    def get_jobs(self):
        filter_rules = [self.rules.is_run, self.rules.is_valid, self.rules.job_need_run]
        for d in self.db_action.find(self.query):
            template = TemplateItem(**d)
            if all(r(template) for r in filter_rules):
                yield template


class Scheduler(object):

    def __init__(self):
        self.mongo_action = TemplateInfo()
        self.redis_action = RedisAction()

    @property
    def jobs(self):
        return chain(BaseSource(self.mongo_action).get_jobs(), )

    def start(self):
        job_num = 0
        for job_num, job in enumerate(self.jobs, start=1):
            task = pickle.dumps(job)
            self.redis_action.push(REDIS_KEY, task)
            self.mongo_action.update_one({"_id": job._id}, {"$set": {"job_next_time": job.compute_job_next_time(),
                                                                     "last_fetch_time": datetime.now()}})
            print('push in')
        # logger.info("到达运行时间模板数: {}".format(job_num))


if __name__ == "__main__":
    scheduler = Scheduler()
    while True:

        scheduler.start()
        time.sleep(5)
