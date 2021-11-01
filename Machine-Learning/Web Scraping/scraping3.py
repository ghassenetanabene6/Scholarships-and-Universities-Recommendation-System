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
csv_file=open('data3.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Scholarship Name', 'Deadline', 'Offered by', 'Level','Description','Link']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# Ouverture du site web contenant les bourses et extraction des données de chaque bourse
ScholarshipName=[] #   Liste contenant tous les noms des bourses d'étude trouvées
Scholarship_link=[] # Liste contenant les liens pour inscription
Offered_by=[]    #   Liste contenant l'univeristé ou l'organisme
Deadline=[]     #   Liste contenant les dates limites de l'inscription dess bourses
Description=[]     #   Liste contenant les descriptions des bourses
Level=[]        # Liste contenat le niveau d'etude
Link=[]

url="https://www.afterschoolafrica.com/7110/"
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')
Scholarship=soup.find_all('h3')[:-3]
for l in Scholarship:
    ScholarshipName.append(l.get_text().replace(',',''))
    t1=0
    t2=0
    Desc=""
    Lev=""
    Dead=""
    a=l
    while(1):
        a=a.next_sibling
        if ("level of study" in a.get_text().lower() or "eligible field of study" in a.get_text().lower()):
            Lev+=a.get_text().replace(';','').replace(',','').replace("Level of Study:","").replace("Level of study:","").replace("Eligible Field of Study","").replace(':','').strip()
            t1=1
        elif ("application deadline" in a.get_text().lower() or "application starts" in a.get_text().lower()):
            Dead+=a.get_text().replace(';','').replace(',','').replace("Previous Application Deadline:","").replace("Previous Application deadline:","").replace("Application Deadline","").replace(':','').strip()
            t2=1
        elif (a.find("a")):
            if ("scholarship page" in a.get_text().lower() or "scholarship form" in a.get_text().lower()):
                Link.append(a.find("a")['href'])
                if(t1==0):
                    Lev=None
                if(t2==0):
                    Dead=None
                break
        else:
            if(t1==1 and t2==0):
                Lev+=a.get_text().replace(';','').replace(':','').strip()
            if(t1==1 and t2==1):
                Dead+=a.get_text().replace("Application Deadline","").replace(';','').replace(':','').strip()
            if(t1==0 and t2==0):
                Desc+=a.get_text()
    Description.append(Desc.replace(',','').replace(';','').strip())
    Level.append(Lev)
    Deadline.append(Dead)


#insersion des données dans fichier csv
for i in range(len(ScholarshipName)):
    writer.writerow({'Scholarship Name': ScholarshipName[i] , 'Deadline': Deadline[i],'Offered by': None,  'Level': Level[i], 'Description': Description[i], 'Link': Link[i]})

csv_file.close()




