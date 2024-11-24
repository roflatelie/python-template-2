import aioprometheus
from pydantic_settings import BaseSettings, SettingsConfigDict


class PodInfo(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POD_", env_file=".env", extra="ignore")
    node: str | None
    image: str | None


class APM(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTIC_APM_", env_file=".env", extra="ignore")
    ENABLED: bool


class LogConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", extra="ignore")
    LEVEL: str = "INFO"
    FORMATTER: str | None = "json"
    apm: APM = APM()
    pod: PodInfo = PodInfo()

    EXTRA: dict = {
        'pod': pod.model_dump(),
    }


class Metrics:
    http_requests_latency = aioprometheus.Histogram(
        "http_requests_latency",
        "http_requests_latency",
        buckets=[10, 25, 50, 100, 300, 500, 1000, 2000, 5000, 10000]
    )

    @staticmethod
    def render() -> tuple[bytes, dict]:
        return aioprometheus.render(
            aioprometheus.REGISTRY,
            [],
        )
