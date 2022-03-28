import csv

def find_duplicates(inFile, outFile, fields):
    clean = []
    seen = set()
    with open(inFile, newline = '') as l:

        reader = csv.reader(l)
        print(f"total count: {len(reader)}")
        for row in reader:
            #identify by name, license, phone number, zipcode
            identifier = ",".join([row[0], row[5], row[14], row[17]])

            if identifier in seen:
                continue
            else:
                seen.add(identifier)
                clean.append(row)
        
        print(f"unique count: {len(seen)}")
    
    with open(outFile, 'w', newline = '') as l:

        writer = csv.writer(l)

        writer.writerow(fields)
        for row in clean:
            writer.writerow(list(row))