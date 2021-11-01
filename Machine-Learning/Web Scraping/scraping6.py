import os
import requests
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


# Ouverture du site web contenant les bourses et prélévement des liens amenant à chaque description de bourse
Scholarship_link0=[] # Liste contenant les liens dans la plateforme studyportals pour accéder à chaque bourse d'étude à USA
Scholarship_link=[]
for i in range(1,2):
    home="https://www.scholars4dev.com/page/"+str(i)+"/"
    response1 = requests.get(home)
    soup = BeautifulSoup(response1.text, 'html.parser')
    Scholarship_link=soup.find_all('a',{"class": "more-link"})

Scholarship_link=[s['href'] for s in Scholarship_link]
for link in Scholarship_link:
    append_to_file(file, link)

# Extraction des données de chaque bourse sous la structure ci-dessous

Names=[] #   Liste contenant tous les noms des bourses d'étude trouvées
SchoLevel=[]    #   Liste contenant le niveau d'étude demandé des bourse
SchoValue=[]    #   Liste contenant les valeurs des bourse
SchoDeadline=[]     #   Liste contenant les dates limites de l'inscription des bourses
SchoStudyIn=[]        # liste contenant les lieux d'études
SchoStart=[]        # liste contenant les dates de débuts des études
Descriptions=[]     #   Liste contenant les descriptions des bourses
Eligibility=[]      #   Liste contenant les éligibilités des candidats
Application=[]       #   Liste contenant les applications
Website=[]

csv_file=open('data1.csv', mode='w',newline='',encoding="utf-8")
fieldnames = ['Scholarship Name', 'Level of Study' ,'Scholarship Value','Date', 'Eligibility','Benefits','Application','Descriptions']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()
f = open(file, "r")
i=0 # compteur pour nous aider à trouver: nom, deadline , lieu , niveau, date début

for url in  Scholarship_link:  
    response2 = requests.get(url)
    soup = BeautifulSoup(response2.text, 'html.parser')
    X=soup.find_all('div',{"class":"post_column_1"})    # X est le type de page standard d'une bourse pour éviter les problèmes rencontrés
    try:
        if(X!=[]): # test sur la structure de la page de type X 
                    
            for title in soup.find_all('div',{"class":"post_column_1"}):
                try:
                    chaine=title.get_text()                
                    chaine=chaine.replace("Study in",'').replace("Deadline",'').replace(":",'')
                    l=chaine.split('\n')
                    if(i%2==0):
                        try:

                            # Extraction des noms et des niveaux de chaque bourse
                            
                            Names.append(l[0].replace("\xa0"," ").replace('\u200b','').replace('\n','. ').strip())
                            SchoLevel.append(l[1].replace("\xa0"," ").replace('\u200b','').replace('\n','. ').strip())
                            i+=1
                        except:

                            # S'il y'a un manque de données, on remplie les tables par None pour éviter le chevauchement des lignes
                            
                            if(l[0]==''):
                                Names.append(None)
                            if(l[1]==''):
                                SchoLevel.append(None)
                            print("error 1.1 : something is wrong with Names or SchoLevel !") 
                    else:
                        try:

                            # Extraction des dates limites, dates début et des lieux d'étude de chaque bourse
                            
                            SchoDeadline.append(l[0].replace("\xa0"," ").strip())
                            SchoStudyIn.append(l[1].replace("\xa0"," ").replace('\u200b','').strip())
                            SchoStart.append(l[2].replace("\xa0"," ").replace('\u200b','').replace('\n','. ').replace("Course starts",'').strip())
                            i+=1
                        except:
                            
                            # S'il y'a un manque de données, on remplie les tables par None pour éviter le chevauchement des lignes
                            
                            if(l[0]==''):
                                SchoDeadline.append(None)
                            if(l[1]==''):
                                SchoStudyIn.append(None)
                            if(l[1]==''):
                                SchoStart.append(None)
                            print("error 1.2 : something is wrong with SchoDeadline or SchoStudyIn or SchoStart!") 
                                           
                except : print("error 1 : something is wrong !") 

            #les données se trouvent dans les balises p où les développeurs de la plateforme non pas spécifier des classes ou id à chaque donnée
            P=soup.find_all('p')
            P=[s.get_text() for s in P]

            #ici on va faire une extration à l'aide de la programmation et non pas web scrapping pûr
            #les valeurs par défauts des indices sont nulles 
            Descript_index=0
            Host_index=0
            val_index=0
            elig_index=0
            app_index=0
            website_index=0
            #les valeurs par défauts des chaines cherchées sont vides 
            descript=""
            val=""
            elig=""
            app=""
                        
            try:
                for cpt in range(len(P)):
                    try:
                        if('BRIEF DESCRIPTION' in P[cpt].upper()):
                            Descript_index=cpt
                    except:
                        print("error 2.1 : something is wrong with Description !")
                        pass
                    try:
                        if('HOST INSTITUTION' in P[cpt].upper()):
                            Host_index=cpt
                    except:
                        print("error 2.2 : something is wrong with Host Institution !")                        
                        pass
                    try:
                        if('SCHOLARSHIP VALUE' in P[cpt].upper() or 'SCHOLARSHIP INCLUSIONS'in P[cpt].upper()):
                            val_index=cpt
                    except:
                        print("error 2.3 : something is wrong with Scholarship value !")                        
                        pass
                    try:
                        if('ELIGIBILITY' in P[cpt].upper()):
                            elig_index=cpt
                    except:
                        print("error 2.4 : something is wrong with Eligibility !")                        
                        pass
                    try:
                        if('APPLICATION INSTRUCTIONS' in P[cpt].upper()):
                            app_index=cpt
                    except:
                        print("error 2.5 : something is wrong with Application instructions !")                        
                        pass
                    try:
                        if('WEBSITE:' in P[cpt].upper()):
                            website_index=cpt
                    except:
                        print("error 2.6 : something is wrong with Website !")                        
                        pass
                                        
                # Extraction des Descriptions
                
                if(Descript_index!=0 and Host_index!=0):
                    for cpt in range(Descript_index+1,Host_index):
                        descript+=P[cpt]
                    Descriptions.append(descript.replace("\xa0"," ").replace('\u200b','').replace('\n','. '))
                else: 
                    Descriptions.append(None) #en cas où il n'y a pas de description
                    
                # Extraction des Valeurs des bourses
                
                if(val_index!=0 and elig_index!=0):
                    for cpt in range(val_index+1,elig_index):
                        val+=P[cpt]
                    SchoValue.append(val.replace("\xa0"," ").replace('\u200b','').replace('\n','. '))
                else:               
                    SchoValue.append(None) #en cas où il n'y a pas , ou un problème quelconque trouvé
               
                    
                # Extraction des éligibilités des candidats
                
                if(elig_index!=0 and app_index!=0):
                    try:
                        for cpt in range(elig_index+1,app_index):
                            elig+=P[cpt]
                    except:
                        pass   
                    
                    
                    if(elig!=""):
                        try:
                            Eligibility.append(elig.replace("\xa0"," ").replace('\u200b','').replace('\n','. '))
                        except:
                            pass    # on va traiter ce cas dans la partie else au dessous (balise ol dans le site pour qlqes bourses)

                    else:
                        try:
                            balise_ol=""
                            for i in OL:
                                balise_ol+=i.replace("\xa0"," ").replace('\u200b','').replace('\n','. ')                           
                            Eligibilitybility.append(balise_ol)
                        except:
                            print("erreur dans le remplissage de la bource du site {}".format(url))

                else:
                    Eligibility.append(None) #en cas où il n'y a pas, ou un problème quelconque trouvé

                    
                # Extraction des applications des études
                
                if(app_index!=0 and website_index!=0):
                    try:
                        for cpt in range(app_index+1,website_index):
                            app+=P[cpt]
                        Application.append(app.replace("\xa0"," ").replace('\u200b','').replace('Website:','').replace('\n','. '))
                    except:
                        print("erreur\n")
                else:
                    Application.append(None) #en cas où il n'y a pas, ou un problème quelconque trouvé

           
            
            except:
                print("error 2 : something is wrong !")
                pass


        
    except:
        print("error 0 : something is wrong !")
        pass


