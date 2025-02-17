import os

def get_documentation():
    
    NAME_DIRECTORY = "api/docs"
    EXTENTION_FILE = ".md"

    READ = "r"
    CODIFICATION = "utf-8"

    prompts = []
    
    # Verifica se o diretório existe
    if not os.path.exists(NAME_DIRECTORY):
        return prompts
    
    # Itera sobre todos os arquivos no diretório
    for file_name in os.listdir(NAME_DIRECTORY):
        if file_name.endswith(EXTENTION_FILE):
            file_path = os.path.join(NAME_DIRECTORY, file_name)
            
            # Lê o conteúdo do arquivo .md
            with open(file_path, READ, encoding=CODIFICATION) as file:
                content = file.read()
                prompts.append(content)
    
    # Gera um prompt com base no conteúdo dos arquivos
    prompt_final = "\n\n".join(prompts)

    return prompt_final