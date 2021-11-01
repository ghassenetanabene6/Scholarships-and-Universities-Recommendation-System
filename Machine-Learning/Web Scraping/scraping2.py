import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

file='data.txt'

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

create_data_file(file)

#Création du fichier csv
csv_file=open('data2.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Scholarship Name', 'Deadline', 'Amount', 'Offered by', 'State','Descriptions','Essay Required','Recommendations Required','Minimum GPA', 'Major', 'Type','Link']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# Ouverture du site web contenant les bourses et extraction des données de chaque bourse
ScholarshipName=[] #   Liste contenant tous les noms des bourses d'étude trouvées
Link=[] # Liste contenant les liens pour inscription
Offered_by=[]    #   Liste contenant l'univeristé ou l'organisme
Amount=[]    #   Liste contenant les valeurs des bourse
Deadline=[]     #   Liste contenant les dates limites de l'inscription des bourses
Description=[]     #   Liste contenant les descriptions des bourses
State=[]      #   Liste contenant les pays
Major=[]
Type=[]
Essay_Required=[]
Recommendations_Required=[]
Minimum_GPA=[]


for i in range(1,4):
    url="https://www.niche.com/colleges/scholarships/?page="+str(i)
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    Scholarship=soup.find_all('a',{"class": "scholarship-search-result__title"})

    ScholarshipName+=[s.get_text().replace(',','').strip() for s in Scholarship]
    Link+=[s['href'].replace(',','').strip() for s in Scholarship]

    header=soup.find_all('div',{"class": "scholarship-search-result__header-fact-value"})
    for l in header:
        if (l.previous_sibling.get_text()=="Deadline"):
            Deadline.append(l.get_text().replace(',','').strip())
        else: Amount.append(l.get_text().replace(',','').strip())


        
    Details=soup.find_all('div',{"class": "scholarship-search-result__details-fact-value"})
    for l in Details:
        if (l.previous_sibling.get_text()=="Offered By"):
            Offered_by.append(l.get_text().replace(',','').strip())
        if (l.previous_sibling.get_text()=="State"):
            State.append(l.get_text().replace(',','').strip())
        if (l.previous_sibling.get_text()=="Description"):
            Description.append(l.get_text().replace(',','').strip())
        if (l.previous_sibling.get_text()=="Major"):
            Major.append(l.get_text().replace(',','').strip())
        if (l.previous_sibling.get_text()=="Type"):
            Type.append(l.get_text().replace(',','').strip())
            
        
    Requirements=soup.find_all('ol',{"class": "scholarship-search-result__requirements"})
    for l in Requirements:
        a=l.find_all('li')
        Essay_Required.append(a[0].span.get_text().replace(',','').strip())
        Recommendations_Required.append(a[1].span.get_text().replace(',','').strip())
        Minimum_GPA.append(a[2].span.get_text().replace(',','').strip())
    

# insersion des données dans fichier csv
for i in range(len(ScholarshipName)):
    writer.writerow({'Scholarship Name': ScholarshipName[i] , 'Deadline': Deadline[i],'Amount': Amount[i], 'Offered by': Offered_by[i],  'State': State[i], 'Descriptions': Description[i], 'Essay Required': Essay_Required[i],'Recommendations Required': Recommendations_Required[i],'Minimum GPA': Minimum_GPA[i],'Major': Major[i],'Type': Type[i],'Link': Link[i]})

csv_file.close()




