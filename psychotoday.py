import requests
from urllib import request
import time
import bs4
from bs4 import BeautifulSoup
import ssl
import csv
import random

ssl._create_default_https_context = ssl._create_unverified_context


#creating multiple user agents and sleeptimes to avoid bot detection
HEADERS = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'},
{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}]
SLEEP_TIMES = [0.5, 0.7, 1, 1.2]

def scrape(url, fields, outfile):
    info = []
    pageNum = 0

    #clicks on the right arrow key in the pagination area
    nextPage = requests.get(url + f"{pageNum * 20 + 1}", headers= getRandomHeader())
    with open(outfile, 'w', newline = '') as l:
        writer = csv.writer(l)
        writer.writerow(fields)
        while True:

            psycho_soup = BeautifulSoup(nextPage.text, "html.parser")

            # get all cards for therapists (or psychiatrists)
            therapists = psycho_soup.find(class_ = 'results')

            for therapist in therapists.children:
                time.sleep(getRandomSleepTime())  # bot detection

                if therapist and therapist.name == "div" and therapist.has_attr('data-x'):
                    #append therapist info from get_therapist_info()
                    info.append(get_therapist_info(therapist.a["href"]))
                    writer.writerow(list(info[-1]))
                    print(info[-1])

            #if right arrow key does not exist, we have reached the end. else, get next page
            if psycho_soup.find("span", {"class": "chevron-right"}):
                pageNum += 1
                nextPage = requests.get(url + f"{pageNum * 20 + 1}", headers= getRandomHeader())
                print(f"_______________________NEW PAGE {pageNum}_______________________")
            else:
                break
        
    return info

