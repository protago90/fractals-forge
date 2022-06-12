import time
from celery import Celery
from celery.result import AsyncResult
from typing import Dict, List

from fastforge.conf import Config


PUB_FAKE_IMG = 'static/src/fractal.png'


conf = Config().celery
celery = Celery(__name__, broker=conf.broker_url, backend=conf.result_url)


@celery.task(name='create_task')
def create_task() -> bool:
    # TODO: This is just a demo! Here service task computation is faked.
    time.sleep(10)
    return True

def read_tasks_info(uuids: List[str]) -> List[Dict[str, str]]:
    # TODO: This is just a demo! Here service task outcome is mocked.
    return [{'id': uuid, 'status': AsyncResult(uuid).status, 'src': PUB_FAKE_IMG}
            for uuid in uuids]
