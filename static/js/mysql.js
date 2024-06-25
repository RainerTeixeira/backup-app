// static/js/mysql.js

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/mysql-info')
        .then(response => response.json())
        .then(data => {
            const mysqlStatusElement = document.getElementById('mysql-status');
            mysqlStatusElement.innerText = JSON.stringify(data, null, 2);
        });
});
