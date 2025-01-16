document.getElementById('button-submit').onclick = async function (event) {

    const question = document.getElementById('prompt').value;

    if (!question) {
        alert("Por favor, insira uma pergunta.");
        return;
    }

    try {
        const response = await fetch('/generate-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            throw new Error('Erro ao fazer a requisição');
        }

        const data = await response.json();

        console.log(data); 

    } catch (error) {
        console.error('Erro:', error);
    }
};
