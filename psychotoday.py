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

    services = []
    service_tab = card_soup.find('ul', {'class': 'attribute-list specialties-list'}).children
    if service_tab:
        for service in service_tab:
            services.append(service.text.strip())

        services_string = ", ".join(filter(lambda x: x,(services)))

    else:
        services = "See Website"

    finance_tab = card_soup.find('div', {'id': 'tabs-finances-office'})
    if finance_tab:
        cost_tab = finance_tab.find(class_ = "finances-office")
        if cost_tab and cost_tab.ul and cost_tab.ul.li:
            price = cost_tab.ul.li.text.strip()
        else:
            price = "See Website"
    else:
        price = "See Website"
    
    website = card

    return (name, services_string, price, website, number, " ".join(address))