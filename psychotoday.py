import requests
import time
import bs4
from bs4 import BeautifulSoup

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

def scrape(url):
    info = []
    pageNum = 0
    nextPage = requests.get(url + f"{pageNum * 20 + 1}", headers= HEADER)
    while True:
        time.sleep(1)  # added a 1 second sleep to limit bot detection

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
    
    address = []
    for addy_part in card_soup.find("div", {"class": "address-data"}).children:
        if addy_part and isinstance(addy_part, bs4.element.Tag) and addy_part.text and addy_part.has_attr("itemprop"):
            address.append(addy_part.text.strip())

    issues = []
    issues_tab = card_soup.find('div', {'class': 'attributes-issues'}).find('ul', {'class': 'attribute-list'}).children
    if issues_tab:
        for issue in issues_tab:
            if issue.text.strip() == "ADHD" or issue.text.strip() == "Testing and Evaluation" or issue.text.strip() == "Learning Disabilities":
                issues.append(issue.text.strip())

        issues = ", ".join(filter(lambda x: x,(issues)))

    else:
        issues = "N/A"

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
    if profile_tab:
        website_button = card_soup.find('a', {'data-event-label': 'website'})
        if website_button:
            website = website_button.href
        else:
            website = "N/A"
    else:
        website = "N/A"

    qualifications_tab = card_soup.find('div', {'class': 'profile-qualifications'})
    years_in_practice = "N/A"
    license = "N/A"
    school = "N/A"
    grad_year = "N/A"
    if qualifications_tab and qualifications_tab.children and list(qualifications_tab.children)[1].ul:
        qualifications_tab = list(qualifications_tab.children)[1].ul
        for quals in qualifications_tab:
            if quals and isinstance(quals, bs4.element.Tag) and quals.strong:
                category = quals.strong.text
                unwanted = quals.find('strong')  
                unwanted.extract()

                if category == "Years in Practice:":
                    years_in_practice = quals.text.strip()
                elif category == "License:":
                    license = quals.text.strip()
                elif category == "School":
                    school = quals.text.strip()
                elif category == "Year Graduated:":
                    grad_year = quals.text.strip()

    credentials_tab = card_soup.find('div', {'class': 'profile-additional-credentials'})
    certificate = "N/A"
    date = "N/A"
    if credentials_tab and credentials_tab.children and list(credentials_tab.children)[1].ul:
        credentials_tab = list(credentials_tab.children)[1].ul
        for cert in credentials_tab:
            if cert and isinstance(cert, bs4.element.Tag) and cert.strong:
                category = cert.strong.text
                unwanted = cert.find('strong')  
                unwanted.extract()

                if category == "Certificate:":
                    certificate = cert.text.strip()
                elif category == "Certificate Date:":
                    date = cert.text.strip()

    
    return (name, issues, age_groups, years_in_practice, license, school, grad_year, certificate, date, cost, sliding_scale, insurances, website, number, " ".join(address))