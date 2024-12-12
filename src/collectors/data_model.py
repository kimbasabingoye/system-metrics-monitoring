from pydantic import BaseModel
from typing import List


class CoreMetrics(BaseModel):
    core_id: int
    temperature: float  # CPU temperature info per core
    #usage: float  # system-wide CPU utilization as a percentage per core.


class CpuMetrics(BaseModel):
    # List of CPU usage percentages (per-core or aggregate)
    cpus_usage: List[CoreMetrics]
    active_process_count: int  # Number of active processes


class DiskMetrics(BaseModel):
    read_count: int  # Number of read operations
    write_count: int  # Number of write operations
    read_bytes: int  # Total bytes read (in bytes)
    write_bytes: int  # Total bytes written (in bytes)
    disk_total: int  # Total disk space (in bytes)
    disk_used: int  # Used disk space (in bytes)
    inode_total: int  # Total inodes available
    inode_used: int  # Inodes used


class NetworkMetrics(BaseModel):
    network_errors_in: int  # Number of incoming network errors
    network_errors_out: int  # Number of outgoing network errors
    packet_drops_in: int  # Number of inbound packet drops
    packet_drops_out: int  # Number of outbound packet drops
    network_in: int  # Incoming network traffic (bytes)
    network_out: int  # Outgoing network traffic (bytes)


class MemoryMetrics(BaseModel):
    virtual_total: int  # Total virtual memory (in bytes)
    virtual_used: int  # Used virtual memory (in bytes)
    swap_total: int  # Total swap space (in bytes)
    swap_used: int  # Used swap space (in bytes)


class SystemMetrics(BaseModel):
    device_id: str
    timestamp: str  # Timestamp of when the metrics were collected
    cpu: CpuMetrics  # CPU-related metrics
    disk: DiskMetrics  # Disk-related metrics
    # network: NetworkMetrics  # Network-related metrics
    memory: MemoryMetrics  # Memory-related metrics
