import time

import openpyxl
from Persona import Persona
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

workbook = openpyxl.load_workbook("fotocasa.xlsx")
sheet = workbook.active
a1 = sheet['A1']
a2 = sheet['A2']
filas = sheet
lista_perosnas = []

for fila in filas.iter_rows(min_row=2):
    nom = fila[0].value
    tlf = fila[1].value
    pob = fila[2].value
    hab = fila[3].value
    p_max = fila[4].value
    lista_perosnas.append(Persona(nom,tlf,pob,hab,p_max))

workbook.close()
# FIN DEL EXCEL #
# INICO PÁGINA INMOBILIARIA #
"""
Antes de empezar debes abrir la powershell e ir a la carpeta dónde esté instalado chrome
 cd C:\"Program Files"\Google\Chrome\Application
Después hay que ejecutar chrome con este comando
 .\chrome.exe --remote-debugging-port=9999 --user-data-dir="C:\test"

"""
def quitar_card(driver):
    try:
        btn = driver.find_elements(by=By.XPATH,
                                   value="//button[@class='sui-AtomButton sui-AtomButton--primary sui-AtomButton--flat sui-AtomButton--center sui-AtomButton--fullWidth']")
        if btn:
            btn[0].click()
        time.sleep(1)
    except :
        pass


for persona in lista_perosnas:
    # Abrir navegador
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.fotocasa.es/es/")

    # Aceptar Cookies
    time.sleep(0.5)
    btn_cookies = driver.find_elements(by=By.XPATH, value="//button[@data-testid='TcfAccept']")
    if btn_cookies:
        btn_cookies[0].click()

    # Buscar provincia
    barra_busqueda = driver.find_elements(by=By.XPATH, value="//input[@placeholder='Buscar vivienda en municipio, barrio...']")
    barra_busqueda[0].send_keys(persona.poblacion)
    btn_busqueda = driver.find_elements(by=By.XPATH, value="//button[@type='submit']")
    btn_busqueda[0].click()
    time.sleep(1)

    # Precio Máximo
    driver.find_elements(by=By.XPATH, value="//div[@class='sui-MoleculeSelectPopover-select sui-MoleculeSelectPopover-select--m']")[2].click()
    time.sleep(1)
    driver.find_elements(by=By.XPATH, value="//input[@value='Indiferente']")[1].click()
    time.sleep(1)

    preciomax = driver.find_elements(By.XPATH,
    value=f"//*[@id='App']/div[2]/div[1]/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/ul/li[@data-value={persona.precio_max}]")

    if preciomax[0]:
        lista_precios_ul = driver.find_elements(By.XPATH,
        value=f"//*[@id='App']/div[2]/div[1]/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/ul")
        flag = True
        pixeles = 10
        while flag:
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.ARROW_DOWN)
                actions.perform()
                actions.send_keys(Keys.ARROW_DOWN)
                actions.perform()
                time.sleep(0.5)
                pixeles += 10
                preciomax[1].click()
                flag = False
                time.sleep(1)
            except Exception as e:
                print(e)

    # Mostrar resultados y cerrar card
    driver.find_elements(By.XPATH, value="//*[@id='App']/div[2]/div[1]/div[3]/div/div/div/div/div/button")[0].click()
    time.sleep(1)
    quitar_card(driver)

    # Número de habitaciones
    driver.find_elements(by=By.XPATH, value="//div[@class='sui-MoleculeSelectPopover-select sui-MoleculeSelectPopover-select--m']")[2].click()
    time.sleep(3)
    driver.find_elements(by=By.XPATH,
    value=f"//*[@id='App']/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div[1]/div/div/div[2]/button[@aria-label='{persona.habitaciones}+']")[0].click()
    driver.find_elements(By.XPATH, value="//*[@id='App']/div[2]/div[1]/div[3]/div/div[2]/div[3]/div[2]/div[2]/button")[0].click()
    time.sleep(1)
    quitar_card(driver)

    # Ordenar por recientes
    selector_ordenacion = driver.find_elements(by=By.XPATH, value="//select[@aria-label='Ordenar por:']")
    selector_ordenacion[0].click()
    selector_ordenacion[0].find_elements(by=By.XPATH, value="//option[@value='publicationDate,true']")[0].click()
    time.sleep(3)
    quitar_card(driver)

    # Conseguir primer anuncio y hacer click en el precio
    primera_publicacion = driver.find_elements(by=By.XPATH, value="//article[@class='re-CardPackMinimal']")[0]
    precio_publicacion = driver.find_elements(by=By.XPATH, value="//span[@class='re-CardPrice']")[0]
    precio_publicacion.click()
    url_publicacion = driver.current_url

    #Url wahsapp
    url_whatsapp = f"https://web.whatsapp.com/send?phone=+34{persona.telefono}&text=Hola+*{persona.nombre}*!!+Echa+un+vistazo+al+siguiente+anuncio%0A{url_publicacion}"
    driver.get(url_whatsapp)
    time.sleep(5)
    btn_enviar = driver.find_elements(by=By.XPATH, value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span[@data-testid='send']")[0]
    btn_enviar.click()
    driver.quit()
