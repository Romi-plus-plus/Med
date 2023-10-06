from pprint import pprint
from pydantic import BaseSettings


class Settings(BaseSettings):
    NEO_PROFILE: str = "http://localhost:7474/"
    NEO_USER: str = "neo4j"
    NEO_PASSWORD: str = "2132_med"
    NEO_DB_NAME: str = "neo4j"

    MODEL_PATH: str = "./ai/data/joint-bert"
    TOKENIZER_PATH: str = "./ai/data/tokenizer"
    INTENT_LABEL_PATH: str = "./ai/data/labels/intent_labels.txt"
    SLOT_LABEL_PATH: str = "./ai/data/labels/slot_labels.txt"

settings = Settings()
pprint(settings)