'''
for i in range(len(Eligibility)):
	print('i=',i,'\n',Eligibility[i],"\n\n")
print(len(Eligibility))
'''  

#print(Names,'\n',SchoLevel,'\n',SchoDeadline,'\n',SchoStudyIn,'\n',SchoStart,"\n#########\n")



##'''
##hethi tefrez les liens eli jawhom behi wtemchi zay lfol !!!!
##for url in  Scholarship_link:  #Scholarship_link:
##    response2 = requests.get(url)
##    soup = BeautifulSoup(response2.text, 'html.parser')
##    X=soup.find_all('div',{"class":"post_column_1"})
##    if(X==[]):
##        l.append(url)
##for i in Scholarship_link:
##    if (i not in l):
##        print(i)
##        '''


##                for cpt in range(len(P)):
##                    try:
##                        if('BRIEF DESCRIPTION' in P[cpt].upper()):
##                            Descript_index=cpt
##                    except:
##                        print("error 3 : something is wrong with description !")
##                        Descriptions.append('****') #en cas où il n'y a pas de description
##                        pass
##                    try:
##                        if('HOST INSTITUTION' in P[cpt].upper()):
##                            Host_index=cpt
##                    except:
##                        print("error 3 : something is wrong with Host Institution !")
##                        
##                        break
##                for
''''
# Extraction des éligibilités des candidats ça marche avec un probleme fel 1 et 2 je crois
                
                if(elig_index!=0 and app_index!=0):
                    try:
                        for cpt in range(elig_index+1,app_index):
                            elig+=P[cpt]
                        if(elig!=""):
                            Eligibility.append(elig.replace("\xa0"," ").replace('\u200b','').replace('\n','. '))
                        else:
                            Eligibility.append("lahné")
                    except:
                        print("erreur\n")
                else:
                    Eligibility.append('****') #en cas où il n'y a pas, ou un problème quelconque trouvé

'''



   
csv_file.close()
f.close()
