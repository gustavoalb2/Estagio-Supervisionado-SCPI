// JavaScript personalizado para SCPI

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização de tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicialização de popovers do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Função para confirmar exclusões
    window.confirmarExclusao = function(mensagem) {
        return confirm(mensagem || 'Tem certeza que deseja excluir este item?');
    };

    // Função para mostrar alertas temporários
    window.mostrarAlerta = function(tipo, mensagem, tempo = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container:first-of-type');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, tempo);
    };

    // Auto-hide de alertas após 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });
});

// Função para formato de data brasileiro
function formatarData(data) {
    return new Date(data).toLocaleDateString('pt-BR');
}

// Função para formato de data e hora brasileiro
function formatarDataHora(data) {
    return new Date(data).toLocaleString('pt-BR');
}
