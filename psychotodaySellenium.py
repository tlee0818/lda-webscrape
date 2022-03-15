import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape(url):
    info = []
    driver = webdriver.Chrome("chromeDriver")
    driver.get(url)
    print(driver)
    while True:
        time.sleep(1)  # added a 1 second sleep to limit bot detection
        psycho_soup = BeautifulSoup(driver.page_source, "lxml")

        # get all cards
        therapists = psycho_soup.find(class_ = 'results')
        for therapist in therapists.children:
            if therapist and therapist.name == "div" and therapist.has_attr('data-x'):
                print(therapist.a)
                info.append(get_therapist_info(therapist.a["href"]))
                print(info[-1])
        
        buttons = psycho_soup.find(class_ = 'button-element arrow-btn page-btn')

        if len(buttons) < 2:
            break
        else:
            nextPageLink = buttons[1]["href"]
            nextPage = requests.get(nextPageLink)
        
    return info

def get_therapist_info(card):
    card_soup = BeautifulSoup(requests.get(card).text, "html_parser")

    name = card_soup.findAll('h1', {'itemprop': 'name'})
    number = "".join(filter(lambda x: x.isnumber,list(card_soup.findAll(id_ = 'phone-click-reveal'))))
    street_addy = card_soup.find(itemprop_= "streetAddress").text
    city = card_soup.find(itemprop_= "addressLocality").text[:-1]
    state = card_soup.find(itemprop_= "addressRegion").text[:-1]
    zipcode = card_soup.find(itemprop_= "postalcode").text[:-1]
    services = []
    for service in card_soup.findAll(class_ = 'spec-list attributes-treatment-orientation').div.ul:
        services.append(service.text.strip())
    services = ", ".join(services[:-1])
    services += services[-1]
    price = card_soup.findAll(class_ = 'finances-office').ul.li.text
    website = card

    return (name, services, price, website, number, street_addy, city, state, zipcode)