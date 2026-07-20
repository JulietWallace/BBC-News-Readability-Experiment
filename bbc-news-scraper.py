from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import textstat
from textstat import flesch_kincaid_grade

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
    driver.get(ref)
    WebDriverWait(driver, 2).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
)
    paras = driver.find_elements(by = By.TAG_NAME, value="p")
    date_element = driver.find_element(by = By.TAG_NAME, value="time")
    date = date_element.get_attribute("datetime")
    text_paragraphs = []
    for p in paras:
        text_paragraphs.append(p.text)

    text = "\n".join(text_paragraphs)

    file = open(file_name, "a")

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


    writer.writerow([ref, date, fkgl, fre,  dale_chall, gunning_fog, smog])

avg_fkgl = sum_fkgl/len(urls)

avg_fre = sum_fre/len(urls)

avg_dale_chall = sum_dale_chall/len(urls)

avg_gunning_fog = sum_gunning_fog/len(urls)

avg_smog = sum_smog/len(urls)

daily_average = open(output_file, "a")

writer = csv.writer(daily_average)

writer.writerow([datetime.datetime.now(), avg_fkgl, avg_fre, avg_dale_chall, avg_gunning_fog, avg_smog])











