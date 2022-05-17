from unicodedata import name
import requests
import ast
import csv

def scrape(url, state, outfile, fields):

    result = []
    
    r = requests.get(url)
    tutors = ast.literal_eval(r.content.decode('utf-8-sig'))

    print("got all tutors")
    for tutor in tutors:
        if tutor['state'] != state:
            continue
        
        name = tutor['name']
        email = tutor['email']
        city = tutor['city']
        zipcode = tutor['zip']

        toAdd = (name, email, city, zipcode)

        result.append(toAdd)

    print("filtered to specific state")

    write_tutors(result, outfile, fields)

    print(len(result))
    return result

def write_tutors(result, outfile, fields):

    with open(outfile, 'w', newline = '') as l:
        writer = csv.writer(l)
        writer.writerow(fields)
        
        for line in result:
            writer.writerow(list(line))