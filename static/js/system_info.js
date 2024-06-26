document.addEventListener('DOMContentLoaded', function() {
    // Definindo o limite crítico de uso de memória em porcentagem
    const criticalMemoryThreshold = 80; // Exemplo: 80%

    // Selecionando o elemento do card de memória
    const memoryCard = document.querySelector('#memory-usage').closest('.card');

    // Função para atualizar a cor do card com base no uso de memória
    function updateMemoryCardColor(memoryUsagePercent) {
        if (memoryUsagePercent >= criticalMemoryThreshold) {
            memoryCard.classList.remove('bg-success', 'bg-warning', 'bg-info', 'bg-primary');
            memoryCard.classList.add('bg-danger');
        } else if (memoryUsagePercent >= 60) {
            memoryCard.classList.remove('bg-danger', 'bg-warning', 'bg-info', 'bg-primary');
            memoryCard.classList.add('bg-success');
        } else if (memoryUsagePercent >= 40) {
            memoryCard.classList.remove('bg-danger', 'bg-success', 'bg-info', 'bg-primary');
            memoryCard.classList.add('bg-warning');
        } else if (memoryUsagePercent >= 20) {
            memoryCard.classList.remove('bg-danger', 'bg-success', 'bg-warning', 'bg-primary');
            memoryCard.classList.add('bg-info');
        } else {
            memoryCard.classList.remove('bg-danger', 'bg-success', 'bg-warning', 'bg-info');
            memoryCard.classList.add('bg-primary');
        }
    }

    // Função simulada para obter o uso de memória (substitua pela lógica real)
    function getMemoryUsage() {
        return Math.floor(Math.random() * 100); // Simula um valor de uso de memória entre 0 e 100%
    }

    // Simulação de atualização periódica do uso de memória
    setInterval(function() {
        const memoryUsagePercent = getMemoryUsage();
        document.getElementById('memory-usage').textContent = memoryUsagePercent + '%';
        updateMemoryCardColor(memoryUsagePercent);
    }, 5000); // Atualiza a cada 5 segundos (5000 milissegundos)






});
// system_info.js (exemplo de requisição AJAX usando jQuery)
$(document).ready(function() {
    $.ajax({
        url: '/api/mega-info',
        type: 'GET',
        success: function(data) {
            if (!data.error) {
                $('#cloud-usage').text(`Espaço livre: ${data.free_space.toFixed(2)} GB`);
            } else {
                $('#cloud-usage').text('Erro ao carregar informações do Mega.nz');
            }
        },
        error: function() {
            $('#cloud-usage').text('Erro ao conectar-se ao servidor');
        }
    });
});