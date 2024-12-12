from collectors.utils import PubSubHelper
from collectors.data_model import (
    CpuMetrics,
    CoreMetrics,
    DiskMetrics,
    MemoryMetrics,
    SystemMetrics
)
import datetime
import time
import subprocess
import signal
import os

import psutil

from dotenv import load_dotenv

load_dotenv('.env')  # for local dev


SERVICE_ACCOUNT_FILE_PATH = os.getenv(
    "SERVICE_ACCOUNT_FILE_PATH", "Variable Not Set")


class SystemMetricsCollector:
    def __init__(self, project_id: str, topic_name: str):
        """
        Initialize the system metrics collector with Pub/Sub publisher

        :param project_id: GCP Project ID
        :param topic_name: Pub/Sub topic for metric publishing
        """
        self.pub_sub_helper = PubSubHelper(project_id,
                                           SERVICE_ACCOUNT_FILE_PATH)
        self.topic_name = topic_name
        self.is_running = False

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._graceful_shutdown)
        signal.signal(signal.SIGINT, self._graceful_shutdown)

    def _graceful_shutdown(self, signal, frame):
        """
        Handle graceful shutdown when receiving SIGTERM or SIGINT
        """
        print("Initiating graceful shutdown...")
        self.is_running = False

    def collect_system_metrics(self):
        """
        Collect comprehensive system metrics

        :return: SystemMetrics of system performance metrics
        """
        return SystemMetrics(
            device_id=self._get_container_id(),
            timestamp=datetime.datetime.utcnow().isoformat() + "Z",
            cpu=self._get_cpus_metrics(),
            disk=self._get_disk_metrics(),
            memory=self._get_memory_metrics()
        )

    def _get_container_id(self):
        with open('/proc/self/cgroup', 'r', encoding='utf-8') as f:
            for line in f:
                if 'cpu' in line:
                    return line.strip().split('/')[-1][:]
        return "testdevice"  # for local testing

    def _get_cpus_metrics(self) -> CpuMetrics:
        # Fetch the coretemp data
        core_temp_data = psutil.sensors_temperatures().get('coretemp', [])

        # Fetch core usage data
        # cores_usage = psutil.cpu_percent(interval=None, percpu=True)
        cpu_data = []
        for temp in core_temp_data:
            if temp.label.startswith('Core'):
                core_id = int(temp.label.split(' ')[1])
                temperature = temp.current
                cpu_data.append(CoreMetrics(
                    core_id=core_id,
                    temperature=temperature,
                    # usage=cores_usage[core_id - 1]
                ))

        return CpuMetrics(
            cpus_usage=cpu_data,
            active_process_count=len(psutil.pids())
        )

    def _get_disk_metrics(self) -> DiskMetrics:
        inode_usage = self._get_inode_usage()
        disk_metrics = {
            "read_count": psutil.disk_io_counters().read_count,
            "write_count": psutil.disk_io_counters().write_count,
            "read_bytes": psutil.disk_io_counters().read_bytes,
            "write_bytes": psutil.disk_io_counters().write_bytes,
            "disk_total": psutil.disk_usage('/').total,
            "disk_used": psutil.disk_usage('/').used,
            "inode_total": inode_usage[0],
            "inode_used": inode_usage[1]
        }
        return DiskMetrics(**disk_metrics)

    def _get_inode_usage(self):
        """Return inode usage"""
        # Run the df -i command to get inode usage
        df_output = subprocess.check_output(['df', '-i']).decode('utf-8')
        lines = df_output.splitlines()

        # Find the relevant line (assuming you're interested in the root file system '/')
        for line in lines:
            if line.split(' ')[-1] == '/':  # Root filesystem
                parts = line.split()
                used_inodes = int(parts[2])  # Used inodes
                total_inodes = int(parts[1])  # Total inodes
                return (total_inodes, used_inodes)
        return (0, 0)

    def _get_memory_metrics(self) -> MemoryMetrics:
        memory = {
            "virtual_total": psutil.virtual_memory().total,
            "virtual_used": psutil.virtual_memory().used,
            "swap_total": psutil.swap_memory().total,
            "swap_used": psutil.swap_memory().used
        }
        return MemoryMetrics(**memory)

    def _log_message(self, msg, file_path):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(msg)

    def start(self, interval: int = 60):
        """
        Continuously collect and publish metrics with graceful stop capability

        :param interval: Seconds between metric collections
        """
        self.is_running = True
        try:
            while self.is_running:
                try:
                    metrics = self.collect_system_metrics()
                    message = metrics.model_dump_json()
                    self._log_message(message, 'collected_metrics_logs.txt')
                    self.pub_sub_helper.publish_message(self.topic_name,
                                                        message)
                except Exception as e:
                    print(f"Error in metrics collection: {e}")
                for _ in range(int(interval)):
                    if not self.is_running:
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted by user.")
        finally:
            print("Metrics collection stopped.")
