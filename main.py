from psychotoday import scrape
import csv

PYSCHO_CSV_FILE = "csv/psychoCSV.csv"
PSYCHO_URL = "https://www.psychologytoday.com/us/therapists/learning-disabilities/pa/pittsburgh?sid=622fce7cebe9b&ref="

info = scrape(PSYCHO_URL)

with open(PYSCHO_CSV_FILE, 'w', newline = '') as l:

    writer = csv.writer(l)

    for row in info:
        writer.writerow(list(row))

