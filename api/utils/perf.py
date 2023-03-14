"""The perf module contains functions for getting information about the system's performance, including the CPU, memory, disk, network, and running processes."""
from typing import Any, Dict, List, Union
import psutil


def get_processes() -> List[Dict[str, Any]]:
    """The get_processes function returns a list of dictionaries containing information about the running processes. Each dictionary contains the PID, name, CPU percent, memory percent, status, create time, executable path, command line arguments, username, number of threads, and number of context switches of a process."""
    return [
        {
            "pid": process.pid,
            "name": process.name(),
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "status": process.status(),
            "create_time": process.create_time(),
            "exe": process.exe(),
            "cmdline": process.cmdline(),
            "username": process.username(),
            "num_threads": process.num_threads(),
            "num_ctx_switches": process.num_ctx_switches(),
        }
        for process in psutil.process_iter()
    ]


def get_process(pid: int) -> Dict[str, Any]:
    """The get_process function takes in a PID as an argument and returns a dictionary with more detailed information about that specific process, including its connections, threads, memory usage, memory maps, open files, I/O counters, CPU times, CPU affinity, and niceness."""
    _process = psutil.Process(pid)
    return {
        "pid": _process.pid,
        "name": _process.name(),
        "cpu_percent": _process.cpu_percent(),
        "memory_percent": _process.memory_percent(),
        "status": _process.status(),
        "create_time": _process.create_time(),
        "exe": _process.exe(),
        "cmdline": _process.cmdline(),
        "username": _process.username(),
        "num_threads": _process.num_threads(),
        "num_ctx_switches": _process.num_ctx_switches(),
        "ports": _process.connections(),
        "threads": _process.threads(),
        "memory_info": _process.memory_info(),
        "memory_maps": _process.memory_maps(),
        "open_files": _process.open_files(),
        "io_counters": _process.io_counters(),
        "cpu_times": _process.cpu_times(),
        "cpu_affinity": _process.cpu_affinity(),
        "nice": _process.nice(),
    }


def get_memory() -> Dict[str, Union[int, float]]:
    """The get_memory function returns a dictionary with information about the system's memory usage, including the total, available, used, free memory, and the percentage of memory used."""
    return {
        "total": psutil.virtual_memory().total,
        "available": psutil.virtual_memory().available,
        "percent": psutil.virtual_memory().percent,
        "used": psutil.virtual_memory().used,
        "free": psutil.virtual_memory().free,
    }


def get_disk(path: str = "/") -> Dict[str, Union[int, float]]:
    """The get_disk function returns a dictionary with information about the disk usage of a specified path, including the total, used, and free disk space, and the percentage of disk space used."""
    return {
        "total": psutil.disk_usage(path).total,
        "used": psutil.disk_usage(path).used,
        "free": psutil.disk_usage(path).free,
        "percent": psutil.disk_usage(path).percent,
    }


def get_cpu() -> Dict[str, Union[int, float]]:
    """The get_cpu function returns a dictionary with information about the CPU usage, including the overall CPU percentage, the number of cores, and the current CPU frequency."""
    return {
        "percent": psutil.cpu_percent(),
        "cores": psutil.cpu_count(),
        "freq": psutil.cpu_freq().current,
    }


def get_network() -> List[Dict[str, Any]]:
    """The get_network function returns a list of dictionaries containing information about the network interfaces, including the interface name, IP address, netmask, broadcast address, point-to-point address, and network statistics."""
    return [
        {
            "interface": interface,
            "address": address.address,
            "netmask": address.netmask,
            "broadcast": address.broadcast,
            "ptp": address.ptp,
            "stats": psutil.net_if_stats()[interface],
        }
        for interface, addresses in psutil.net_if_addrs().items()
        for address in addresses
    ]


def get_status() -> Dict[str, Any]:
    """The get_status function returns a dictionary containing information about the system status, including the CPU usage, memory usage, disk usage, network usage, and running processes."""
    return {
        "cpu": get_cpu(),
        "memory": get_memory(),
        "disk": get_disk(),
        "network": get_network(),
        "processes": get_processes(),
    }
