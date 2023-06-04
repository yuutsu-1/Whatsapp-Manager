from time import sleep
import time
import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import socket
from urllib.parse import quote
import os
from selenium.webdriver.common.keys import Keys


def element_presence(by, css, time):
    element_present = EC.presence_of_element_located((by, css))
    WebDriverWait(driver, time).until(element_present)


def elemento_existe_css(css):
    try:
        driver.find_element(By.CSS_SELECTOR, css)
    except NoSuchElementException:
        return False
    return True
    

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True

    except BaseException:
        is_connected()

appPath = os.getenv("APPDATA")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(r"user-data-dir={app}\Local\Google\Chrome\User Data\Default".format(app=appPath))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def sendWhatsappMsg(phone_no, text):
    driver.get(
        "https://web.whatsapp.com/send?phone={number}&text={texto}".format(number=phone_no, texto=quote(text))
    )
    
    try:
        driver.switch_to.alert.accept()

    except:
        pass

    while elemento_existe_css("#app > div > div > div.landing-window > div.landing-main > div > div._25pwu > div._2UwZ_"):
        print("Favor ler QRCODE")
        sleep(5)

    try:
        element_presence(
            By.CSS_SELECTOR,
            '#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div._3HQNh._1Ae7k > button',
            60)
        botao_enviar = driver.find_element(
            By.CSS_SELECTOR, '#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div._3HQNh._1Ae7k > button')
        botao_enviar.click()
        
    except Exception:
        current_time = time.localtime()
        log.log_message(_time=current_time, receiver=phone_no, message=f"Não foi possível enviar mensagem para {phone_no}")

        

def sendWhatsappMsgAnexo(phone_no, text):
    driver.get(
        "https://web.whatsapp.com/send?phone={number}&text={texto}".format(number=phone_no, texto=quote(text))
    )
    
    try:
        driver.switch_to.alert.accept()

    except:
        pass

    while elemento_existe_css("#app > div > div > div.landing-window > div.landing-main > div > div._25pwu > div._2UwZ_"):
        print("Favor ler QRCODE")
        sleep(5)

    try:
        element_presence(
            By.CSS_SELECTOR,
            '#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div._3HQNh._1Ae7k > button',
            60)
        
        txtBox = driver.find_element(
            By.CSS_SELECTOR, '#main > footer > div._2BU3P.tm2tP.copyable-area > div > span:nth-child(2) > div > div._2lMWa > div.p3_M1')
        txtBox.send_keys(Keys.CONTROL, 'v')
        
        element_presence(
            By.CSS_SELECTOR,
            '#app > div > div > div._3ArsE > div.ldL67._3sh5K > span > div > span > div > div > div.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.r7fjleex.bs7a17vp > div > div._1HI4Y > div._33pCO',
            60)
        
        botao_enviar = driver.find_element(
            By.CSS_SELECTOR, '#app > div > div > div._3ArsE > div.ldL67._3sh5K > span > div > span > div > div > div.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.r7fjleex.bs7a17vp > div > div._1HI4Y > div._33pCO')
        botao_enviar.click()
        
    except Exception:
        current_time = time.localtime()
        log.log_message(_time=current_time, receiver=phone_no, message=f"Não foi possível enviar mensagem para {phone_no}")