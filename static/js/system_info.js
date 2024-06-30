

    document.addEventListener('DOMContentLoaded', function () {
        // Funções para carregar informações do sistema
        loadDiskUsage();
        loadMemoryInfo();
        loadCPUInfo();
        loadSystemTemperature();
        loadServiceStatus();
        loadOSVersion();
        loadNetworkUsage();
        loadServicesStatus();
        loadDBWorkload();
        loadBackupStatus();
        loadSystemResources();
        loadNetworkLatency();
        loadDiskPartitions();
        loadConnectedUsers();
        loadSecurityStatus();
    });

    function loadDiskUsage() {
        fetch('/api/disk-info')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar uso do disco: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('disk-usage').textContent = `${data.used} GB / ${data.total} GB (${data.percent}%)`;
            })
            .catch(error => {
                document.getElementById('disk-usage').textContent = 'Erro ao carregar uso do disco.';
                console.error(error);
            });
    }

    function loadMemoryInfo() {
        fetch('/api/memory-info')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar informações de memória: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('memory-usage').textContent = `${data.used} GB / ${data.total} GB (${data.percent}%)`;
            })
            .catch(error => {
                document.getElementById('memory-usage').textContent = 'Erro ao carregar informações de memória.';
                console.error(error);
            });
    }

    function loadCPUInfo() {
        fetch('/api/cpu-info')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar informações da CPU: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('cpu-usage').textContent = `${data.percent}%`;
            })
            .catch(error => {
                document.getElementById('cpu-usage').textContent = 'Erro ao carregar informações da CPU.';
                console.error(error);
            });
    }

    function loadSystemTemperature() {
        fetch('/api/temperature-info')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar temperatura do sistema: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('system-temperature').textContent = data.temperature;
            })
            .catch(error => {
                document.getElementById('system-temperature').textContent = 'Erro ao carregar temperatura do sistema.';
                console.error(error);
            });
    }

    function loadServiceStatus() {
        fetch('/api/service-status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar status do serviço: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('service-status').textContent = data.status;
            })
            .catch(error => {
                document.getElementById('service-status').textContent = 'Erro ao carregar status do serviço.';
                console.error(error);
            });
    }

    function loadOSVersion() {
        fetch('/api/os-version')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar versão do sistema operacional: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('os-version').textContent = data.version;
            })
            .catch(error => {
                document.getElementById('os-version').textContent = 'Erro ao carregar versão do sistema operacional.';
                console.error(error);
            });
    }

    function loadNetworkUsage() {
        fetch('/api/network-usage')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar utilização da rede: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('network-usage').textContent = data.usage;
            })
            .catch(error => {
                document.getElementById('network-usage').textContent = 'Erro ao carregar utilização da rede.';
                console.error(error);
            });
    }

    function loadServicesStatus() {
        fetch('/api/services-status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar status dos serviços: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('services-status').textContent = data.status;
            })
            .catch(error => {
                document.getElementById('services-status').textContent = 'Erro ao carregar status dos serviços.';
                console.error(error);
            });
    }

    function loadDBWorkload() {
        fetch('/api/db-workload')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar carga de trabalho do banco de dados: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('db-workload').textContent = data.queries_per_second;
            })
            .catch(error => {
                document.getElementById('db-workload').textContent = 'Erro ao carregar carga de trabalho do banco de dados.';
                console.error(error);
            });
    }

    function loadBackupStatus() {
        fetch('/api/backup-status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar status de backups: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('backup-status').textContent = data.status;
            })
            .catch(error => {
                document.getElementById('backup-status').textContent = 'Erro ao carregar status de backups.';
                console.error(error);
            });
    }

    function loadSystemResources() {
        fetch('/api/system-resources')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar utilização de recursos do sistema: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('system-resources').textContent = data.resources;
            })
            .catch(error => {
                document.getElementById('system-resources').textContent = 'Erro ao carregar utilização de recursos do sistema.';
                console.error(error);
            });
    }

    function loadNetworkLatency() {
        fetch('/api/network-latency')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar latência de rede: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('network-latency').textContent = data.latency;
            })
            .catch(error => {
                document.getElementById('network-latency').textContent = 'Erro ao carregar latência de rede.';
                console.error(error);
            });
    }

    function loadDiskPartitions() {
        fetch('/api/disk-partitions')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar partições de disco: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('disk-partitions').textContent = data.partitions;
            })
            .catch(error => {
                document.getElementById('disk-partitions').textContent = 'Erro ao carregar partições de disco.';
                console.error(error);
            });
    }

    function loadConnectedUsers() {
        fetch('/api/connected-users')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar contagem de usuários conectados: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('connected-users').textContent = data.users;
            })
            .catch(error => {
                document.getElementById('connected-users').textContent = 'Erro ao carregar contagem de usuários conectados.';
                console.error(error);
            });
    }

    function loadSecurityStatus() {
        fetch('/api/security-status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar status de segurança: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('security-status').textContent = data.status;
            })
            .catch(error => {
                document.getElementById('security-status').textContent = 'Erro ao carregar status de segurança.';
                console.error(error);
            });
    }
