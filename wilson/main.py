from wilson import scrape

#state should be initials
STATE = "PA"
WILSON_CSV = f"../csv/wilsonTutors{STATE}.csv"
WILSON_URL = "https://wilsonacademypublic.blob.core.windows.net/public/tutor/Tutors.json.gz"
FIELDS = ["Name", "Email", "City", "Zipcode"]

scrape(WILSON_URL, STATE, WILSON_CSV, FIELDS)