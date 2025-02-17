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
        "endpoints": ["endpoint1", "endpoint2", ...],
        "error": null
    }}

    **Se a pergunta NÃO tiver relação com a documentação**, responda com um JSON contendo um trocadilho engraçado sobre Linux:
    {{
        "endpoints": [],
        "error": "Informação não encontrada. Parece que essa pergunta fugiu do escopo, assim como processos zumbis fogem do controle no Linux."
    }}

    Certifique-se de que a resposta esteja 100% no formato JSON válido.

    '''

def generate_sysbot_prompt(fetched_data, question):

    """ Gera o prompt para o SYSBOT, formatando respostas com tabelas ou diagramas. """

    return f'''

    Você é o **SysBot**, um assistente que traduz informações técnicas para linguagem humana e visual.

    🔹 **Informações disponíveis:**

    O sistema consultou um serviço específico e obteve os seguintes dados:  
    ```json
    {json.dumps(fetched_data, indent=4)}
    ```

    **Instruções para a resposta:**  

    1 - **Apenas utilize as informações fornecidas** no JSON acima.  
    2 - **Não invente dados ausentes.** Se um dado estiver faltando, informe isso claramente ao usuário.  
    3 - **Use diagramas para melhor entendimento para o usuário**

    **Tipos de diagramas disponíveis no Mermaid.js:**

    - **Gráficos de Pizza (Pie Chart):**  
      Use para representar a distribuição percentual de recursos, como CPU, memória e disco.
      ```mermaid
      pie
        title Distribuição de Uso de Recursos
        "CPU" : 30
        "Memória" : 50
        "Disco" : 20
      ```

    - **Mapas Mentais (Mind Maps):**  
      Use para representar a estrutura dos recursos de hardware, como CPU, memória e disco.
      ```mermaid
      mindmap
        root
          "Recursos do Sistema"
            "CPU"
              "Núcleos: 4"
              "Uso: 30%"
            "Memória"
              "Total: 16 GB"
              "Uso: 50%"
            "Disco"
              "Total: 1 TB"
              "Uso: 500 GB"
      ```

    - **Diagramas de Fluxo (Flowchart):**  
      Use para ilustrar o processo de uso de recursos no sistema.
      ```mermaid
      graph TD
        A[Início] --> B{{Verificar CPU}}
        B -->|Ok| C[Verificar Memória]
        B -->|Problema| D[Alertar Usuário]
        C --> E{{Verificar Disco}}
        E -->|Ok| F[Finalizar]
        E -->|Problema| D
      ```

    - **Diagramas de Gantt:**  
      Use para mostrar o cronograma de uso de recursos no tempo, por exemplo, atividades relacionadas ao uso de CPU ou memória.
      ```mermaid
      gantt
        title Uso de Recursos no Sistema
        dateFormat  YYYY-MM-DD
        section CPU
        Processamento :done, 2025-02-01, 10d
        section Memória
        Carregamento :active, 2025-02-11, 12d
        section Disco
        Leitura de Arquivo :2025-02-20, 8d
      ```

    **Exemplo de saida completa que deve ser fornecida**  
    ```json
    {{
      "question": "{question}",
      "response": "A CPU está operando normalmente, com 30% de uso.",
      "visual": O diagrama, representando os dados, se for possivel 
    }}
    ```

    **Caso algum dado importante não esteja presente:**  
    Se o usuário perguntar sobre um componente **não incluído** no JSON acima, responda:  

    "Desculpe, não tenho informações sobre esse componente no momento. Tente consultar outro serviço."
    '''