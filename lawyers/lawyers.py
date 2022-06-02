import requests
import random
import pandas as pd
import numpy as np
import string



# creating multiple user agents and sleeptimes to avoid bot detection
HEADERS = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}]
SLEEP_TIMES = [0.5, 0.7, 1, 1.2]
AUTH = {"authorization": "Bearer 8mw0vs7ziibql03va7lf1bf4l"}

ADDY_BASS_URL = ""


def organize_data(url):

    print(f"CALLING AVVO API FOR ...{url[-35:-15]}")

    pageNum = 1

    master_df = pd.DataFrame([])
    r = requests.get(url + str(pageNum), headers = AUTH)

    maxPage = r.json()["meta"]["total_pages"]


    while(pageNum <= maxPage):
        print(f"page {pageNum} OUT OF {maxPage}")
        r = requests.get(url + str(pageNum), headers = getRandomHeader())

        lawyers = r.json()["lawyers"]

        if not lawyers:
            break

        this_df = pd.DataFrame(lawyers)

        if master_df.empty:
            master_df = this_df
        else:
            master_df = master_df.append(this_df, ignore_index=True)

        pageNum += 1

    print("getting rid of duplicates")
    master_df = master_df.drop_duplicates(subset=['id'])

    print("annotating disabilities")
    master_df = annotate_disability(master_df)
    
    print("formatting specialties and links")
    master_df = format_specialties(master_df)
    master_df = format_links(master_df)

    print("finding addresses")
    master_df = add_addy(master_df)
    master_df = delete_non_penn_lawyers(master_df)


    print("dropping duplicates again and unnecessary columns")
    master_df = master_df.drop_duplicates(subset=['id'])
    master_df = drop_columns(master_df)

    
    return master_df

def format_specialties(df):

    df["lawyer_specialties"] = format_specialties_helper(df["lawyer_specialties"])

    return df

def format_specialties_helper(rows):
    simplified = []

    for row in rows:

        this_specs = []

        for spec in row:
            if spec['name'] == "Social Security":
                this_specs.append("Social Security & Disability")
            else:
                this_specs.append(spec['name'])

        simplified.append(",".join(this_specs))

    return simplified

def format_links(df):

    profiles, contacts = format_links_helper(df["browse_links"])

    df['profile'] = profiles.tolist()
    df['contact'] = contacts.tolist()

    return df



def format_links_helper(rows):
    profiles = []
    contacts = []

    for row in rows:

        this_profile = "N/A"
        this_contact = "N/A"
        for link in row:
            if link['type'] == "profile":
                this_profile = link['url']
            if link['type'] == "contact":
                this_contact = link['url']

        profiles.append(this_profile)
        contacts.append(this_contact)

    return np.array(profiles), np.array(contacts)

def add_addy(df):
    
    lawyer_ids = df["id"].tolist()

    df["street"] = ""
    df["city"] = ""
    df["zipcode"] = ""

    df["alt_street"] = ""
    df["alt_city"] = ""
    df["alt_zipcode"] = ""

    

    for i in range(0, len(lawyer_ids)-2, 2):
        chunk = ",".join(list(map(str, lawyer_ids[i:i+2])))
        r = requests.get("https://api.avvo.com/api/4/lawyer_addresses.json", params={"lawyer_ids": chunk}, headers = getRandomHeader())
        addys = r.json()["lawyer_addresses"]
        df = add_addy_helper(df, addys)

    return df

def add_addy_helper(df, addys):

    for addy in addys:

        lawyer = addy["lawyer_id"]

        if addy["state_code"] != "PA":
            continue

        street = addy["line1"]

        if addy["line2"]:
            street += " " + addy["line2"]

        if not df.loc[df.id == lawyer]["street"].item() or df.loc[df.id == lawyer]["street"].item() == "" or (df.loc[df.id == lawyer]["street"].item()).isspace():
            df.loc[df.id == lawyer, ["street", "city", "zipcode"]] = street, addy["city"], addy["postal_code"]
        else:
            df.loc[df.id == lawyer, ["alt_street", "alt_city", "alt_zipcode"]] = street, addy["city"], addy["postal_code"]

    return df

def annotate_disability(df):
    df["mentions_disability?"] = annotate_disability_helper(df["bio"])

    return df

def annotate_disability_helper(rows):

    result = []

    for row in rows:
        
        if not row:
            result.append("No")
            continue

        bio = row.lower()

        if "disab" in bio:
            result.append("Yes")
        else:
            result.append("No")

    return result

def delete_non_penn_lawyers(df):
    df = df.drop(df[df.street == ""].index)

    return df

def drop_columns(df):
    return df.drop(['suffix', 'aliases', 'avvo_pro', 'bio', 'avvo_rating', 'client_review_count', 'client_review_score', 'avvo_rating', 'bio', 'browse_links'], axis=1)

#for fields we can't find
EMPTY = "N/A"

def getRandomHeader():
    to_return = HEADERS[random.randint(0, 1)]
    to_return.update(AUTH)
    return to_return


def getRandomSleepTime():
    return SLEEP_TIMES[random.randint(0, 3)]
