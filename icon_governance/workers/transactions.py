import json
from uuid import uuid4

from icon_governance.config import settings
from icon_governance.db import session
from icon_governance.log import logger
from icon_governance.metrics import Metrics
from icon_governance.models.preps import Prep
from icon_governance.utils.details import get_details
from icon_governance.workers.kafka import KafkaClient

metrics = Metrics()


class TransactionsWorker(KafkaClient):
    msg_count: int = 0
    preps_created: int = 0
    preps_updated: int = 0

    def process(self, msg):
        # Filter on only txs to the governance address
        if self.msg_count % 10000 == 0:
            logger.info(
                f"msg count {self.msg_count} and block {msg.value().block_number} "
                f"for consumer group {self.consumer_group}"
            )
            metrics.block_height.set(msg.value().block_number)
        self.msg_count += 1

        if msg.key() != settings._governance_address:
            return

        value = msg.value()

        # Ignore any unsuccessful txs
        if value.receipt_status != 1:
            return

        data = json.loads(value.data)

        address = value.from_address
        timestamp = int(value.timestamp, 16) / 1e6

        # Ignore anything without a method call like contract creation events
        if "method" not in data:
            return

        method = data["method"]

        # P-Reps
        if method in ["registerPRep", "setPrep", "unregisterPRep"]:
            params = data["params"]
            details = get_details(params["details"])

            prep = self.session.get(Prep, address)

            if prep is not None:
                if method == "unregisterPRep":
                    logger.info(f"Prep unregistration tx hash {value.hash}")
                    prep.status = "unregistered"

                    self.preps_created += 1
                    metrics.preps_created.set(self.preps_created)

                    self.session.add(prep)
                    self.session.commit()
                    return

                if prep.last_updated_block > value.block_number and method == "setPrep":
                    logger.info(
                        f"Skipping setPrep call in tx_hash {value.hash} because it has since been updated."
                    )
                    return
            else:
                prep = Prep(
                    address=address,
                )

            if prep.last_updated_block is None:
                logger.info(f"Prep update registration tx hash {value.hash}")
                prep.created_block = value.block_number
                prep.created_timestamp = timestamp

            prep.last_updated_block = value.block_number
            prep.last_updated_timestamp = timestamp
            prep.name = params["name"]
            prep.email = params["email"]
            prep.city = params["city"]
            prep.website = params["website"]
            prep.country = params["country"]
            prep.details = params["details"]
            prep.p2p_endpoint = params["p2pEndpoint"]
            prep.node_address = params["nodeAddress"]

            # Add information from details
            for k, v in details.items():
                setattr(prep, k, v)

            self.preps_updated += 1
            metrics.preps_updated.set(self.preps_updated)

            self.session.add(prep)
            self.session.commit()

        # Staking
        if method == "setStake":
            print()

        if method == "setDelegation":
            logger.info(f"{value.block_number}")
            # for i in data['params']['delegations']:
            #     logger.info(str(i))

        if method == "claimIScore":
            print()

        if method == "setGovernanceVariables":
            import sys

            sys.exit(1)

        if method == "registerProposal":
            print()

        if method == "cancelProposal":
            print()

        if method == "voteProposal":
            print()


def transactions_worker():
    kafka = TransactionsWorker(
        session=session,
        topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
        consumer_group=settings.CONSUMER_GROUP_HEAD,
    )

    kafka.start()


if __name__ == "__main__":
    transactions_worker()
