from flask import request, jsonify
from utils.utils import get_documentation
from services.ai_service import ask_ai
import json
import requests

from config.settings import get_api_url

def generate_response():

    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400 

        # DOCBOT: Analisa a documentação e encontra os endpoints necessários
        documentation = get_documentation()
        prompt_docbot = generate_docbot_prompt(documentation, question)
        response_docbot = ask_ai(prompt_docbot)

        # Converte a resposta da IA para JSON
        try:
            response_data = json.loads(response_docbot)
        except json.JSONDecodeError:
            return jsonify({'error': 'Falha ao interpretar resposta da IA'}), 500

        # Se não há endpoints relevantes, retorna erro bem-humorado
        if response_data.get("error"):
            return jsonify(response_data)

        # Busca dados da API
        fetched_data = {}
        for endpoint in response_data.get('endpoints', []):
            fetched_data[endpoint] = fetch_system_info(endpoint)

        # SYSBOT: Responde ao usuário de forma natural
        prompt_sysbot = generate_sysbot_prompt(fetched_data, question)
        response_sysbot = ask_ai(prompt_sysbot)

        return jsonify({'response': response_sysbot})

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    

def fetch_system_info(endpoint):

    """ Faz uma requisição à API para obter informações do sistema. """

    try:
        response = requests.get(get_api_url(endpoint), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None


def generate_docbot_prompt(documentation, question):

    """ Gera o prompt para o DOCBOT, que seleciona os endpoints. """

    return f'''

    Você é o **DocBot**, um assistente especializado em interpretar documentações de API. 
    Aqui está a documentação disponível: {documentation}

    O usuário fez a seguinte pergunta: "{question}".  
    Seu trabalho é identificar quais **endpoints da API** são necessários para responder à pergunta.

    **Se a pergunta estiver relacionada à documentação**, responda com um JSON no seguinte formato:
    {{
        "question": Pergunta original feita pelo usuário
        "endpoints": ["endpoint1", "endpoint2", ...],
        "error": null
    }}

    **Se a pergunta NÃO tiver relação com a documentação**, responda com um JSON contendo um trocadilho engraçado sobre Linux:
    {{
        "question": Pergunta original feita pelo usuário,
        "endpoints": [],
        "error": "Resposta bem humorada do porque a pergunta não pode ser respondida, seja engraçado usando tracadilhos com o Linux"
    }}

    Certifique-se de que a resposta esteja 100% no formato JSON válido.

    '''

def generate_sysbot_prompt(fetched_data, question):
    """Gera o prompt para o SYSBOT, formatando respostas com tabelas ou diagramas."""

    return f'''

    Você é o **SysBot**, um assistente que traduz informações técnicas para linguagem simples e acessível. 
    Está conversando com um **usuário leigo**, então evite jargões e explique conceitos de maneira fácil de entender. Não fale para o 
    usuário de onde veio a informação, trate como: O sistema possui ..., seja o mais entendível possível, e não se estenda muito. 
    Responda somente o que o usuário deseja.

    **Informações disponíveis:**

    O sistema consultou um serviço e obteve os seguintes dados:  

    <pre>{json.dumps(fetched_data, indent=4)}</pre>

    A pergunta feita pelo usuário foi: {question}

    **Instruções para a resposta:**

    1 - **Use apenas os dados fornecidos no JSON acima.**  
    2 - **Não invente dados ausentes.** Se algo estiver faltando, avise claramente ao usuário.  
    3 - **Use diagramas para facilitar o entendimento,** usando o código da biblioteca **Mermaid.js** do JavaScript. 
          Passe apenas o código puro dos diagramas, sem a necessidade de comentários adicionais. Exemplo: para gerar um gráfico de pizza, 
          use o formato adequado, lembrando que **não pode exceder o valor total de 100** para pie charts.
            - Tome cuidado para respeitar a sintaxe, preste bastante atenção nisso.
    4 - **Explique termos técnicos** de forma simples. Use exemplos práticos sempre que possível.  
    5 - **Se precisar modificar algum dado para usá-lo no gráfico,** explique ao usuário o que foi alterado e por quê.  
    6 - **Estruture a resposta em HTML de forma clara** para facilitar a leitura.  

        - Use **parágrafos `<p>`** para separar informações importantes.  
        - **Destaque termos importantes com `<span>`**.  
        - Para títulos ou seções importantes, use **`<h1>`, `<h2>`, etc.** conforme necessário.  
        - Use listas, tabelas, etc., para organizar as informações.

    **Exemplo de saída esperada:**

    <pre>
    {{
      "question": "Pergunta feita pelo usuário",
      "response": "Resposta em linguagem natural, separando HTML para conteúdo explicativo.",
      "visual": [
        "O diagrama Mermaid gerado (somente o código gerado pelo Mermaid)",
        "Outros diagramas gerados, se houver"
      ]
    }}
    </pre>

    **Caso faltem dados importantes:**  
    Se o usuário perguntar sobre um componente **não incluído** no JSON, responda:

    <p>Desculpe, não tenho informações sobre <span>componente</span> no momento. Tente consultar outro serviço.</p>

    FORMATE A SAÍDA CONFORME O JSON, separando cada informação pela CHAVE

    '''




