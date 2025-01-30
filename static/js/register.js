document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        const username = document.getElementById('username').value;
        const senha = document.getElementById('senha').value;
        const confirmarSenha = document.getElementById('confirmar_senha').value;
        let isValid = true;

        // Limpa mensagens de erro anteriores
        document.querySelectorAll('.error-message').forEach(el => el.remove());

        // Validação do username
        if (username.length < 3) {
            showError('username', 'O nome de usuário deve ter pelo menos 3 caracteres');
            isValid = false;
        }

        // Validação da senha
        if (senha.length < 6) {
            showError('senha', 'A senha deve ter pelo menos 6 caracteres');
            isValid = false;
        }

        // Validação da confirmação de senha
        if (senha !== confirmarSenha) {
            showError('confirmar_senha', 'As senhas não coincidem');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });

    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
}); 