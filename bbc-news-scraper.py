from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

from bs4 import BeautifulSoup

import textstat

import time

import csv

import datetime

site = input("BBC or Newsround?")

if site == "BBC":
    url = "https://www.bbc.co.uk/news"
    path = "//ul/li/div/div[@type = 'article']/div/div/div/h3/a[@href]"
    file_name = "bbc-readability.csv"
    output_file = "daily-bbc-readability.csv"
else:
    url = "https://www.bbc.co.uk/newsround"
    path = "//ul/li/div[@type = 'article']/div/div/div/a[@href]"
    file_name = "newsround-readability.csv"
    output_file = "daily-newsround-readability.csv"

driver = webdriver.Chrome()

driver.get(url)

driver.implicitly_wait(3)

links = driver.find_elements(by = By.XPATH, value = path)

urls = []

for link in links:
    ref = link.get_attribute("href")
    if "/live/" not in ref and "/videos/" not in ref and ref not in urls: #not looking at live stories
        urls.append(ref)

sum_fkgl = 0
sum_fre = 0
sum_dale_chall = 0
sum_gunning_fog = 0
sum_smog = 0

for ref in urls:
    page = requests.get(ref)
    page.encoding = "utf-8"


    soup = BeautifulSoup(page.text, "html.parser")
    article = soup.find("article")

    paras = []
    for p in article.select('[data-block="text"] p'):
        paras.append(p.get_text())

    text = "\n".join(paras)

    date = datetime.datetime.now().strftime("%d-%m-%y")

    file = open("./data/{date}-{file}".format(date=date, file=file_name), "a") #this saves the data from each day. timestamped so we know what day it is from.

    writer = csv.writer(file)

    fkgl = textstat.flesch_kincaid_grade(text)
    sum_fkgl += fkgl
    fre = textstat.flesch_reading_ease(text)
    sum_fre += fre
    dale_chall = textstat.dale_chall_readability_score(text)
    sum_dale_chall += dale_chall
    gunning_fog = textstat.gunning_fog(text)
    sum_gunning_fog += gunning_fog
    smog = textstat.smog_index(text)
    sum_smog += smog


    writer.writerow([ref, fkgl, fre,  dale_chall, gunning_fog, smog])
    time.sleep(0.5)

avg_fkgl = sum_fkgl/len(urls)

avg_fre = sum_fre/len(urls)

avg_dale_chall = sum_dale_chall/len(urls)

avg_gunning_fog = sum_gunning_fog/len(urls)

avg_smog = sum_smog/len(urls)

daily_average = open(output_file, "a")

writer = csv.writer(daily_average)

writer.writerow([datetime.datetime.now(), avg_fkgl, avg_fre, avg_dale_chall, avg_gunning_fog, avg_smog])











