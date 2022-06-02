from lawyers import scrape

PENN_LAWYERS_CSV = "../csv/lawyersPENN.csv"
URL = "https://www.lawyers.com/americans-with-disabilities-act/all-cities/pennsylvania/law-firms/"
FIELDS = ["Name", "Issues", "Services", "Age Groups", "Years in Practice", "License", "Recent School", "Graduation Year", "Certificate", "Certificate Date", "Cost per Session", "Sliding Scale", "Insurances", "Website", "Phone Number", "Street Address", "City/State", "Zipcode"]

scrape(PENN_LAWYERS_CSV, FIELDS, URL)
