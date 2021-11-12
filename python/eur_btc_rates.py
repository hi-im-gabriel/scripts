#Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from os import getcwd
import csv

#Filename constant
FILE_NAME = "eur_btc_rates.csv"

#Defining options to hide browser and lowering verbose by log-level
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')

#Starting scraping
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://finance.yahoo.com/quote/BTC-EUR/history/")

#Create a dictionary to put the values in ("Data" : "Close")
values = dict()

#Wait till page loads to avoid errors
date = WebDriverWait(driver,99).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[5]/td[1]/span'))) 

#Loop to get all 20 elements
for i in range(1,11):
    date = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{i}]/td[1]/span')
    
    #Avoid "Close" "-" value
    try:
        close = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{i}]/td[5]/span')
    except:
        close = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{i}]/td[5]')
    values[date.text]=close.text

#Opening/Creating .csv file
with open('eur_btc_rates.csv', mode='w') as csv_file:
    data_writer = csv.writer(csv_file, delimiter=',', lineterminator = '\n')

    #Columns
    data_writer.writerow(['Date', 'BTC Closing Value'])

    #Rows
    for i,j in values.items():
        data_writer.writerow([i, j])

#Quitting
driver.quit()
