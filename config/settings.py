
DEBUG = True
PORT = 5002
BASE_PATH = "/"
API_BASE_URL = f"http://localhost:{PORT}{BASE_PATH}"

def get_api_url(endpoint):
    """Gera URLs dinâmicas para os endpoints da API"""
    return f"{API_BASE_URL}{endpoint}"
