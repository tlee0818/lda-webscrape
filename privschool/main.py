from privschool import scrape

#state should be initials
SCHOOL_CSV = "../csv/privateSchools.csv"
SCHOOL_URL = "https://www.privateschoolreview.com/pennsylvania/special-education-private-schools"
FIELDS = ["Name", "School Type", "Student Body Type", "Address", "Zipcode", "Number", "Website", "Grades Offered", "Religion", "Total Size", "Average Class Size", "ADHD Support", "Learning Different Support", "Learning Difference Programs"]

scrape(SCHOOL_URL, FIELDS, SCHOOL_CSV)