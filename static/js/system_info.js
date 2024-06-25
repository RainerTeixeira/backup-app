document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/system-info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('disk-usage').innerText = data.disk_usage.percent;
            document.getElementById('memory-usage').innerText = data.memory_info.percent;
            document.getElementById('cpu-usage').innerText = data.cpu_info;
            document.getElementById('system-temperature').innerText = data.system_temperature + '°C';
            document.getElementById('service-status').innerText = 'Carregando...'; // Adicione o status do servidor
            document.getElementById('os-version').innerText = 'Carregando...'; // Adicione a versão do sistema operacional
            document.getElementById('network-usage').innerText = data.network_usage + ' Mbps'; // Adicione a utilização da rede
            document.getElementById('services-status').innerText = 'Carregando...'; // Adicione o status dos serviços
            document.getElementById('db-workload').innerText = data.db_workload + ' consultas por segundo'; // Adicione a carga de trabalho do banco de dados
            document.getElementById('backup-status').innerText = 'Carregando...'; // Adicione o status dos backups
            document.getElementById('system-resources').innerText = 'Carregando...'; // Adicione a utilização de recursos do sistema
            document.getElementById('network-latency').innerText = data.network_latency + ' ms'; // Adicione a latência de rede
            document.getElementById('disk-partitions').innerText = 'Carregando...'; // Adicione o espaço em disco por partição
            document.getElementById('connected-users').innerText = 'Carregando...'; // Adicione a contagem de usuários conectados
        })
        .catch(error => {
            console.error('Erro ao buscar informações do sistema:', error);
            // Tratar erros conforme necessário
        });
});
