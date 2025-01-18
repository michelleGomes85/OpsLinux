document.addEventListener('DOMContentLoaded', function() {

    var modal = document.querySelectorAll('.modal');

    M.Modal.init(modal, {
        opacity: 0.8,
        inDuration: 300,
        outDuration: 200,
        startingTop: '10%',
        endingTop: '10%',
        onOpenEnd: function() {
            var textarea = document.getElementById('pergunta');
            textarea.value = ''; 
            textarea.focus(); 
        }
    });

    var sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    var tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips, {
        position: 'bottom'
    });

    document.querySelectorAll('.icon-link').forEach(function(link) {
        link.addEventListener('click', function() {
            var pergunta = this.getAttribute('data-pergunta');
            document.getElementById('pergunta').value = pergunta;
        });
    });

    document.getElementById('limparPergunta').addEventListener('click', function() {
        document.getElementById('pergunta').value = '';
    });


    document.getElementById('enviarPergunta').onclick = async function (event) {

        const question = document.getElementById('pergunta').value;
        var loadingEffect = document.getElementById('loadingEffect');
    
        if (!question) {
            alert("Por favor, insira uma pergunta.");
            return;
        }
    
        try {
            loadingEffect.style.display = 'block';
            const response = await fetch('/generate-response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
    
            if (!response.ok) {
                throw new Error('Erro ao fazer a requisição');
            }
    
            const data = await response.json();

            loadingEffect.style.display = 'none';

            alert("Pergunta enviada com sucesso: " + pergunta);

            M.Modal.getInstance(document.getElementById('modalPergunta')).close();
    
            console.log(data); 
    
        } catch (error) {
            console.error('Erro:', error);
        }
    };
});