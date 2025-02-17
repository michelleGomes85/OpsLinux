document.addEventListener('DOMContentLoaded', function() {

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

                displayResponse(data)
            } catch (error) {
                console.error('Erro:', error);
            }
        };
    }
});

const isSpeechRecognitionSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

if (!isSpeechRecognitionSupported) {
    alert('Seu navegador não suporte reconhecimento de voz. Use Chrome ou outro navegador moderno');
} else {

    // Criando uma instância do objeto de reconhecimento de voz
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'pt-BR'; 
    recognition.interimResults = false;

    const textarea = document.getElementById('question');
    const microphone = document.getElementById('microphone');
    const microphoneContainer = document.getElementById('microphone-container');

    // Variavel que ver o microfone está ativo
    let isListening = false;

    // Função começar a escutar
    const startListening = () => {
        recognition.start(); 
        textarea.placeholder = "Escutando ...";
        textarea.disabled = true; 
        isListening = true;

        const pulseEffect = document.createElement('div');
        pulseEffect.classList.add('pulsating-effect');
        microphoneContainer.appendChild(pulseEffect);
    };

    // Função para de escutar
    const stopListening = () => {
        recognition.stop(); 
        textarea.placeholder = "Faça uma pergunta sobre o sistema ...";
        textarea.disabled = false; 
        isListening = false;

        const pulseEffect = microphoneContainer.querySelector('.pulsating-effect');
        if (pulseEffect)
            pulseEffect.remove();
    };

    if (microphone) {
        microphone.addEventListener('click', () => {
            if (isListening)
                stopListening();
            else
                startListening();
        });
    
        // Transcrever o resultado no textArea
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            textarea.value = transcript;
            stopListening(); 
        };
    
        // Se ocorre um erro ao escutar
        recognition.onerror = (event) => {
            textarea.placeholder = "Erro ao escutar tente novamente";
            stopListening(); 
        };
    
        // Quando o reconhecimento de voz terminar
        recognition.onend = () => {
            stopListening();
        };
    }
}