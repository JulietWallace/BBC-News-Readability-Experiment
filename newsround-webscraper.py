from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.bbc.co.uk/newsround")

driver.implicitly_wait(0.5)

links = driver.find_elements(by = By.XPATH, value = "//ul/li/div[@type = 'article']/div/div/div/a[@href]")

print(len(links))

urls = []

for link in links:
    ref = link.get_attribute("href")
    print(ref)
    urls.append(ref)


for ref in urls:
    driver.get(ref)
    paras = driver.find_elements(by = By.TAG_NAME, value="p")
    text_paragraphs = []
    for p in paras:
        text_paragraphs.append(p.text)

    text = "\n".join(text_paragraphs)
    print(text)