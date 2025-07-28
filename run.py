from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

contato_nome = config["contato"]
tempoMensagem = config["tempo_entremensagens"]
tempoAutenticacao = config["tempo_paraaguardarautenticacao"]

# Inicializa o navegador Chrome
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

try:
    with open("SHREK.txt", "r", encoding="utf-8") as arquivo_legenda:
        mensagemCompleto = arquivo_legenda.read()
except FileNotFoundError:
    print("Erro: O arquivo 'legenda_shrek.txt' não foi encontrado. Verifique se ele está na mesma pasta do script.")
    exit() # Encerra o script se o arquivo não for encontrado

mensagemCompletoSlitado = mensagemCompleto.split(" ")

#print("Try 1")
# Espera até que a caixa de pesquisa esteja disponível
caixa_pesquisa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
#print("Localizado caixa de pesquisa")

# Insere o nome do contato na caixa de pesquisa
caixa_pesquisa.send_keys(contato_nome)
caixa_pesquisa.send_keys(Keys.ENTER)
#print("Colocado o nome do contato na caixa de pesquisa")

for mensagem in mensagemCompletoSlitado:
    mensagem
    #print("Contato " + contato_nome + " - Mensagem: " + mensagem)
    try:
        
        # Espera até que a caixa de mensagem esteja disponível
        caixa_mensagem = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        #print("Esperando disponibilidade da caixa de mensagem")
        
        # Insere a mensagem na caixa de mensagem
        caixa_mensagem.send_keys(mensagem)
        caixa_mensagem.send_keys(Keys.ENTER)

        # Aguarda até que a mensagem seja de fato exibida no chat (e enviada)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="msg-check"]'))
            )
        except:
            print(f"⚠️ A mensagem '{mensagem}' pode não ter sido enviada.")
        #print("Anexado mensagem")
        
        # Aguarda um pouco para garantir que a mensagem seja enviada
        #print("Aguardando garantia da mensagem ter ido")
        time.sleep(tempoMensagem)
        #print("Finalizando")

        if "offline" in driver.page_source:
            print("❌ WhatsApp Web está offline.")
            driver.quit()
            exit()
    
    except Exception as e:
        print("Ocorreu um erro:", e)

# Fecha o navegador
driver.quit()
