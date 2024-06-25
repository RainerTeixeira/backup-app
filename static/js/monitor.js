// static/js/monitor.js

document.addEventListener('DOMContentLoaded', function() {
    // Atualiza informações do sistema
    fetch('/api/system-info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('disk-usage').innerText = data.disk_usage.percent;
            document.getElementById('memory-usage').innerText = data.memory_info.percent;
            document.getElementById('cpu-usage').innerText = data.cpu_info;
        });

    // Atualiza informações do MySQL
    fetch('/api/mysql-info')
        .then(response => response.json())
        .then(data => {
            const mysqlStatusElement = document.getElementById('mysql-status');
            mysqlStatusElement.innerText = JSON.stringify(data, null, 2);
        });
});
