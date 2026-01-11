def get_cpu_status(cpu_usage: float) -> str:
    if cpu_usage < 50:
        return "Good Standing"
    elif cpu_usage < 80:
        return "Moderate Load"
    return "High Load"


def get_ram_status(memory_percent: float) -> str:
    if memory_percent < 60:
        return "Good Standing"
    elif memory_percent < 80:
        return "Maintenance Suggested"
    return "Memory Overload"


def get_disk_status(disk_percent: float) -> str:
    if disk_percent < 70:
        return "Good Standing"
    elif disk_percent < 90:
        return "Maintenance Suggested"
    return "Critical Condition"
