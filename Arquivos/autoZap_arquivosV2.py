from tkinter import Tk, filedialog, messagebox
import pandas as pd
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def selecionarPlan():
    root = Tk()
    root.withdraw()
    caminhoArquivo = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx")])
    return caminhoArquivo


def abreGrupo(wait):
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Robô')]"))).click()
    except Exception as e:
        logging.error(
            f'Erro ao abrir o grupo do Robô.\nErro retornado:{str(e)}')


def encaminhaMsg(wait, driver):
    sleep(2)
    try:
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='application']")))
        aplication = driver.find_element(
            By.XPATH, "//div[@role='application']")
        lastRow = aplication.find_element(
            By.CSS_SELECTOR, "div[role='row']:last-child")
        foward = lastRow.find_element(
            By.XPATH, "//div[@role='button' and @aria-label='Encaminhar mídia']")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='button' and @aria-label='Encaminhar mídia']")))
        foward.click()
    except Exception as e:
        logging.error(
            f'Erro ao clicar para encaminhar a ultima mensagem.\nErro retornado: {str(e)}')


def enviaMensagem(driver, wait, contatos):
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@title="Encaminhar mensagem para"]')))
    pesquisa = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@role="textbox" and @contenteditable="true" and @data-lexical-editor="true"]')))

    erros = []
    for contato in contatos:
        try:
            pesquisa.send_keys(Keys.CONTROL + "a")
            pesquisa.send_keys(Keys.DELETE)
            sleep(1)
            pesquisa.send_keys(contato)
            sleep(1)
            try:
                check = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[@role='checkbox' and @aria-checked='false']")))
                check.click()
                pesquisa.send_keys(Keys.CONTROL + "a")
                pesquisa.send_keys(Keys.DELETE)
                sleep(1)
            except Exception as e:
                logging.error(
                    f'Erro ao marcar checkbox. Contato que deu errado: {contato}\nErro retornado: {str(e)}')
                pesquisa.send_keys(Keys.CONTROL + "a")
                pesquisa.send_keys(Keys.DELETE)
                erros.append(contato)
                continue
        except Exception as e:
            logging.error(
                f'Erro no sendkeys. Contato que deu errado: {contato}.\nErro retornado: {str(e)}')
            pesquisa.send_keys(Keys.CONTROL + "a")
            pesquisa.send_keys(Keys.DELETE)
            erros.append(contato)
            continue
    try:
        enviar = driver.find_element(
            By.XPATH, '//span[@aria-label="Enviar" and @data-icon="send"]')
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@aria-label='Enviar' and @data-icon='send']")))
        enviar.click()
    except Exception as e:
        logging.error(
            f'Erro ao clicar em enviar mensagem.\nErro retornado:{str(e)}')


def mostraPopup():
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Automação Concluída",
                        "A automação foi concluida.\n\nClique em 'Ok' para encerrar o programa.")
    root.destroy()


def criaLog(nomeArquivo):
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Logs')

    if not os.path.exists(desktop):
        os.makedirs(desktop)

    logsPath = os.path.join(desktop, nomeArquivo)

    logging.basicConfig(filename=logsPath, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    return logging.getLogger()


def main():
    log = criaLog('AutoZapArquivos.log')
    log.info(
        f"Automação AutoZapArquivos iniciando.\nUser: {os.environ['USERPROFILE']}\n")
    planilha = selecionarPlan()
    df = pd.read_excel(planilha, dtype={'Celular': str})
    contatos = df['Celular'].tolist()
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        wait = WebDriverWait(driver, 60)
        driver.get('https://web.whatsapp.com/')
    except Exception as e:
        logging.error(
            f'Erro ao iniciar o WebDriver.\nErro retornado: {str(e)}')
        return
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'pane-side')))
        abreGrupo(wait)
        encaminhaMsg(wait, driver)
        for i in range(0, len(contatos), 5):
            enviaMensagem(driver, wait, contatos[i:i+5])
            sleep(2)
            if i + 5 < len(contatos):
                abreGrupo(wait)
                encaminhaMsg(wait, driver)
    except Exception as e:
        logging.error(f'Erro ao executar programa.\nErro retornado: {str(e)}')
    finally:
        mostraPopup()
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