#for fields we can't find
EMPTY = "N/A"
#card = link of the therapist page
def get_therapist_info(card):

    card_soup = BeautifulSoup(requests.get(card, headers= getRandomHeader()).text, "html.parser")

    name = card_soup.find('h1', {'itemprop': 'name'}).text

    number_tab = card_soup.find('a', {'id': 'phone-click-reveal'})
    number = "".join(filter(lambda x: x.isnumeric(), list(number_tab.text.strip()))) if number_tab else EMPTY
    number = number[:11]

    street = EMPTY
    citystate = EMPTY
    postalcode = EMPTY
    addy_soup = card_soup.find("div", {"class": "address-data"})
    if addy_soup:
        #street
        street = addy_soup.find("span", {"itemprop": "streetAddress"}).text.strip() if addy_soup.find("span", {"itemprop": "streetAddress"}) else EMPTY

        #citystate
        if addy_soup.find("span", {"itemprop": "addressLocality"}) and addy_soup.find("span", {"itemprop": "addressRegion"}):
            citystate = addy_soup.find("span", {"itemprop": "addressLocality"}).text.strip() + " " + addy_soup.find("span", {"itemprop": "addressRegion"}).text.strip()
        elif addy_soup.find("span", {"itemprop": "addressLocality"}):
            citystate = addy_soup.find("span", {"itemprop": "addressLocality"}).text.strip()
        elif addy_soup.find("span", {"itemprop": "addressRegion"}):
            citystate = addy_soup.find("span", {"itemprop": "addressRegion"}).text.strip()

        #postalcode
        postalcode = addy_soup.find("span", {"itemprop": "postalcode"}).text.strip() if addy_soup.find("span", {"itemprop": "postalcode"}) else EMPTY

    #not elegant, but not all therapists have services/issues in their respective tabs. rather, some of them just have it in their bios.
    
    services = []
    issues = []
    services.append("Counseling")
    if card_soup.find_all(text=lambda x: x and ("evaluation" in x or "Evaluation" in x or "testing" in x or "Testing" in x)):
        services.append("Testing and Evaluation")
    
    #All of them should at serve for LD
    issues.append("Learning Disabilities")
    if card_soup.find_all(text=lambda x: x and "ADHD" in x):
        issues.append("ADHD")
    if card_soup.find_all(text=lambda x: x and ("dysgraphia" in x or "Dysgraphia" in x)):
        issues.append("Dysgraphia")

    #show age groups as show in psychotoday
    age_groups = []
    age_tab = card_soup.find('div', {'class': 'attributes-age-focus'})
    if age_tab and age_tab.find('ul', {'class': 'attribute-list'}).children:
        age_tab = age_tab.find('ul', {'class': 'attribute-list'}).children
        for age in age_tab:
            age_groups.append(age.text.strip())

        age_groups = ", ".join(filter(lambda x: x,(age_groups)))

    else:
        age_groups = EMPTY


    finance_tab = card_soup.find('div', {'id': 'tabs-finances-office'})
    cost = EMPTY
    sliding_scale = EMPTY
    insurances_list = []
    #if insurance info could not be found, label it empty
    insurances = EMPTY
    if finance_tab:
        cost_tab = finance_tab.find(class_ = "finances-office")
        if cost_tab and cost_tab.ul and cost_tab.ul.li:
            for info in cost_tab.ul:
                if info and isinstance(info, bs4.element.Tag) and info.strong:
                    category = info.strong.text
                    unwanted = info.find('strong')  
                    unwanted.extract()

                    if category == "Cost per Session:":
                        cost = info.text.strip()
                    elif category == "Sliding Scale:":
                        sliding_scale = info.text.strip()

        insurance_tab = finance_tab.find(class_="attributes-insurance")
        if insurance_tab and insurance_tab.ul and insurance_tab.ul.li:
            for insurance in insurance_tab.ul:
                if insurance and isinstance(insurance, bs4.element.Tag):
                    insurances_list.append(insurance.text.strip())
            
            insurances = ", ".join(filter(lambda x: x,(insurances_list)))



    
    profile_tab = card_soup.find('div', {'class': 'profile-buttons'})
    website = card
    if profile_tab:
        website_button = profile_tab.find('a', {'data-event-label': 'website'})
        if website_button:
            #website urls are redirects. need to access the link and find the original website
            redirect_url = website_button["href"]
            redirect_request = request.Request(redirect_url)
            redirect_request.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
            try:
                response = request.urlopen(redirect_request)
                website = response.geturl()
            except Exception as e:
                website = e

    qualifications_tab = card_soup.find('div', {'class': 'profile-qualifications'})
    years_in_practice = EMPTY
    license = EMPTY
    school = EMPTY
    grad_year = EMPTY
    if qualifications_tab and qualifications_tab.ul:
        for quals in qualifications_tab.ul:
            if quals and isinstance(quals, bs4.element.Tag) and quals.strong:
  
                category = quals.strong.text
                unwanted = quals.find('strong')  
                unwanted.extract()

                if category == "Years in Practice:":
                    years_in_practice = quals.text.strip()
                elif category == "License:":
                    license = " ".join(quals.text.split())
                elif category == "School:":
                    school = quals.text.strip()
                elif category == "Year Graduated:":
                    grad_year = quals.text.strip()

    credentials_tab = card_soup.find('div', {'class': 'profile-additional-credentials'})
    certificate = EMPTY
    date = EMPTY
    if credentials_tab and credentials_tab.ul:
        for cert in credentials_tab.ul:
            if cert and isinstance(cert, bs4.element.Tag) and cert.strong:
                category = cert.strong.text
                unwanted = cert.find('strong')  
                unwanted.extract()

                if category == "Certificate:":
                    certificate = cert.text.strip()
                elif category == "Certificate Date:":
                    date = cert.text.strip()

    return (name, ", ".join(issues), ", ".join(services), age_groups, years_in_practice, license, school, grad_year, certificate, date, cost, sliding_scale, insurances, website, number, street, citystate, postalcode)

def getRandomHeader():
    return HEADERS[random.randint(0,1)]

def getRandomSleepTime():
    return SLEEP_TIMES[random.randint(0,3)]