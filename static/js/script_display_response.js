function displayResponse(data) {
    mermaid.initialize({
        'theme': 'base',
        'themeVariables': {
        'primaryColor': 'rgb(17, 46, 81)',
        'primaryTextColor': '#fff',
        'primaryBorderColor': '#fff',
        'lineColor': '#fff',
        'secondaryColor': 'rgb(46, 113, 191)',
        'tertiaryColor': '#fff',
        'tertiaryColor': 'rgb(10, 55, 107)'
        }
    });
    

    const responseContainer = document.getElementById('response-container');
    const card = document.querySelector('.card');
    const questionElement = document.querySelector(".question-card");
    const responseElement = document.querySelector(".answer");
    const mermaidContainer = document.getElementById('mermaid-container');

    // Limpar conteúdo antes de exibir novos dados
    if (questionElement) questionElement.innerHTML = '';
    if (responseElement) responseElement.innerHTML = '';
    if (mermaidContainer) mermaidContainer.innerHTML = '';

    if (responseContainer) {
        responseContainer.style.display = 'flex';
        setTimeout(() => {
            responseContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    let responseData;

    if (data.error) {
        const questionElement = document.querySelector(".question-card");
        if (questionElement)
            questionElement.innerHTML = `${data.question}`;

        const responseElement = document.querySelector(".answer");
        if (responseElement)
            responseElement.innerHTML = `<p>${data.error}</p>`;
        return;
    }

    try {
        responseData = JSON.parse(data.response);
    } catch (error) {
        return;
    }

    if (questionElement) questionElement.innerHTML = `${responseData.question}`;

    if (responseElement) responseElement.innerHTML = `${responseData.response}`;

    if (Array.isArray(responseData.visual) && responseData.visual.length > 0) {
        const mermaidContainer = document.getElementById('mermaid-container');
        if (mermaidContainer) {
            mermaidContainer.innerHTML = '';

            responseData.visual.forEach((diagram) => {
                const sanitizedDiagram = diagram.replace(/```mermaid/g, '').replace(/```/g, '').trim();

                try {

                    // Verifica se o diagrama é válido
                    if (mermaid.parse(sanitizedDiagram)) {
                        const diagramElement = document.createElement('div');
                        diagramElement.textContent = sanitizedDiagram;
                        mermaidContainer.appendChild(diagramElement);

                        // Captura erros durante a renderização
                        mermaid.init(undefined, diagramElement).catch((err) => {
                            mermaidContainer.innerHTML = '';
                            const errorMessage = document.createElement('div');
                            errorMessage.textContent = "Me desculpe não conseguimos reenderizar uma resposta visual para você";
                            mermaidContainer.appendChild(errorMessage);
                        });

                    } else {
                        mermaidContainer.innerHTML = '';
                        const errorMessage = document.createElement('div');
                        errorMessage.textContent = "Me desculpe não conseguimos reenderizar uma resposta visual para você";
                        mermaidContainer.appendChild(errorMessage);
                    }
                } catch (err) {
                    mermaidContainer.innerHTML = '';
                    const errorMessage = document.createElement('div');
                    errorMessage.textContent = "Me desculpe não conseguimos reenderizar uma resposta visual para você"
                    mermaidContainer.appendChild(errorMessage);
                }
            });
        }
    }
}