document.getElementById('search-pecas').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase(); // Converte o termo de busca para minúsculas
    const pecas = document.querySelectorAll('.peca-card'); // Seleciona todos os cards de peças

    pecas.forEach(peca => {
        const descricao = peca.getAttribute('data-descricao');
        const posicao = peca.getAttribute('data-posicao');
        const partNumber = peca.getAttribute('data-partnumber');

        // Verifica se o termo de busca está na descrição, posição ou part number
        if (descricao.includes(searchTerm) || posicao.includes(searchTerm) || partNumber.includes(searchTerm)) {
            peca.classList.remove('hide'); // Mostra a peça
        } else {
            peca.classList.add('hide'); // Oculta a peça
        }
    });
});