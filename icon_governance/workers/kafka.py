from time import sleep
from typing import Any

from confluent_kafka import (
    DeserializingConsumer,
    KafkaError,
    Producer,
    SerializingProducer,
)
from confluent_kafka.admin import AdminClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import (
    ProtobufDeserializer,
    ProtobufSerializer,
)
from confluent_kafka.serialization import StringDeserializer, StringSerializer
from loguru import logger
from pydantic import BaseModel, validator

# from icon_governance.log import logger
from icon_governance.config import settings
from icon_governance.schemas.governance_prep_processed_pb2 import (
    GovernancePrepProcessed,
)
from icon_governance.schemas.transaction_raw_pb2 import TransactionRaw


class KafkaClient(BaseModel):
    name: str = None
    schema_registry_url: str = settings.SCHEMA_REGISTRY_URL
    schema_registry_client: Any = None
    sleep_seconds: float = 0.25

    session: Any = None

    kafka_server: str = settings.KAFKA_BROKER_URL
    consumer_group: str = None

    topic: str = None

    consumer: Any = None
    consumer_schema: Any = None
    consumer_deserializer: Any = None

    json_producer: Any = None

    protobuf_producer: Any = None
    protobuf_serializer: Any = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.name is None:
            self.name = self.topic

        self.consumer_deserializer = ProtobufDeserializer(TransactionRaw)

        self.consumer = DeserializingConsumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": self.consumer_group,
                "key.deserializer": StringDeserializer("utf_8"),
                "value.deserializer": self.consumer_deserializer,
                "auto.offset.reset": "earliest",
            }
        )

        # Producers
        # Json producer for dead letter queues
        self.json_producer = Producer({"bootstrap.servers": self.kafka_server})

        self.schema_registry_client = SchemaRegistryClient({"url": settings.SCHEMA_REGISTRY_URL})

        self.protobuf_serializer = ProtobufSerializer(
            GovernancePrepProcessed,
            self.schema_registry_client,
            conf={"auto.register.schemas": True},
        )

        self.protobuf_producer = SerializingProducer(
            {
                "bootstrap.servers": self.kafka_server,
                "key.serializer": StringSerializer("utf_8"),
                "value.serializer": self.protobuf_serializer,
            }
        )

        admin_client = AdminClient({"bootstrap.servers": self.kafka_server})
        topics = admin_client.list_topics().topics

        if self.topic and self.topic not in topics:
            raise RuntimeError()

        self.init()

    def produce_json(self, topic, key, value):
        try:
            # https://github.com/confluentinc/confluent-kafka-python/issues/137#issuecomment-282427382
            self.json_producer.produce(topic=topic, value=value, key=key)
            self.json_producer.poll(0)
        except BufferError:
            self.json_producer.poll(1)
            self.json_producer.produce(topic=topic, value=value, key=key)
        self.json_producer.flush()

    def produce_protobuf(self, topic, key, value):
        try:
            self.protobuf_producer.produce(topic=topic, value=value, key=key)
            self.protobuf_producer.poll(0)
        except BufferError:
            self.protobuf_producer.poll(1)
            self.protobuf_producer.produce(topic=topic, value=value, key=key)
        self.protobuf_producer.flush()

    def start(self):
        self.consumer.subscribe([self.topic])
        logger.info("Kafka consumer connected...")

        while True:
            # Poll for a message
            msg = self.consumer.poll(timeout=1)

            # If no new message, try again
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    err_msg = "{topic} {partition} reached end at offset {offset}".format(
                        topic=msg.topic(),
                        partition=msg.partition(),
                        offset=msg.offset(),
                    )
                    logger.error("Kafka consumer: " + err_msg)
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    logger.error(
                        f"Kafka consumer: Kafka topic {msg.topic()} not ready. Restarting."
                    )
                elif msg.error():
                    logger.error("Kafka consumer: " + str(msg.error()))
                sleep(1)
                continue
            else:
                self.process(msg)
                self.consumer.commit()

        # Flush the last of the messages
        self.json_producer.flush()

    def init(self):
        """Overridable process that runs on init."""
        pass

    def process(self, msg):
        """Overridable process that processes each message."""
        pass
