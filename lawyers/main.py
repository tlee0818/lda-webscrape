import lawyers as l

PENN_LAWYERS_CSV = "../csv/lawyersPENN.csv"
SSD_URL = "https://api.avvo.com/api/4/lawyers/search.json?loc=Pennsylvania&q=Social Security&per_page=50&page="
DISC_URL = "https://api.avvo.com/api/4/lawyers/search.json?loc=Pennsylvania&q=Discrimination&per_page=50&page="

FIELDS = ["Name", "Issues", "Services", "Age Groups", "Years in Practice", "License", "Recent School", "Graduation Year", "Certificate", "Certificate Date", "Cost per Session", "Sliding Scale", "Insurances", "Website", "Phone Number", "Street Address", "City/State", "Zipcode"]

if __name__ == '__main__':
    ssd_res = l.organize_data(SSD_URL)
    disc_res = l.organize_data(DISC_URL)

    ssd_res = ssd_res.append(disc_res, ignore_index=True)
    master_df = ssd_res

    print("getting rid of duplicates one last time")
    master_df = master_df.drop_duplicates(subset=['id'])

    master_df = master_df.drop(['id'], axis=1)

    master_df.to_csv(PENN_LAWYERS_CSV, index=False)
