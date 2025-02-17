function displayResponse(data) {
    const responseContainer = document.getElementById('response-container');
    responseContainer.innerHTML = '';

    console.log(data); // Verifique o console para ver a estrutura completa do JSON

    // Parsear o data.response se for uma string JSON
    let responseData;
    try {
        responseData = JSON.parse(data.response); // Converte a string JSON em um objeto
    } catch (error) {
        console.error('Erro ao parsear data.response:', error);
        return;
    }

    // Exibir a pergunta
    const questionElement = document.createElement('div');
    questionElement.innerHTML = `<strong>❓ Pergunta:</strong> ${responseData.question}`;
    responseContainer.appendChild(questionElement);

    // Exibir a resposta textual
    const responseElement = document.createElement('div');
    responseElement.innerHTML = `<strong>💬 Resposta:</strong> ${responseData.response}`;
    responseContainer.appendChild(responseElement);

    // Exibir o diagrama Mermaid
    if (responseData.visual) {
        const mermaidElement = document.createElement('div');
        mermaidElement.classList.add('mermaid');
        mermaidElement.textContent = responseData.visual.replace(/```mermaid/g, '').replace(/```/g, '').trim(); // Remove os marcadores ```mermaid
        responseContainer.appendChild(mermaidElement);

        mermaid.init(undefined, mermaidElement);
    }
}