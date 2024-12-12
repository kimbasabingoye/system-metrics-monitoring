import os
import yaml

from dotenv import load_dotenv

load_dotenv()

def load_config(env='dev'):
    config_path = f'config/{env}.yaml'
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


class Config:
    GCP_PROJECT = os.getenv('GCP_PROJECT')
    PUBSUB_TOPIC = os.getenv('PUBSUB_TOPIC', 'system-metrics')
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', '60'))