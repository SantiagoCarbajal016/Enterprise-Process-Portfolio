from typing import Dict, Any


def build_summary(row: Dict[str, Any]) -> str:
    return f"""=== Daily Health Report ===
Timestamp: {row["timestamp"]}

CPU Usage: {row["cpu_usage"]}% - {row["cpu_status"]}
RAM Usage: {row["ram_percent"]}% - {row["ram_status"]}
Disk Usage: {row["disk_percent"]}% - {row["disk_status"]}

Network Sent: {row["bytes_sent_mb"]:.2f} MB - {row["upload_status"]}
Network Received: {row["bytes_recv_mb"]:.2f} MB - {row["download_status"]}
Packets Sent: {row["packets_sent"]} - {row["packet_out_status"]}
Packets Received: {row["packets_recv"]} - {row["packet_in_status"]}

Errors In: {row["err_in"]}
Errors Out: {row["err_out"]}
"""
