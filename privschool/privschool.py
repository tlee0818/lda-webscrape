import requests
from urllib import request
import time
import bs4
from bs4 import BeautifulSoup
import ssl
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ssl._create_default_https_context = ssl._create_unverified_context

DRIVER_PATH = "/Users/texeirareborn/Downloads/chromedriver"
BASE_LINK = "https://www.privateschoolreview.com"
# creating multiple user agents and sleeptimes to avoid bot detection
HEADERS = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}]
SLEEP_TIMES = [0.5, 0.7, 1, 1.2]


def scrape(url, fields, outfile):
    info = []

    # clicks on the right arrow key in the pagination area
    with open(outfile, 'w', newline='') as l:
        writer = csv.writer(l)
        writer.writerow(fields)

        print("opening driver")
        school_list_text = get_school_list(url)

        schools = BeautifulSoup(school_list_text, "html.parser")


        for school in schools:
            time.sleep(getRandomSleepTime())  # bot detection

            if school and school.name == "div" and "tp-list-row" in school['class']:
                if not school.find("a", {"class": "tpl-school-link"}):
                    print(school)
                    continue

                path = (school.find("a", {"class": "tpl-school-link"}))["href"]
                
                # append school info from get_school_info()
                info.append(get_school_info(path))
                writer.writerow(list(info[-1]))
                print(info[-1])

    return info


def get_school_list(url):
    s = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=s)
    driver.get(url)

    error_count = 0

    while error_count < 10:
        try:
            driver.find_element_by_id('tpl-showmore').click()
            print("clicking again")
            time.sleep(5)
        except:
            error_count += 1
            time.sleep(5)

    return (driver.find_element_by_id('tp-school-list')).get_attribute('innerHTML')

#for fields we can't find
EMPTY = "N/A"

def get_school_info(path):

    card_soup = BeautifulSoup(requests.get(BASE_LINK + path, headers= getRandomHeader()).text, "html.parser")

    name = card_soup.find('h1', {'id': 'main-headline'}).text.strip()
    
    address = EMPTY
    zipcode = EMPTY
    number = EMPTY
    website = BASE_LINK + path

    address_card = card_soup.find('div', {'class': "card-address"})
    phone_card = card_soup.find('div', {'class': "card-tel"})
    website_card = card_soup.find('div', {'class': "card-website"})

    #address
    if address_card:
        addy_parts = address_card.find('div', {'class': "cr_content_wrapper"}).children
        addy_parts_list = []
        for part in addy_parts:
            if part.text:
                addy_parts_list.append(part.text)

        if addy_parts_list[-1].isnumeric():
            zipcode = addy_parts_list[-1]
        
        address = (" ".join(addy_parts_list[:-1])).strip()

    #phone
    if phone_card:
        content = phone_card.find('div', {'class': "cr_content_wrapper"})
        if content:
            number = content.a.text
    #website
    if website_card:
        content = website_card.find('div', {'class': "cr_content_wrapper"})
        if content:
            website = content.a.text

    type = EMPTY
    grades = EMPTY
    student_body_type = EMPTY
    religion = EMPTY
    total_students = EMPTY
    class_size = EMPTY
    adhd_support = EMPTY
    learning_difference_support = EMPTY
    programs = EMPTY
    
    detail_rows = card_soup.find_all('div', {'class': 'dt-row'})

    for row in detail_rows:

        #school type
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "School Type":
            type = row.find('div', {'class': "dt-value-cell"}).a.text.strip()
        
        #religion
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Religious Affiliation":
            religion = row.find('div', {'class': "dt-value-cell"}).a.text.strip()
        
        #grades
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Grades Offered":
            grades = row.find('div', {'class': "dt-value-cell"}).text.strip()
        
        #adhd
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "ADD/ADHD Support":
            adhd_support = row.find('div', {'class': "dt-value-cell"}).text.strip()
        
        #ld programs
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Learning Difference Programs":
            learning_difference_support = row.find('div', {'class': "dt-value-cell"}).text.strip()

        #learning programs
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Learning Programs Supported":
            programs = row.find('div', {'class': "dt-value-cell"}).text.strip()
        
        #class size
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Average Class Size":
            class_size = row.find('div', {'class': "dt-value-cell"}).text.strip()

        #coed or not
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Student Body Type":
            if not row.find('div', {'class': "dt-value-cell"}).a:
                student_body_type = "Co-Ed"
            else:
                student_body_type = "Not Co-Ed"
        
        #student population
        if row.find('div', {'class': "dt-name-cell"}).text.strip() == "Total Students":
            total_students = row.find('div', {'class': "dt-value-cell"}).text.strip()



    result = (name, type, student_body_type, address, zipcode, number, website, grades, religion, total_students, class_size, adhd_support, learning_difference_support, programs)
    
    return result



def getRandomHeader():
    return HEADERS[random.randint(0, 1)]


def getRandomSleepTime():
    return SLEEP_TIMES[random.randint(0, 3)]
