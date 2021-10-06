from pydantic import BaseSettings


class Settings(BaseSettings):

    NAME: str = "governance"
    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8180
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/heath"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/governance/docs"

    CORS_ALLOW_ORIGINS: str = "*"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: str = "false"
    LOG_FILE_NAME: str = "governance.log"
    LOG_FORMAT: str = "string"

    # ICON Nodes
    ICON_NODE_URL = "https://icon.geometry-dev.net/api/v3"
    BACKUP_ICON_NODE_URL = "http://34.218.244.40:9000/api/v3"

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"

    KAFKA_GROUP_ID: str = "governance-service"

    # Topics
    CONSUMER_GROUP_HEAD: str = "governance-head"
    CONSUMER_GROUP_TAIL: str = "governance-tail"
    SCHEMA_NAME_TOPICS: str = "governance-ws:block"

    CONSUMER_TOPIC_BLOCKS: str = "governance"
    CONSUMER_TOPIC_TRANSACTIONS: str = "transactions"
    CONSUMER_TOPIC_LOGS: str = "logs"

    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    # Redis
    # REDIS_HOST: str = "redis"
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = ""
    # REDIS_CHANNEL: str = "governance"
    # REDIS_SENTINEL_CLIENT_MODE: bool = False
    # REDIS_SENTINEL_CLIENT_MASTER_NAME: str = "master"

    _governance_address: str = "cx0000000000000000000000000000000000000000"

    CRON_SLEEP_SEC: int = 600

    class Config:
        case_sensitive = True
        # env_prefix = "GOVERNANCE_"


settings = Settings()
