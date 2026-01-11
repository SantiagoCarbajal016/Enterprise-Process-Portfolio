import os
import time
import platform

import psutil
from dotenv import load_dotenv

from thresholds import get_cpu_status, get_ram_status, get_disk_status
from reporters.csv_reporter import ensure_csv_exists, append_row
from reporters.email_reporter import send_email
from utils.formatters import build_summary

load_dotenv()


def default_disk_path() -> str:
    # Windows commonly needs C:\ ; Linux/mac use /
    return "C:\\" if platform.system().lower().startswith("win") else "/"


def network_status_bytes_sent(bytes_sent_mb: float) -> str:
    if bytes_sent_mb < 100:
        return "Idle/Light"
    elif bytes_sent_mb < 500:
        return "Light Uploads"
    elif bytes_sent_mb < 1000:
        return "Moderate"
    elif bytes_sent_mb < 5000:
        return "High Usage"
    return "Heavy/Unusual"


def network_status_bytes_recv(bytes_recv_mb: float) -> str:
    if bytes_recv_mb < 100:
        return "Idle/Light"
    elif bytes_recv_mb < 500:
        return "Light Downloads"
    elif bytes_recv_mb < 2000:
        return "Moderate"
    elif bytes_recv_mb < 5000:
        return "High Usage"
    return "Heavy/Unusual"


def packet_status(count: int) -> str:
    if count < 10000:
        return "Very Light"
    elif count < 50000:
        return "Moderate"
    elif count < 200000:
        return "High"
    return "Alert"


def collect_metrics() -> dict:
    timestamp = time.ctime()

    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_status = get_cpu_status(cpu_usage)

    # RAM
    memory = psutil.virtual_memory()
    ram_percent = memory.percent
    ram_status = get_ram_status(ram_percent)

    # Disk
    disk_path = os.getenv("HEALTHIT_DISK_PATH", default_disk_path())
    disk = psutil.disk_usage(disk_path)
    disk_percent = disk.percent
    disk_status = get_disk_status(disk_percent)

    # Network
    net = psutil.net_io_counters()
    bytes_sent_mb = net.bytes_sent / (1024 ** 2)
    bytes_recv_mb = net.bytes_recv / (1024 ** 2)

    upload_status = network_status_bytes_sent(bytes_sent_mb)
    download_status = network_status_bytes_recv(bytes_recv_mb)

    # Packets
    packets_sent = net.packets_sent
    packets_recv = net.packets_recv

    packet_out_status = packet_status(packets_sent)
    packet_in_status = packet_status(packets_recv)

    # Errors
    err_in = net.errin
    err_out = net.errout

    return {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "cpu_status": cpu_status,
        "ram_percent": ram_percent,
        "ram_status": ram_status,
        "disk_percent": disk_percent,
        "disk_status": disk_status,
        "bytes_sent_mb": bytes_sent_mb,
        "upload_status": upload_status,
        "bytes_recv_mb": bytes_recv_mb,
        "download_status": download_status,
        "packets_sent": packets_sent,
        "packet_out_status": packet_out_status,
        "packets_recv": packets_recv,
        "packet_in_status": packet_in_status,
        "err_in": err_in,
        "err_out": err_out,
    }


def main() -> None:
    log_file = os.getenv("HEALTHIT_LOG_FILE", "logs/healthit_systemlog.csv")

    ensure_csv_exists(log_file)

    row = collect_metrics()
    append_row(log_file, row)

    summary = build_summary(row)
    print(summary)

    send_flag = os.getenv("HEALTHIT_SEND_EMAIL", "false").strip().lower() == "true"
    if send_flag:
        send_email("Daily HealthIT System Report", summary)
        print("Email sent (HEALTHIT_SEND_EMAIL=true).")
    else:
        print("Email not sent (HEALTHIT_SEND_EMAIL=false).")


if __name__ == "__main__":
    main()
