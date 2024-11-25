from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from tkinter import Tk, filedialog, scrolledtext, messagebox
import time
import logging
import os
import pandas as pd
import tkinter as tk


def retornaDriver():
    driver = webdriver.Chrome()
    return driver


def retornaWait(driver):
    wait = WebDriverWait(driver, 60)
    return wait


def formataMensagem(mensagem):
    mensagemFormatada = mensagem.replace("\n", "%0A")

    return mensagemFormatada


def enviaMsg(driver, wait, numero, mensagemFormatada):
    driver.get(
        f'https://web.whatsapp.com/send?phone={numero}&text={mensagemFormatada}')
    try:
        enviar = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "span[data-icon='send']")))
        enviar.click()
        time.sleep(5)
        return True
    except NoAlertPresentException as e:
        logging.error(f'Erro ao clicar para enviar mensagem.\n')
        return False


def criaLog(nomeArquivo):
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Logs')

    if not os.path.exists(desktop):
        os.makedirs(desktop)

    logsPath = os.path.join(desktop, nomeArquivo)

    logging.basicConfig(filename=logsPath, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    return logging.getLogger()


def selecionarPlan():
    root = Tk()
    root.withdraw()
    caminhoArquivo = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx")])
    return caminhoArquivo


def solicitaMsg():
    root = Tk()
    root.title('Digite a mensagem a ser enviada')
    root.geometry("500x400")
    mensagem = tk.StringVar()

    def enviar():
        texto = text_area.get("1.0", tk.END).strip()
        textoF = formataMensagem(texto)
        mensagem.set(textoF)
        root.quit()

    text_area = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, width=45, height=10)
    text_area.pack(padx=20, pady=20)
    enviar_btn = tk.Button(root, text="Enviar", command=enviar)
    enviar_btn.pack(pady=10)
    root.mainloop()
    root.destroy()
    return mensagem.get()


def main():
    driver = retornaDriver()
    wait = retornaWait(driver)
    log = criaLog('AutoZapTexto.log')
    log.info(
        f'Automação AutoZapTexto iniciando.\nUser: {os.environ["USERPROFILE"]}\n')
    try:
        planilha = selecionarPlan()
    except Exception as e:
        messagebox.showerror('Planilha não encontrada!',
                             "Não foi localizada a planilha contendo os contatos.\nReinicie o programa e tente novamente.")
        log.error(f'Planilha não encontrada.\nErro retornado: {str(e)}')

    if planilha:
        df = pd.read_excel(planilha, dtype={'Celular': str})
    else:
        log.error(f'Erro! Planilha não encotrada.\n')
        messagebox.showerror('Planilha não encontrada!',
                             "Não foi localizada a planilha contendo os contatos.\nReinicie o programa e tente novamente.")
        return

    mensagem = solicitaMsg()

    if mensagem:
        log.info(f'Mensagem inserida: {mensagem}')
    else:
        messagebox.showerror('Mensagem não encontrada!',
                             "Não foi inserida a mensagem a ser enviada.\nReinicie o programa e tente novamente.")
        log.error(f'Nenhuma mensagem foi inserida.\nEncerrando programa.\n')
        return

    driver.get('https://web.whatsapp.com')
    driver.maximize_window()
    painel = wait.until(EC.presence_of_element_located((By.ID, 'side')))
    errados = []

    if painel.is_displayed():
        for index, row in df.iterrows():
            if pd.notnull(row['Celular']):
                numero = row['Celular']
                numeroFormatado = f'55{numero}'
                try:
                    if enviaMsg(driver, wait, numeroFormatado, mensagem):
                        log.info(
                            f'Mensagem enviada para o número: {numeroFormatado}')
                    else:
                        log.error(
                            f'Falha ao enviar mensagem para o número: {numeroFormatado}\n')
                        continue
                except Exception as e:
                    log.error(f'Numero: {numero} incorreto/não encontrado.\n')
                    errados.append(numero)
                    continue
                driver.delete_all_cookies()
            else:
                log.warning(f'Envio de mensagem falhou: Número {numero}.\n')
    root = Tk()
    root.withdraw()
    messagebox.showinfo(f'Programa Concluído.',
                        "O programa foi concluído com sucesso.\n\nConsulte o arquivo de log para mais informações.\n\nCaminho do arquivo: Área de trabalho > Pasta 'Logs'.")
    root.destroy()


if __name__ == "__main__":
    main()
# ------------------------------------- #
