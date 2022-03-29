from psychotoday import scrape
import csv

PYSCHO_THERAPIST_PITTSBURGH_CSV_FILE = "csv/psychoTherapistCSV.csv"
PSYCHO_URL_THERAPIST_PITTSBURGH = "https://www.psychologytoday.com/us/therapists/learning-disabilities/pa/pittsburgh?sid=622fce7cebe9b&ref="

PSYCHO_URL_THERAPIST_PENN = "https://www.psychologytoday.com/us/therapists/pennsylvania?category=learning-disabilities&sid=624219fe2027b&ref="
PYSCHO_THERAPIST_PENN_CSV_FILE = "csv/psychoTherapistPennCSV.csv"

PYSCHO_PSYCHIATRIST_PENN_CSV_FILE = "csv/psychoPsychiatristCSV.csv"
PYSCHO_URL_PSYCHIATRIST_PENN = "https://www.psychologytoday.com/us/psychiatrists/pennsylvania?sid=62390f910804f&ref="

FIELDS = ["Name", "Issues", "Services", "Age Groups", "Years in Practice", "License", "Recent School", "Graduation Year", "Certificate", "Certificate Date", "Cost per Session", "Sliding Scale", "Insurances", "Website", "Phone Number", "Street Address", "City/State", "Zipcode"]
psycho_therapist_info = scrape(PSYCHO_URL_THERAPIST_PENN, FIELDS, PYSCHO_THERAPIST_PENN_CSV_FILE)

"""with open(PYSCHO_THERAPIST_PENN_CSV_FILE, 'w', newline = '') as l:

    writer = csv.writer(l)

    writer.writerow(FIELDS)
    for row in psycho_therapist_info:
        writer.writerow(list(row))"""

psycho_psychiatrist_info = scrape(PYSCHO_URL_PSYCHIATRIST_PENN, FIELDS, PYSCHO_PSYCHIATRIST_PENN_CSV_FILE)

"""with open(PYSCHO_PSYCHIATRIST_PENN_CSV_FILE, 'w', newline = '') as l:

    writer = csv.writer(l)

    writer.writerow(FIELDS)
    for row in psycho_psychiatrist_info:
        writer.writerow(list(row))"""
