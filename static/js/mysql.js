document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/mysql-info')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao obter informações do MySQL');
            }
            return response.json();
        })
        .then(data => {
            const mysqlStatusElement = document.getElementById('mysql-status');
            mysqlStatusElement.innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Erro:', error);
            // Tratar o erro conforme necessário, como exibir uma mensagem de erro no elemento `mysql-status`
            const mysqlStatusElement = document.getElementById('mysql-status');
            mysqlStatusElement.innerText = 'Erro ao carregar as informações do MySQL.';
        });
});
