from prometheus_client import Gauge


class Metrics:
    def __init__(self):

        self.preps_created = Gauge(
            "preps_created",
            "Num created.",
        )

        self.preps_updated = Gauge(
            "preps_updated",
            "Num updated.",
        )

        self.block_height = Gauge(
            "max_block_number_transactions_raw",
            "The block height",
        )
