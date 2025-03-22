// Função para alternar a sidebar (abrir/fechar)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

// Garantir que a sidebar inicie fechada
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.add('collapsed'); // Adiciona a classe 'collapsed' para iniciar fechada
});