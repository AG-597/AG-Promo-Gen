import os
import unittest
import requests
import base64
import json
import logging
import random
import string
import sys
import threading
import time
import tls_client
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore
import re as uwu
from kopeechka import MailActivations
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from seleniumbase import Driver
import time
import requests

kopeechka = "8af773f0a79d5701c64c708a3f984da8"

def type_text(element, text, min_delay=0.01, max_delay=0.05):
    """Simulate typing text into an element with a random delay between each keystroke."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))
        
def getuser():
    with open("data/usernames.txt", 'r', encoding='utf-8') as u:
        usernames = u.readlines()
        if usernames:
            username = random.choice(usernames).strip()
        else:
            raise ValueError("The usernames file is empty.")
    return username

def gen():
        
    print()
    print(Fore.LIGHTBLUE_EX + "=" * os.get_terminal_size().columns)    
    print(Fore.LIGHTGREEN_EX + center_text("LOGS"))
    print(Fore.LIGHTBLUE_EX + "=" * os.get_terminal_size().columns)
    
    fname = getuser()
    lname = getuser()
    mailapi = MailActivations(api_token=kopeechka)

    maildata = mailapi.mailbox_get_email("epicgames.com", "hotmail.com")

    email = maildata.mail
    emailid = maildata.id
    password = "JustANugget11!"

    driver = Driver(uc=True)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    cwait = WebDriverWait(driver, 30)
    driver.get("https://www.epicgames.com/id/login?lang=en-US&noHostRedirect=true&redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2Fp%2Fdiscord--discord-nitro")
    time.sleep(0.1)
    driver.get("https://www.epicgames.com/id/login?lang=en-US&noHostRedirect=true&redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2Fp%2Fdiscord--discord-nitro")
    mailinput = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    type_text(mailinput, email)    
    send_button = wait.until(EC.presence_of_element_located((By.ID, 'send')))
    send_button.click()
    input(Fore.YELLOW + "Press Enter Once Captcha Is Solved...")
    try:
        cwait.until(lambda driver: "date-of-birth" in driver.current_url)
        print(Fore.GREEN + "[+] Captcha Solved")
    except:
        print(Fore.RED + "[X] Failed To Solve Captcha...")
        driver.quit()
        gen()
        
    months = ["Jan", "Feb", "Mar", "Apr"]
    month = random.choice(months)
    wait.until(EC.presence_of_element_located((By.ID, 'month'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{month}')]"))).click()
    
    day = random.randint(1, 6)
    wait.until(EC.presence_of_element_located((By.ID, 'day'))).click()
    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN).perform()    
    actions.send_keys(day)
        
    wait.until(EC.presence_of_element_located((By.ID, 'year'))).send_keys(random.randint(1990 ,2003))
    
    wait.until(EC.presence_of_element_located((By.ID, "continue"))).click()
    
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(fname)
    wait.until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys(lname)
    wait.until(EC.presence_of_element_located((By.ID, "displayName"))).send_keys(f"{getuser()}_{random.randint(0000, 9999)}")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    wait.until(EC.presence_of_element_located((By.ID, "tos"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "btn-submit"))).click()
    while True:
    
            try:
                code= mailapi.mailbox_get_message(emailid, 1).fullmessage.split('letter-spacing: 10px !important;border-radius: 4px;">')[1].split('<br>')[0].strip()
                print(Fore.GREEN + "[+] Got Verification Code: " + code)
                break
            except Exception as E:
                time.sleep(1)
                
    for i, digit in enumerate(code):
        code_input = wait.until(EC.presence_of_element_located((By.NAME, f"code-input-{i}")))
        type_text(code_input, digit)
    wait.until(EC.presence_of_element_located((By.ID, "continue"))).click()
    
    cwait.until(lambda driver: "https://store.epicgames.com/en-US/p/discord--discord-nitro" == driver.current_url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1rdfk94"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "agree"))).click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-187rod9"))).click()
    
    resp = mailapi.mailbox_reorder("epicgames.com", email)
    emailid = resp.id
    print(Fore.YELLOW + f"[-] Waiting For Promo...")
    driver.quit()
    while True:

        try:
            code= mailapi.mailbox_get_message(emailid, 1).fullmessage.split('<p style="text-align:center;"> <a href="')[1].split('"')[0]
            print(Fore.MAGENTA + f"[*] Got Promo Code: {code[:40]}")
            open("promos.txt", "a").write(f"{code}\n")
            print()
            print(Fore.LIGHTBLUE_EX + "=" * os.get_terminal_size().columns)    
            print(Fore.LIGHTGREEN_EX + center_text("LOGS"))
            print(Fore.LIGHTBLUE_EX + "=" * os.get_terminal_size().columns)
            break
        except Exception as E:

            time.sleep(1)
    
def center_text(text):
    lines = text.split('\n')
    terminal_width = os.get_terminal_size().columns
    centered_lines = [(line.center(terminal_width)) for line in lines]
    return '\n'.join(centered_lines)

logo = Fore.LIGHTBLUE_EX + """
           _____     _____ ______ _   _ 
     /\   / ____|   / ____|  ____| \ | |
    /  \ | |  __   | |  __| |__  |  \| |
   / /\ \| | |_ |  | | |_ |  __| | . ` |
  / ____ \ |__| |  | |__| | |____| |\  |
 /_/    \_\_____|   \_____|______|_| \_|
                                
"""

def Main():
    print(center_text(logo))
    print(Fore.LIGHTGREEN_EX + center_text("[+] AG Promo Generator"))
    print(Fore.LIGHTGREEN_EX + center_text("[+] Made By AG-597 & Cypher"))
    print(Fore.LIGHTGREEN_EX + center_text("[+] Discord >>> https://discord.gg/kp3tTJeq2f"))
    print(Fore.LIGHTGREEN_EX + center_text("[+] Github >>> https://github.com/AG-597"))
    print()
    p = int(input((Fore.CYAN + "[-] Promos To Gen >>> ")))
    
    for i in range(p):
        gen()
        
    if p > 1:
        print(Fore.LIGHTGREEN_EX + center_text(f"[+] Successfully Made {p} promos"))
    else:
        print(Fore.LIGHTGREEN_EX + center_text("[+] Successfully Made 1 promo"))
        
    print(Fore.LIGHTGREEN_EX + center_text(f"[-] Enter To Exit..."))

os.system('cls')
Main()