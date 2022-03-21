from psychotoday import scrape
import csv

PYSCHO_CSV_FILE = "csv/psychoCSV.csv"
PSYCHO_URL = "https://www.psychologytoday.com/us/therapists/learning-disabilities/pa/pittsburgh?sid=622fce7cebe9b&ref="

info = scrape(PSYCHO_URL)

with open(PYSCHO_CSV_FILE, 'w', newline = '') as l:

    writer = csv.writer(l)

    writer.writerow(["Name", "Issues", "Age Groups", "Years in Practice", "License", "Recent School", "Graduation Year", "Certificate", "Certificate Date", "Cost per Session", "Sliding Scale", "Insurances", "Website", "Phone Number", "Address"])
    for row in info:
        writer.writerow(list(row))

