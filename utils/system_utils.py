import psutil
import platform

# Função para obter informações completas do sistema
def get_system_info():
    disk_usage = psutil.disk_usage('/')
    memory_usage = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    temperatures = psutil.sensors_temperatures()
    network_usage = "1.5 GB"  # Substituir com lógica real para obter o uso de rede
    services_status = "All services running"  # Implementação fictícia para ilustrar o exemplo
    os_version = platform.system() + ' ' + platform.release()
    db_workload = {'queries_per_second': 100}  # Implementação fictícia para ilustrar o exemplo
    backup_status = "Backup successful"  # Implementação fictícia para ilustrar o exemplo
    system_resources = "High"  # Implementação fictícia para ilustrar o exemplo
    network_latency = "Low"  # Implementação fictícia para ilustrar o exemplo
    partitions = psutil.disk_partitions()
    partitions_list = [p.device for p in partitions]
    connected_users = 10  # Implementação fictícia para ilustrar o exemplo
    security_status = "Secure"  # Implementação fictícia para ilustrar o exemplo

    system_info_data = {
        'disk_usage': {
            'used': round(disk_usage.used / (1024 * 1024 * 1024), 2),  # Convertendo bytes para GB
            'total': round(disk_usage.total / (1024 * 1024 * 1024), 2),
            'percent': disk_usage.percent
        },
        'memory_usage': {
            'used': round(memory_usage.used / (1024 * 1024 * 1024), 2),  # Convertendo bytes para GB
            'total': round(memory_usage.total / (1024 * 1024 * 1024), 2),
            'percent': memory_usage.percent
        },
        'cpu_percent': {
            'percent': cpu_percent
        },
        'temperature': {
            'temperature': temperatures['coretemp'][0].current if 'coretemp' in temperatures else 'N/A'
        },
        'network_usage': {
            'usage': network_usage
        },
        'services_status': {
            'status': services_status
        },
        'os_version': {
            'version': os_version
        },
        'db_workload': db_workload,
        'backup_status': {
            'status': backup_status
        },
        'system_resources': {
            'resources': system_resources
        },
        'network_latency': {
            'latency': network_latency
        },
        'disk_partitions': {
            'partitions': partitions_list
        },
        'connected_users': {
            'users': connected_users
        },
        'security_status': {
            'status': security_status
        }
    }

    return system_info_data
