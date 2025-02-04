from flask import request, jsonify
from util.utils import get_documentation
from services.ai_service import ask_ai

PROMPT = """  

Analise cuidadosamente a seguinte documentação:  {documentation}  

Com base nessa análise, determine quais endpoints são necessários para responder à seguinte pergunta:  "{question}"  

Se a pergunta fizer sentido com a documentação disponível, forneça a resposta no seguinte formato JSON:  

{{
    "endpoints": ["endpoint1", "endpoint2", ...],
    "error": null
}}

Caso a pergunta **não tenha relação** com a documentação, retorne um JSON com uma explicação bem-humorada e um trocadilho com Linux sobre o motivo da informação não existir. Exemplo:  

{{
    "endpoints": [],
    "error": Informação não encontrada. Parece que essa pergunta fugiu do escopo, assim como processos zumbis fogem do controle no Linux."
}}

Certifique-se de que a resposta esteja bem formatada e estruturada conforme os exemplos acima.  

"""

def generate_response():

    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400 

        documentation = get_documentation()

        response = ask_ai(PROMPT.format(documentation=documentation, question=question))

        response_data = {'response': response}

        return jsonify(response_data)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
