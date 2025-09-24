from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

#Configurations
print("Enter bni website extension (example: lt):")
raw_link = input("Enter input: ")
print("Enter file name for scraped information (example: membersLt)")
filename = input("Enter input: ")
print("Enter delay in seconds for browser to load pages (default: 3, when entering nothing)")
delay = int(input("Enter input: ") or 3)
parser = "html.parser"
WAIT_LOCATED = 'located'
WAIT_CLICK = 'click'



def main(raw_link, filename, delay):
    driver = webdriver.Chrome()
    
    if delay == None or delay == 0:
        delay = 3

    link = f"https://bni.{raw_link}"
    links = []

    if os.path.exists(f'{filename}.csv') and os.path.exists(f'BNI_Pending_{filename}.csv'):
        get_member_info(driver, filename)


    else:
        with open (f'{filename}.csv', 'w') as file:
            file.write("#;Name;Company;Description;Phone number;Email link")

        get_links(link, driver, links)
        get_member_info(driver, filename)

    driver.quit()

def get_links(link, driver, links):
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, parser)
    lang = soup.find('html')['lang']
    
    wait_for_element(driver, delay, '[href="advancedchaptersearch"]', WAIT_CLICK)

    button = driver.find_element(By.CSS_SELECTOR, '[href="advancedchaptersearch"]')
    button.click()

    wait_for_element(driver, delay, '[name="chapterCity"]', WAIT_LOCATED)

    driver.page_source
    options = driver.find_element(By.CSS_SELECTOR, '[name="chapterCity"]').text.split('\n')
    
    for option in options:
        select = Select(driver.find_element(By.CSS_SELECTOR, '[name="chapterCity"]'))
        select.select_by_value(option)

        wait_for_element(driver, delay, '[name="submit"]', WAIT_CLICK)

        button = driver.find_element(By.CSS_SELECTOR, '[name="submit"]')
        button.click()

        wait_for_element(driver, delay, '[id="chapterList"]', WAIT_LOCATED)

        soup = BeautifulSoup(driver.page_source, parser)
        raw_chapterlist = soup.find_all('tr', class_=['even', 'odd'])
        
        for mem in raw_chapterlist:
            links.append(f"https://bni.{raw_link}/{lang}/" + mem.find('td').a['href'])

        driver.back()
    
    write_pending_links(links, filename)



def get_member_info(driver, filename):
    link_count = 0
    i = 0
    failed_links = []
    links = []

    with open(f'BNI_Pending_{filename}.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                links.append(row[0])


    for link in links.copy():
        try:
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, parser)
            lang = soup.find('html')['lang']

            wait_for_element(driver, delay, '[id="chapterDetail"]', WAIT_LOCATED)

            soup = BeautifulSoup(driver.page_source, parser)
            raw_memberlist = soup.find_all('tr', class_=['even', 'odd'])

            for mem in raw_memberlist:
                i += 1
                name = mem.find_all('td')[0].a.text
                company = mem.find_all('td')[1].text
                description = mem.find_all('td')[2].text
                phone_nr = mem.find_all('td')[3].bdi.text
                send_mail = ''
                try:
                    send_mail = f"https://bni.{raw_link}/{lang}/" + mem.find_all('td')[4].a['href']

                except Exception as e:
                    print (f'Failed to process {mem}: {e}')
                    pass

                with open (f'{filename}.csv', 'a') as file:
                    file.write(f"\n{i};{name};{company};{description};{phone_nr};{send_mail}")
        
        except Exception as e:
            print (f'Failed to process {link}: {e}')
            failed_links.append(link)

        finally:
            links.remove(link)
            print(f'{len(links)} links left.')
            link_count += 1

            if link_count % 10 == 0 or len(links) == 0:
                write_pending_links(links, filename)
                print('Progress saved to file.')

        if failed_links:
            write_failed_links(failed_links, filename)

def write_pending_links(links, filename):
    with open(f"BNI_Pending_{filename}.csv", 'w') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link])

def write_failed_links(failed_links, filename):
    with open(f"BNI_Failed_Links_{filename}.csv", 'w') as file:
        writer = csv.writer(file)
        for link in failed_links:
            writer.writerow([link])

def wait_for_element(driver, delay, selector, wait_type):
    start = time.time()
    if wait_type == WAIT_CLICK:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
    elif wait_type == WAIT_LOCATED:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    passed = time.time() - start
    if passed < delay:
        time.sleep(delay - passed)

main(raw_link, filename, delay)

