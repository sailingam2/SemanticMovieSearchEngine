from django.shortcuts import render

# Create your views here.

import sys
from django.http import HttpResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home(request):
    template = 'home.html'
    context = {}
    if request.user and request.user.is_authenticated():
		    	userN = User.objects.filter(username=request.user.username)[0]
			context = {'loggedin':1,'user':userN}
			#user = authenticate(username=userN.username,password=userN.password)
			#login(request,user)
			genreObj = genre.objects.filter(user=userN.username)
			if genreObj:
				genreSelected = genreObj[0].genreS
				q = getQuery.genreQuery(genreSelected)
				print "qyer",q
				sparqlQ = SPARQLWrapper("http://localhost:3030/movies/query")
				sparqlQ.setQuery(q)
				sparqlQ.setReturnFormat(JSON)

				results = sparqlQ.query().convert()
				print "res",results
				context['results'] = results['results']['bindings']



			return render(request, 'home.html', context)
    return render(request, template, context)

def register(request):
	if request.method == 'POST':
		username = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = User.objects.create_user(username, email, password)
		user.save()
		context = {'loggedin':1}
		return render(request, 'register.html', context)

	template = 'register.html'
	context = {}
	return render(request, template, context)

from jenyapp.models import genre

def signin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			userN = User.objects.filter(username=username)[0]
			context = {'loggedin':1,'user':userN}
			#user = authenticate(username=userN.username,password=userN.password)
			#login(request,user)
			genreObj = genre.objects.filter(user=userN.username)
			if genreObj:
				genreSelected = genreObj[0].genreS
				q = getQuery.genreQuery(genreSelected)
				print "qyer",q
				sparqlQ = SPARQLWrapper("http://localhost:3030/movies/query")
				sparqlQ.setQuery(q)
				sparqlQ.setReturnFormat(JSON)

				results = sparqlQ.query().convert()
				print "res",results
				context['results'] = results['results']['bindings']



			return render(request, 'home.html', context)
		context = {}
		
		return render(request, 'register.html', context)

	template = 'signin.html'
	context = {}
	return render(request, template, context)

import getQuery

from SPARQLWrapper import SPARQLWrapper, JSON
def logoutUser(request):
	logout(user)
	return render(request,'signin.html',{})

def searchForm(request):
	
	postData = request.POST
	inDict = {}
	for key,val in postData.items():
		inDict.update({key:val})
		if key=='genre':
			loggedin= request.user.is_authenticated()
			print "re",request.user
			print "logged in valeu ",loggedin
			genreObj = None
			if loggedin and val:
				user = request.user
				if genre.objects.filter(user=user.username):
					genreObj= genre.objects.filter(user=user.username)[0]
					genreObj.genreS = val
				else:
					genreObj = genre(user=user.username,genreS=val)
				genreObj.save()



			if genreObj:
				genreSelected = genre.genreS


	q = getQuery.formQuery(inDict)
	print "indict"
	sparqlQ = SPARQLWrapper("http://localhost:3030/movies/query")
	print "qyer",q
	sparqlQ.setQuery(q)
	sparqlQ.setReturnFormat(JSON)

	results = sparqlQ.query().convert()

        res = []
	for result in results["results"]["bindings"]:
		res.append(result["title"])
	context = {}
        context['res'] = res
	return render(request, 'results.html', context)

def getMovieInfo(request):
	movie = request.GET.get('movie')
	q = getQuery.getMovieInfo(movie)
	print "indict"
	sparqlQ = SPARQLWrapper("http://localhost:3030/movies/query")
	print "qyer",q
	sparqlQ.setQuery(q)
	sparqlQ.setReturnFormat(JSON)

	results = sparqlQ.query().convert()

        #res = []
	#for result in results["results"]["bindings"]:
		#res.append(result["ti)
	context = {}
	res = {}
        context['res'] = results["results"]["bindings"]
        print "fsadfdsafsdfsdfcontedx",context['res']
        for i in context['res']:
        	for key,val in i.items():
        		if res.get(key):
        			res[key] += ", " + val['value']
        		else:
        			res[key] = val['value']
        context['res'] = res

        print context
	return render(request, 'movieinfo.html', context)



def getActorInfo(request):
	actor = request.GET.get('actor')
	if len(actor.split(',')) > 1:
		actor = actor.split(',')[0]
	actor = actor.strip()
	q = getQuery.getActorQuery(actor)
	print "indict"
	sparqlQ = SPARQLWrapper("http://localhost:3030/movies/query")
	print "qyer",q
	sparqlQ.setQuery(q)
	sparqlQ.setReturnFormat(JSON)

	results = sparqlQ.query().convert()

        #res = []
	#for result in results["results"]["bindings"]:
		#res.append(result["ti)
	context = {}
	res = {}
        context['res'] = results["results"]["bindings"]
        print "fsadfdsafsdfsdfcontedx",context['res']
        for i in context['res']:
        	for key,val in i.items():
        		if res.get(key):
        			res[key] += ", " + val['value']
        		else:
        			res[key] = val['value']
        context['res'] = res

        print context
	return render(request, 'actorinfo.html', context)




