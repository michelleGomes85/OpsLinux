document.addEventListener('DOMContentLoaded', function() {

    var modal = document.querySelectorAll('.modal');

    M.Modal.init(modal, {
        opacity: 0.8,
        inDuration: 300,
        outDuration: 200,
        startingTop: '10%',
        endingTop: '10%',
        onOpenEnd: function() {
            var textarea = document.getElementById('question');
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
            var question = this.getAttribute('data-question');
            document.getElementById('question').value = question;
        });
    });

    let clearQuestion = document.getElementById('clear-question');
    
    if (clearQuestion) {
        clearQuestion.addEventListener('click', function() {
            document.getElementById('question').value = '';
        });
    }

    let sendQuestion = document.getElementById('send-question');

    if (sendQuestion) {
        
        sendQuestion.onclick = async function () {

            const question = document.getElementById('question').value;
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
    
                alert("Pergunta enviada com sucesso: " + question);
    
                M.Modal.getInstance(document.getElementById('modal-question')).close();
        
                console.log(data); 
        
            } catch (error) {
                console.error('Erro:', error);
            }
        };
    }
});

