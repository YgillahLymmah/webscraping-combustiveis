from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# Configurar opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializar o driver do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL da página com os dados
url = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis"
driver.get(url)
time.sleep(5)  # Esperar o carregamento da página

# Encontrar todos os links que contenham arquivos .csv
links = driver.find_elements(By.TAG_NAME, "a")
csv_links = []

for link in links:
    href = link.get_attribute("href")
    if href and href.endswith('.csv'):
        # Verificar se o link corresponde aos anos de interesse
        if any(ano in href for ano in ['2020', '2021', '2022', '2023', '2024', '2025']):
            csv_links.append(href)

driver.quit()

# Pasta onde os arquivos serão salvos
output_dir = "dados_combustiveis"
os.makedirs(output_dir, exist_ok=True)

# Baixar os arquivos encontrados
for link in csv_links:
    nome_arquivo = link.split("/")[-1]
    caminho = os.path.join(output_dir, nome_arquivo)
    try:
        response = requests.get(link)
        with open(caminho, "wb") as f:
            f.write(response.content)
        print(f"✅ Baixado: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao baixar {link}: {e}")

print("Download concluído.")
