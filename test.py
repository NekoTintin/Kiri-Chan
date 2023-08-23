from selenium import webdriver
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

opts = webdriver.ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)

driver.get("https://www.youtube.com/@MiyunaASMR")
elem = driver.find_element("id", "img")

for e in elem:
    print(e.text)
    
driver.quit()