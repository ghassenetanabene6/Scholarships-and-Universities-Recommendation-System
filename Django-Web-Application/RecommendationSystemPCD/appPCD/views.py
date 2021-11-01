from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . models import scholarship,Historique
from datetime import datetime
import io
import csv
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
import string

def loginUser(request):
    if request.user.is_authenticated:
        return redirect ('Recommandation')
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect ('Recommandation')
            else:
                messages.info(request, 'Email or Password is incorrect')
                return render(request,"login.html",{})
        return render(request,"login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect ('Recommandation')
    else:
        if request.method=="POST":
            username=request.POST.get('username')
            email=request.POST.get('email')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            user1 = User.objects.create_user(username=username,email=email,password=password1)
            user=authenticate(request,username=username,password=password1)
            login(request,user)
            return (redirect ('Recommandation'))
        return render(request,"SignUp.html")

@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect ('index')

@login_required(login_url="login")
def recom(request):
	obj=scholarship.objects.all()
	p=set()
	loc=set()
	for i in obj:
		l=i.Program.split(",")
		loc.add(i.Location)
		for j in l:
			p.add(j)
	return render(request,"Recommandation.html",{"programs": p, "location":loc})
    

@login_required(login_url="login")
def rec_sans(request):
    obj=scholarship.objects.order_by("-ScholarshipValue").order_by("-Deadline")
    context={"sansP": obj}
    return render(request,"Rec_sans_pref.html",context)

@login_required(login_url="login")
def histo(request,classe):
    obj=scholarship.objects.filter(Class=classe).order_by("-ScholarshipValue").order_by("-Deadline")
    context={"sansP": obj}
    return render(request,"Rec_sans_pref.html",context)

@login_required(login_url="login")
def rec_avec(request):
	if request.method=="POST":
		username = request.user.username
		path="C:/Users/assus/Downloads/"
		value=request.POST.get('money')
		location=request.POST.get('location')		
		programme=request.POST.get('programme')
		Bachelor=request.POST.get('Bachelor')
		Master=request.POST.get('Master')
		PHD=request.POST.get('PHD')
		if(Bachelor):
			Bachelor=1.0
		else : 
			Bachelor=0.0
		if(Master):
			Master=1.0
		else : 
			Master=0.0
		if(PHD):
			PHD=1.0
		else : 
			PHD=0.0
		description=request.POST.get('description')
		all_Scho_values=scholarship.objects.order_by("-ScholarshipValue")
		for i in all_Scho_values:
			maximum=i.ScholarshipValue
			break
		model = pickle.load(open(path+"kmean.sav", 'rb'))
		vectorizer = pickle.load(open(path+"tf-idf.sav", 'rb'))
		description=text_process(description)
		t=vectorizer.transform([description]).toarray().tolist()
		prediction=model.predict([list((float(value)/float(maximum),int(Bachelor),int(PHD),int(Master)))+t[0]])
		Historique.objects.create(username=request.user.username,date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),classe=prediction[0])
		obj=scholarship.objects.filter(Class=prediction[0]).order_by("-Deadline")
		context={"avecP":obj}
		
		
	else: 
		return render(request,"Recommandation.html")
	return render(request,"Rec_avec_pref.html",context)

@login_required(login_url="login")
def apropos(request):
    return render(request,"Apropos.html")

@login_required(login_url="login")
def historique(request):
    username = request.user.username
    obj=Historique.objects.filter(username=username).order_by("-date")
    context={"histo": obj}
    return render(request,"historique.html",context)

@login_required(login_url="login")
def details(request,id):
    obj = scholarship.objects.get(id=id)
    context={'obj':obj,}
    return render(request,"details.html",context)

def index(request):
    return render(request,"index.html")


@login_required(login_url="login")
def scholarship_upload(request):
	if request.method=="GET":
		return redirect ('index')
	csv_file=request.FILES['file']
	if not csv_file.name.endswith('.csv'):
		messages.error(request,"this is not csv file")
	
	data_set=csv_file.read().decode('UTF-8')
	io_string=io.StringIO(data_set)
	next(io_string)
	scholarship.objects.all().delete()
	for i,row in enumerate(csv.reader(io_string,delimiter=',')):
		x=''
		if row[5]=="1.0":
			x+='Bachelor '
		if row[6]=="1.0":
			x+='Phd '
		if row[7]=="1.0":
			x+='Master '
		if(row[2]!=None and row[2]!=''):
			SV=float(row[2])
		else:
			SV=None
		if(row[11]!=None and row[11]!='' and row[11]!="Un"):
			Rk=float(row[11])
		else:
			Rk=None
		
		_,s = schol=scholarship.objects.update_or_create(
            id=i,
            ScholarshipName=row[0],
            University=row[1],
            ScholarshipValue=SV,
            Deadline=row[3],
            Location=row[4],
            Level=x.strip(),
            Description=row[8],
            Link=row[9],
			Program=row[10],
			Rank=Rk,
            Class=row[12]
            )
	return redirect ('login')


def text_process(text):
    stemmer = WordNetLemmatizer()
    nopunc = [char for char in text if char not in string.punctuation] #supprimer ponctuation
    nopunc = ''.join([i for i in nopunc if not i.isdigit()]) #supprimer les chiffres
    nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('english')] #supprimer les mots d'arrêts
    r = [stemmer.lemmatize(word) for word in nopunc]  #Racination des motes
    return(' '.join(r))