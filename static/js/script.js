// /static/script.js

document.addEventListener("DOMContentLoaded", function() {
    // Funções para carregar dados dinamicamente
    loadOverview();
    loadMySQLInfo();
    loadSystemInfo();
    loadBackupInfo();
});

function loadOverview() {
    fetch('/system-info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('overview').innerHTML = `
                <h2>Informações do Sistema</h2>
                <p>Uso do Disco: ${data.disk_usage.percent}%</p>
                <p>Memória Usada: ${data.memory_info.percent}%</p>
            `;
        });
}

function loadMySQLInfo() {
    // Carregar informações do MySQL
}

function loadSystemInfo() {
    // Carregar informações do sistema
}

function loadBackupInfo() {
    // Carregar informações de backup
}
