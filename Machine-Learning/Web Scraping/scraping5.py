import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd



#Création du fichier csv
csv_file=open('data5.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Rank', 'University', 'Location', 'Description', 'Link']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# Ouverture du site web contenant les bourses et extraction des données de chaque bourse
University=[] #   Liste contenant tous les noms universités
Rank=[] # Liste contenant le classement de l'université
Location=[]    #   Liste contenant la localisation de l'université
Link=[]
Description=[]


url="https://www.4icu.org/us/"
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

Rows=soup.find_all('td')
for l in Rows:
    if l.attrs:
        pass
    else:
        if l.find('b'):
            Rank.append(l.get_text().replace(',','').strip())
        elif l.find('a'):
            University.append(l.get_text().replace(',','').strip())
            Link.append(l.find('a')['href'].strip())
        else:
            Location.append(l.get_text().replace(',','').strip())
x=0
for l in Link[:-1]:
    req = Request(url[:-3]+l)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    Description.append(soup.find('p',{"itemprop":"description"}).get_text().replace(',','').strip())
    print(x)
    x+=1
# insersion des données dans fichier csv
for i in range(len(Rank)):
    writer.writerow({'Rank': Rank[i] , 'University': University[i],'Location': Location[i], 'Description': Description[i],  'Link': Link[i]})

csv_file.close()

df = pd.read_csv("C:/Users/assus/Desktop/data5.csv")
df.to_excel("C:/Users/assus/Desktop/data5.xlsx", encoding='utf-8')

