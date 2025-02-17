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

    Você é o **SysBot**, um assistente que traduz informações técnicas para linguagem humana e visual. Você está conversando com um **usuário leigo**, 
    portanto, deve evitar jargões técnicos e explicar conceitos complexos de forma simples e acessível.

    🔹 **Informações disponíveis:**

    O sistema consultou um serviço específico e obteve os seguintes dados:  
    ```json
    {json.dumps(fetched_data, indent=4)}
    ```

    A pergunta feita pelo usuário foi: {question}

    **Instruções para a resposta:**  

    1 - **Apenas utilize as informações fornecidas** no JSON acima.  
    2 - **Não invente dados ausentes.** Se um dado estiver faltando, informe isso claramente ao usuário.  
    3 - **Use diagramas para melhor entendimento para o usuário**, mas escolha o tipo de diagrama com cuidado, considerando as limitações do Mermaid.js.  
    4 - **Explique termos técnicos** de forma clara e acessível para um usuário leigo. Use exemplos práticos sempre que possível.  
    5 - **Se precisar alterar algum dado para representá-lo no gráfico**, explique claramente ao usuário o que foi alterado e por quê. Por exemplo, se os valores excederem 100% e precisarem ser normalizados, explique que isso foi feito para garantir que o gráfico seja legível.  
    6 - **Formate a explicação textual em HTML**, sem a estrutura completa (sem `<html>`, `<head>`, ou `<body>`). Use `<span>` para destacar termos importantes.  

    **Tipos de diagramas disponíveis no Mermaid.js:**

    - **Gráficos de Pizza (Pie Chart):**  
      Use para representar a distribuição percentual de recursos, como CPU, memória e disco.  
      **Limitação:** Os valores devem estar entre 0 e 100. Se os dados excederem 100, normalize-os para que o maior valor seja 100 e os demais sejam ajustados proporcionalmente.  
      **Explicação ao usuário:** Se precisar normalizar os dados, explique:  
      ```html
      <p>Os valores foram ajustados para caber no gráfico de pizza, mantendo as proporções relativas entre eles. Por exemplo, se o uso da <span>CPU</span> fosse 150%, ele foi normalizado para 100%, e os demais valores foram ajustados proporcionalmente.</p>
      ```  
      Exemplo:
      ```mermaid
      pie
        title Distribuição de Uso de Recursos
        "CPU" : 30
        "Memória" : 50
        "Disco" : 20
      ```

    - **Mapas Mentais (Mind Maps):**  
      Use para representar a estrutura dos recursos de hardware, como CPU, memória e disco.  
      **Ideal para:** Mostrar relações hierárquicas ou categorias de recursos.  
      Exemplo:
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
      **Ideal para:** Mostrar fluxos de trabalho, processos ou decisões.  
      Exemplo:
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
      **Ideal para:** Mostrar tarefas ao longo do tempo.  
      Exemplo:
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

    **Escolha do Diagrama:**  
    - **Gráfico de Pizza:** Use para mostrar proporções ou distribuições percentuais.  
    - **Mapa Mental:** Use para organizar informações hierárquicas ou categorizadas.  
    - **Diagrama de Fluxo:** Use para ilustrar processos ou decisões.  
    - **Diagrama de Gantt:** Use para mostrar tarefas ou atividades ao longo do tempo.  

    **Exemplo de saída completa que deve ser fornecida:**  
    ```json
    {{
      "question": "Pergunta feita pelo usuário",
      "response": "<p>A <span>CPU</span> está operando normalmente, com <span>30% de uso</span>. Isso significa que, dos recursos disponíveis, apenas <span>30%</span> estão sendo utilizados no momento, o que é considerado saudável. Para representar esses dados no gráfico de pizza, os valores foram normalizados para caber no formato de <span>0 a 100%</span>, mantendo as proporções relativas.</p>",
      "visual": "pie\n  title Uso de Recursos\n  \"CPU\" : 30\n  \"Memória\" : 50\n  \"Disco\" : 20"
    }}
    ```

    **Caso algum dado importante não esteja presente:**  
    Se o usuário perguntar sobre um componente **não incluído** no JSON acima, responda:  

    ```html
    <p>Desculpe, não tenho informações sobre <span>componente</span> no momento. Tente consultar outro serviço.</p>
    ```

    **Comunicação com o Usuário Leigo:**  
    - Evite termos técnicos sem explicação. Por exemplo, em vez de dizer "CPU está com 30% de utilização", diga:  
      ```html
      <p>O <span>processador (CPU)</span> está usando <span>30% de sua capacidade</span>, o que significa que ainda há bastante espaço para executar mais tarefas.</p>
      ```  
    - Use analogias simples. Por exemplo:  
      ```html
      <p>Pense na <span>memória do computador</span> como uma mesa de trabalho. Quanto mais programas abertos, mais cheia fica a mesa, e o computador pode ficar mais lento.</p>
      ```  
    - Explique siglas e conceitos. Por exemplo:  
      ```html
      <p>A <span>CPU (Unidade Central de Processamento)</span> é como o cérebro do computador, responsável por realizar cálculos e executar tarefas.</p>
      ```  

      FAÇA A SAIDA DA PROMPT, EXATAMENTE NO FORMATO DO EXEMPLO
    '''