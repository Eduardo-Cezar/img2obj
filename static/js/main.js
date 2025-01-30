document.addEventListener('DOMContentLoaded', function() {
    // Função para criar nova nota
    const criarNota = async () => {
        const titulo = document.getElementById('titulo').value;
        const conteudo = document.getElementById('conteudo').value;

        const response = await fetch('/api/notas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ titulo, conteudo })
        });

        if (response.ok) {
            window.location.reload();
        }
    };

    // Adicionar eventos aos botões
    const btnCriarNota = document.getElementById('btnCriarNota');
    if (btnCriarNota) {
        btnCriarNota.addEventListener('click', criarNota);
    }
}); 