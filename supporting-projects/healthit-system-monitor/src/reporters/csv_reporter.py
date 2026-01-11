import csv
import os
from typing import Dict, Any, List

CSV_HEADERS: List[str] = [
    "Timestamp",
    "CPU %", "CPU Status",
    "RAM %", "RAM Status",
    "Disk %", "Disk Status",
    "Network Sent (MB)", "Upload Status",
    "Network Received (MB)", "Download Status",
    "Packets Sent", "Packet Sent Status",
    "Packets Received", "Packet Received Status",
    "Receiving Errors", "Sending Errors",
]


def ensure_csv_exists(log_file: str) -> None:
    # Ensure logs folder exists (e.g., logs/healthit_systemlog.csv)
    folder = os.path.dirname(log_file)
    if folder:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def append_row(log_file: str, row: Dict[str, Any]) -> None:
    with open(log_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            row["timestamp"],
            row["cpu_usage"], row["cpu_status"],
            row["ram_percent"], row["ram_status"],
            row["disk_percent"], row["disk_status"],
            row["bytes_sent_mb"], row["upload_status"],
            row["bytes_recv_mb"], row["download_status"],
            row["packets_sent"], row["packet_out_status"],
            row["packets_recv"], row["packet_in_status"],
            row["err_in"], row["err_out"],
        ])
