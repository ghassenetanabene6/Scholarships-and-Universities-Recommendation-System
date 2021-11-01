import os
import requests
from bs4 import BeautifulSoup
import csv

file='data.txt'
error_file='error.txt'
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
create_data_file(error_file)

'''
# Ouverture du site web contenant les bourses et prélévement des liens amenant à chaque description de bourse
Scholarship_link=[] # Liste contenant les liens dans la plateforme studyportals pour accéder à chaque bourse d'étude à USA
for i in range(1,73):
        home="https://www.scholarshipportal.com/scholarships/united-states?page="+str(i)
        response1 = requests.get(home)
        soup = BeautifulSoup(response1.text, 'html.parser')
        Scholarship_link+=soup.find_all('a',{"class": "scholarship scholarship__type--list"})
        print (i, end=' ')
        

Scholarship_link=["https://www.scholarshipportal.com"+s['href'] for s in Scholarship_link]
for link in Scholarship_link:
    append_to_file(file, link)

print("links saved")'''


# Extraction des données de chaque bourse
Names=[] #   Liste contenant tous les noms des bourses d'étude trouvées
SchoLevel=[]    #   Liste contenant le niveau d'étude demandé des bourse
SchoValue=[]    #   Liste contenant les valeurs des bourse
SchoDate=[]     #   Liste contenant les dates limites de l'inscription des bourses
Descriptions=[]     #   Liste contenant les descriptions des bourses
Eligibility=[]      #   Liste contenant les éligibilités des candidats
Benefits=[]
Application=[]
Link=[]
L=[]
i=0
j=0
csv_file=open('data1.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Scholarship Name', 'Level of Study' ,'Scholarship Value','Date', 'Eligibility','Benefits','Application','Descriptions','Link']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()
f = open(file, "r")

for url in  f.readlines():
        response2 = requests.get(url)
        soup = BeautifulSoup(response2.text, 'html.parser')

        try:
            
            # Extraction des noms de chaque bourse
    
            ScholarshipName=soup.find_all('meta',{"name": "og:title"})
            ScholarshipName=[s['content'] for s in ScholarshipName]
            Names.append(ScholarshipName.pop().replace('\n','').replace(',',''))     
        
            # Extraction des niveaux d'étude demandés, des valeurs des bourses, et des dates limites de l'inscription à chaque bourse

            Details= soup.find_all('span',{"class":"u-m-left-20"})
            Details=[s.get_text() for s in Details]
            SchoLevel.append(Details[0].replace('\n','').replace(',',''))
            SchoValue.append(Details[1].replace('\n','').replace(',',''))
            try:
                SchoDate.append(Details[2].replace('\n','').replace(',',''))
            except:
                SchoDate.append(None)
        
        
            # Extraction des descriptions des bourses

            Descript=soup.find_all('div',{"itemprop": "description"})
            Descript=[s.get_text() for s in Descript]
            Descriptions.append(Descript.pop().replace('\u200b','').replace('\n','').replace(',',''))


            # Extraction des liens des bourses

            L=soup.find_all('a',{"class": "btn btn--primary u-m-top-10"})
            L=[s['href'] for s in L]
            if len(L)!=0:
                Link.append(L.pop())
            else: Link.append(None)

            # Extraction des benefits, eligibility et application
        
            h2=soup.find_all('h2')
            div=[]
            for s in h2:
                if s.get_text().lower()=="eligibility":
                    Eligibility.append(s.next_sibling.get_text().replace('\n','').replace(',',''))
                elif s.get_text().lower()=="benefits":
                    Benefits.append(s.next_sibling.get_text().replace('\n','').replace(',',''))
                elif s.get_text().lower()=="application":
                    Application.append(s.next_sibling.get_text().replace('\n','').replace(',',''))

            # insersion des données dans fichier csv
        
            writer.writerow({'Scholarship Name': Names[-1] , 'Level of Study': SchoLevel[-1],'Scholarship Value': SchoValue[-1], 'Date': SchoDate[-1],  'Eligibility': Eligibility[-1], 'Benefits': Benefits[-1], 'Application': Application[-1],'Descriptions': Descriptions[-1],'Link': Link[-1]})

            
            print("inst: "+str((j%15)+1)+"  page: "+str((j//15)+1))
            j+=1
        except:
            j+=1
            print("inst: "+str((j%15)+1)+"  page: "+str((j//15)+1)+"  "+url)
            append_to_file(error_file, url)
        
csv_file.close()
f.close()
