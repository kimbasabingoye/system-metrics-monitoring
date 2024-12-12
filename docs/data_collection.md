# Data Collection

The following sections document the metrics being collected, their meaning, importance, and the command used to retrieve them. Additionally, the format of the data sent to Pub/Sub is specified.

## Metrics Collected

#### **System Metrics**

1. **CPU Usage (%)**
   - **Meaning**: The percentage of the system’s CPU capacity currently being used.
   - **Why it's important**: High CPU usage indicates that the system is under heavy load, which may affect overall performance and responsiveness. Monitoring CPU usage helps detect bottlenecks.
   - **Command**: `psutil.cpu_percent(interval=1)`

2. **Memory Usage (%)**
   - **Meaning**: The percentage of system memory (RAM) currently in use.
   - **Why it's important**: High memory usage can indicate that the system is consuming more memory than it can handle, leading to potential swapping or performance degradation.
   - **Command**: `psutil.virtual_memory().percent`

3. **Disk Usage (%)**
   - **Meaning**: The percentage of total disk space that is currently in use on the system.
   - **Why it's important**: High disk usage can indicate that the disk is close to full, which can slow down performance and prevent the system from saving data.
   - **Command**: `psutil.disk_usage('/').percent`

4. **Network Traffic (Inbound/Outbound)**
   - **Meaning**: The rate of incoming and outgoing network traffic in bytes per second.
   - **Why it's important**: Monitoring network traffic helps ensure the system's network resources are not saturated. High network activity could indicate issues or the need for optimization.
   - **Command**: `psutil.net_io_counters().bytes_recv` for inbound, `psutil.net_io_counters().bytes_sent` for outbound

5. **System Uptime**
   - **Meaning**: The amount of time the system has been running since the last reboot.
   - **Why it's important**: Uptime helps track system stability. Frequent reboots could indicate system instability or failure.
   - **Command**: `psutil.boot_time()`

6. **Active Process Count**
   - **Meaning**: The number of active processes running on the system.
   - **Why it's important**: A large number of processes may cause resource contention. Monitoring the number of active processes helps identify if the system is overloaded.
   - **Command**: `len(psutil.pids())`

7. **Load Average (1, 5, 15 min)**
   - **Meaning**: The system load, representing the average number of processes in the system’s run queue over 1, 5, and 15 minutes.
   - **Why it's important**: High load averages relative to the number of CPU cores indicate a system under stress, which may require performance tuning.
   - **Command**: `psutil.getloadavg()`

---

#### **Disk Metrics**

1. **Disk Read/Write Speed (MB/s)**
   - **Meaning**: The rate at which data is being read from or written to the disk.
   - **Why it's important**: High disk read/write speeds may indicate I/O-heavy processes, which can impact overall system performance. Monitoring this helps detect potential disk bottlenecks.
   - **Command**: `psutil.disk_io_counters().read_bytes` and `psutil.disk_io_counters().write_bytes`

2. **Disk I/O Operations Count**
   - **Meaning**: The number of disk read/write operations performed by the system.
   - **Why it's important**: High I/O operations can indicate disk-intensive processes or services that may need optimization or scaling.
   - **Command**: `psutil.disk_io_counters().read_count` and `psutil.disk_io_counters().write_count`

3. **Inode Usage (%)**
   - **Meaning**: The percentage of file system inodes in use.
   - **Why it's important**: Inodes are data structures that store information about files. If inodes run out, the system cannot create new files, even if there is free disk space.
   - **Command**: `psutil.disk_inodes()`



---

#### **Network Metrics**

1. **Network Errors (Inbound/Outbound)**
   - **Meaning**: The number of network errors encountered while receiving or transmitting data.
   - **Why it's important**: Network errors can cause delays and packet loss, affecting system performance and user experience.
   - **Command**: `psutil.net_if_stats()`

2. **Active Network Connections Count**
   - **Meaning**: The number of active network connections to/from the system.
   - **Why it's important**: A large number of active connections can indicate heavy network usage, or a possible security concern if unexpected.
   - **Command**: `psutil.net_connections(kind='inet')`

3. **Packet Drops (Inbound/Outbound)**
   - **Meaning**: The number of network packets that were dropped during transmission.
   - **Why it's important**: Packet drops can indicate network congestion, which could affect the performance of network services or applications.
   - **Command**: `psutil.net_if_stats()`

---

#### **Temperature Metrics (Optional)**

1. **CPU Temperature (°C)**
   - **Meaning**: The temperature of the CPU, which can provide insight into the system’s thermal health.
   - **Why it's important**: High CPU temperatures can lead to thermal throttling, causing performance degradation or hardware damage.
   - **Command**: `psutil.sensors_temperatures()['coretemp']`. This command depends on your system.

---

### **Data Format for Publishing to Pub/Sub**

The collected metrics are formatted into **JSON** and published to **Google Cloud Pub/Sub**. Each message represents the system's metrics at a specific timestamp.

#### Published Data format
```json
{
  "timestamp": "2024-12-10T14:32:45Z",
  "cpu_usage": 75.3,
  "memory_usage": 82.1,
  "disk_usage": 65.5,
  "network_in": 1045,
  "network_out": 512,
  "system_uptime": 102345,
  "active_process_count": 120,
  "load_average": [1.25, 1.30, 1.40],
  "disk_read_speed": 50.3,
  "disk_write_speed": 25.7,
  "disk_queue_length": 3,
  "inode_usage": 90.2,
  "network_errors_in": 0,
  "network_errors_out": 2,
  "packet_drops_in": 0,
  "packet_drops_out": 1,
  "cpu_temperature": {
    "id": 1,
    "temp": 50
  }
}
```

#### **Data Fields**:
- **timestamp**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`)
- **cpu_usage**: Percentage of CPU in use
- **memory_usage**: Percentage of memory in use
- **disk_usage**: Percentage of disk space in use
- **network_in**: Network inbound traffic (bytes)
- **network_out**: Network outbound traffic (bytes)
- **system_uptime**: System uptime in seconds
- **active_process_count**: Number of active processes
- **load_average**: Load average for 1, 5, and 15 minutes
- **disk_read_speed**: Disk read speed in MB/s
- **disk_write_speed**: Disk write speed in MB/s
- **disk_queue_length**: Disk queue length
- **inode_usage**: Percentage of inodes used
- **network_errors_in**: Inbound network errors
- **network_errors_out**: Outbound network errors
- **packet_drops_in**: Inbound packet drops
- **packet_drops_out**: Outbound packet drops
- **cpu_temperature**: CPU temperature in Celsius for each core identified by id

---
