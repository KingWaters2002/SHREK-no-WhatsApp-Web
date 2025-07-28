# Importação das variaveis do Selenium para usar o script
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
# Importacaoo do time para pausas e do json para ler o arquivo de legenda
import time
import json

# Abrindo o arquivo de configuracoes
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
# Atribuindo os valores as variaveis
contato_nome = config["contato"]
tempoMensagem = config["tempo_entremensagens"]
tempoAutenticacao = config["tempo_paraaguardarautenticacao"]
# Inicializando o navegador Chrome
CAMINHO_DRIVER = './chromeDriver/chromedriver.exe'
options = webdriver.ChromeOptions() 
options.add_argument("--log-level=3")
service = Service(CAMINHO_DRIVER) 
driver = webdriver.Chrome(service=service, options=options) 
# driver = webdriver.Chrome()

# Abre o WhatsApp Web
driver.get(config["site"])
print("Esperando a autenticação")
time.sleep(tempoAutenticacao)  # Aguarde o usuário fazer a autenticação manualmente
print("Autenticação - ok")

# Abre o arquivo de legenda
try:
    with open(config["nome_arquivo"], "r", encoding="utf-8") as arquivo_legenda:
        mensagemCompleto = arquivo_legenda.read()
except FileNotFoundError:
    print("Erro: O arquivo 'legenda_shrek.txt' não foi encontrado. Verifique se ele está na mesma pasta do script.")
    exit() # Encerra o script se o arquivo não for encontrado
# Faz o arquivo ficar separado, sendo a separacao o " " (espaço em branco), para enviar palavra por palavra
mensagemCompletoSlitado = mensagemCompleto.split(config["split"],)

# Espera até que a caixa de pesquisa esteja disponível
caixa_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)

# Insere o nome do contato na caixa de pesquisa
caixa_pesquisa.send_keys(contato_nome)
caixa_pesquisa.send_keys(Keys.ENTER)

# Percorre todo o arquivo de legenda
for mensagem in mensagemCompletoSlitado:
    try:
        # Espera até que a caixa de mensagem esteja disponível
        caixa_mensagem = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        
        # Insere a mensagem na caixa de mensagem
        caixa_mensagem.send_keys(mensagem)
        caixa_mensagem.send_keys(Keys.ENTER)

        # Aguarda até que a mensagem seja de fato exibida no chat e enviada
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="msg-check"]'))
            )
        except:
            print(f"⚠️ A mensagem '{mensagem}' pode não ter sido enviada.")
        
        # Aguarda um pouco para garantir que a mensagem seja enviada
        time.sleep(tempoMensagem)

        # Verifica se o WhatsApp ficou offline, se sim fecha tudo
        if "offline" in driver.page_source:
            print("❌ WhatsApp Web está offline.")
            driver.quit()
            exit()
    
    except Exception as e:
        print("Ocorreu um erro:", e)

# Fecha o navegador
driver.quit()
