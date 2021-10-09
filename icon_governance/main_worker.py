from multiprocessing.pool import ThreadPool
from threading import Thread

from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.workers.cron import cron_worker
from icon_governance.workers.transactions import (
    transactions_worker_head,
    transactions_worker_tail,
)

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

transactions_worker_head_thread = Thread(
    target=transactions_worker_head,
    args=(),
)

transactions_worker_tail_thread = Thread(
    target=transactions_worker_tail,
    args=(),
)

prep_cron = Thread(
    target=cron_worker,
    args=(),
)

transactions_worker_head_thread.start()
transactions_worker_tail_thread.start()
prep_cron.start()
