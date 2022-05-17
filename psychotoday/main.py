from psychotoday import scrape

PYSCHO_THERAPIST_PENN_CSV_FILE = "csv/psychoTherapistPennCSV.csv"
PSYCHO_THERAPIST_PENN_URL = "https://www.psychologytoday.com/us/therapists/pennsylvania?category=learning-disabilities&sid=624219fe2027b&ref="

PYSCHO_PSYCHIATRIST_PENN_CSV_FILE = "csv/psychoPsychiatristCSV.csv"
PYSCHO_PSYCHIATRIST_PENN_URL = "https://www.psychologytoday.com/us/psychiatrists/pennsylvania?sid=62390f910804f&ref="

FIELDS = ["Name", "Issues", "Services", "Age Groups", "Years in Practice", "License", "Recent School", "Graduation Year", "Certificate", "Certificate Date", "Cost per Session", "Sliding Scale", "Insurances", "Website", "Phone Number", "Street Address", "City/State", "Zipcode"]

scrape(PSYCHO_THERAPIST_PENN_URL, FIELDS, PYSCHO_THERAPIST_PENN_CSV_FILE)
scrape(PYSCHO_PSYCHIATRIST_PENN_URL, FIELDS, PYSCHO_PSYCHIATRIST_PENN_CSV_FILE)
