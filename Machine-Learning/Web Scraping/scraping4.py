import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv


def create_data_file(file):
    if not os.path.isfile(file):
        write_file(file,'')

# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

# Add data into an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


#Création du fichier csv
csv_file=open('data4.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Scholarship Name', 'Deadline', 'Amount', 'Offered by', 'Eligibility','Description','Link']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# Ouverture du site web contenant les bourses et extraction des données de chaque bourse
ScholarshipName=[] #   Liste contenant tous les noms des bourses d'étude trouvées
Link=[] # Liste contenant les liens pour inscription
Amount=[]    #   Liste contenant les valeurs des bourse
Deadline=[]     #   Liste contenant les dates limites de l'inscription des bourses
Description=[]     #   Liste contenant les descriptions des bourses
Eligibility=[]      #   Liste contenant les pays



url="https://www.affordablecolleges.com/resources/scholarships-for-international-students/"
req = Request(url)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')
Scholarship=soup.find_all('h4',{"class": "title js-toggle"})
Amount=[s.find('span') for s in Scholarship]
ScholarshipName=[s.previous_sibling.replace(',','').strip() for s in Amount]
Amount=[s.get_text().replace(',','').strip() for s in Amount]
Link=soup.find_all('a',{"class": "btn-tertiary"})
Link=[s['href'] for s in Link]
Details=soup.find_all('div',{"class": "content"})
for i in Details:
    Description.append(i.find('p').previous_sibling.replace(',','').replace('\n','').strip())
    Eligibility+=i.find_all('ul')
    a=i.find_all('p')
    for x in a:
        if("scholarship deadline" in x.get_text().lower()):
            Deadline.append(x.find('strong').next_sibling.replace(',','').strip())
Eligibility=[s.get_text().replace(',','').replace('\n','').strip() for s in Eligibility]
Description=[x if x!='' else None for x in Description]


# Insersion des données dans fichier csv
for i in range(len(ScholarshipName)):
    writer.writerow({'Scholarship Name': ScholarshipName[i] , 'Deadline': Deadline[i],'Amount': Amount[i], 'Offered by': None,'Eligibility': Eligibility[i],'Description': Description[i],'Link': Link[i]})

csv_file.close()




