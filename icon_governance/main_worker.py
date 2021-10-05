import asyncio
from multiprocessing.pool import ThreadPool
from threading import Thread

from loguru import logger
from prometheus_client import start_http_server

from icon_governance.config import settings
from icon_governance.db import init_db
from icon_governance.workers.transactions import transactions_worker

logger.info("Starting metrics server.")
metrics_pool = ThreadPool(1)
metrics_pool.apply_async(start_http_server, (settings.METRICS_PORT, settings.METRICS_ADDRESS))

transactions_worker_thread = Thread(
    target=transactions_worker,
    args=(),
)

# prep_cron = Thread(
#     target=transactions_worker,
#     args=(),
# )

transactions_worker_thread.start()
