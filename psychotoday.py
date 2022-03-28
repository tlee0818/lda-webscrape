import requests
from urllib import request
import time
import bs4
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

def scrape(url):
    info = []
    pageNum = 0
    nextPage = requests.get(url + f"{pageNum * 20 + 1}", headers= HEADER)
    while True:
        time.sleep(0.5)  # added a 1 second sleep to limit bot detection

        psycho_soup = BeautifulSoup(nextPage.text, "html.parser")

        # get all cards
        therapists = psycho_soup.find(class_ = 'results')

        for therapist in therapists.children:
            if therapist and therapist.name == "div" and therapist.has_attr('data-x'):
                info.append(get_therapist_info(therapist.a["href"]))
                print(info[-1])

        if psycho_soup.find("span", {"class": "chevron-right"}):
            pageNum += 1
            nextPage = requests.get(url + f"{pageNum * 20 + 1}", headers= HEADER)
            print("_______________________NEW PAGE_______________________")
        else:
            break
        
    return info

def get_therapist_info(card):
    card_soup = BeautifulSoup(requests.get(card, headers= HEADER).text, "html.parser")

    name = card_soup.find('h1', {'itemprop': 'name'}).text

    number_tab = card_soup.find('a', {'id': 'phone-click-reveal'})

    number = "".join(filter(lambda x: x.isnumeric(), list(number_tab.text.strip()))) if number_tab else "See Website"
    number = number[:11]

    street = "N/A"
    citystate = "N/A"
    postalcode = "N/A"
    addy_soup = card_soup.find("div", {"class": "address-data"})
    if addy_soup:
        #street
        street = addy_soup.find("span", {"itemprop": "streetAddress"}).text.strip() if addy_soup.find("span", {"itemprop": "streetAddress"}) else "N/A"

        #citystate
        if addy_soup.find("span", {"itemprop": "addressLocality"}) and addy_soup.find("span", {"itemprop": "addressRegion"}):
            citystate = addy_soup.find("span", {"itemprop": "addressLocality"}).text.strip() + " " + addy_soup.find("span", {"itemprop": "addressRegion"}).text.strip()
        elif addy_soup.find("span", {"itemprop": "addressLocality"}):
            citystate = addy_soup.find("span", {"itemprop": "addressLocality"}).text.strip()
        elif addy_soup.find("span", {"itemprop": "addressRegion"}):
            citystate = addy_soup.find("span", {"itemprop": "addressRegion"}).text.strip()

        #postalcode
        postalcode = addy_soup.find("span", {"itemprop": "postalcode"}).text.strip() if addy_soup.find("span", {"itemprop": "postalcode"}) else "N/A"

    #not elegant, but not all therapists have services/issues in their respective tabs. rather, some of them just have it in their bios
    services = []
    issues = []
    if card_soup.find_all(text=lambda x: x and ("counseling" in x or "Counseling" in x or "testing" in x or "Testing" in x)):
        services.append("Counseling")
    if card_soup.find_all(text=lambda x: x and ("evaluation" in x or "Evaluation" in x or "testing" in x or "Testing" in x)):
        services.append("Testing and Evaluation")
    

    if card_soup.find_all(text=lambda x: x and "Learning Disabilities" in x):
        issues.append("Learning Disabilities")
    if card_soup.find_all(text=lambda x: x and "ADHD" in x):
        issues.append("ADHD")
    if card_soup.find_all(text=lambda x: x and ("dysgraphia" in x or "Dysgraphia" in x)):
        issues.append("Dysgraphia")

    age_groups = []
    age_tab = card_soup.find('div', {'class': 'attributes-age-focus'})
    if age_tab and age_tab.find('ul', {'class': 'attribute-list'}).children:
        age_tab = age_tab.find('ul', {'class': 'attribute-list'}).children
        for age in age_tab:
            age_groups.append(age.text.strip())

        age_groups = ", ".join(filter(lambda x: x,(age_groups)))

    else:
        age_groups = "N/A"


    finance_tab = card_soup.find('div', {'id': 'tabs-finances-office'})
    cost = "N/A"
    sliding_scale = "N/A"
    insurances_list = []
    insurances = "N/A"
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
            redirect_url = website_button["href"]
            redirect_request = request.Request(redirect_url)
            redirect_request.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
            try:
                response = request.urlopen(redirect_request)
                website = response.geturl()
            except Exception as e:
                website = e

    qualifications_tab = card_soup.find('div', {'class': 'profile-qualifications'})
    years_in_practice = "N/A"
    license = "N/A"
    school = "N/A"
    grad_year = "N/A"
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
    certificate = "N/A"
    date = "N/A"
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