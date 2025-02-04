import os

def get_documentation():
    
    NAME_DIRECTORY = "api/docs"
    EXTENTION_FILE = ".md"

    READ = "r"
    CODIFICATION = "utf-8"

    endpoint_doc = []
    
    # Verifica se o diretório existe
    if not os.path.exists(NAME_DIRECTORY):
        return endpoint_doc
    
    # Itera sobre todos os arquivos no diretório
    for file_name in os.listdir(NAME_DIRECTORY):

        if file_name.endswith(EXTENTION_FILE):
            file_path = os.path.join(NAME_DIRECTORY, file_name)
            
            # Lê o conteúdo do arquivo .md
            with open(file_path, READ, encoding=CODIFICATION) as file:
                content = file.read()
                endpoint_doc.append(content)
    
    # Gera um prompt com base no conteúdo dos arquivos
    final_doc = "\n\n".join(endpoint_doc)

    return final_doc