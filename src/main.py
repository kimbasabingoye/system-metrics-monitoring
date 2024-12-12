import os

from dotenv import load_dotenv

from collectors.system_metrics_collector import SystemMetricsCollector

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "Value not set")
TOPIC_ID = os.getenv("TOPIC_ID", "Value not set")


collector = SystemMetricsCollector(PROJECT_ID, TOPIC_ID)
collector.start()
