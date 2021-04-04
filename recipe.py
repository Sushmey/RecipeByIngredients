from flask import Flask, render_template, url_for,request
import requests
import json
from forms import IngredientsInput
import os
app = Flask(__name__)



#Default values
recipesCalled = False

SECRET_KEY = os.urandom(32)
# SECRET KEY to prevent modifying of cookies
app.config['SECRET_KEY'] = SECRET_KEY


def apiCall(ingredients,intolerances,vegetarian): #Function to call the API to get the data
	try:
			urlForRecipeByIngredient = 'https://api.spoonacular.com/recipes/complexSearch?apiKey='+apiKey+'&includeIngredients='+ingredients+'&intolerances='+intolerances+'&diet='+vegetarian+'&ignorePantry=true&number=3'
			print(urlForRecipeByIngredient)
			response = requests.get(urlForRecipeByIngredient)
			responseJSON=response.json()
			statusCode = response.status_code
			if(response.status_code==200 and responseJSON['results']!=[]):
				ids=[]
				for i in responseJSON["results"]:
					ids.append(i['id'])
				recipeLinks = []
				timeToCook=[]
				for i in ids:
					i = str(i)
					urlForRecipeLink = 'https://api.spoonacular.com/recipes/'+i+'/information?apiKey='+apiKey+'&includeNutrition=false'
					recipeLinkResponse = requests.get(urlForRecipeLink)
					recipeLinks.append(recipeLinkResponse.json()["sourceUrl"])
					timeToCook.append(recipeLinkResponse.json()["readyInMinutes"])
					statusCode = recipeLinkResponse.status_code		
				if(recipeLinkResponse.status_code==200 and recipeLinkResponse.json()!=[]):
					return responseJSON, statusCode, recipeLinks, timeToCook
				else:
					jsonResponse = None
					recipeLinks = None
					statusCode = 400
					timeToCook = None
					return 	jsonResponse, statusCode, recipeLinks, timeToCook		
			else:
				jsonResponse = None
				recipeLinks = None
				timeToCook = None
				return 	jsonResponse, statusCode, recipeLinks, timeToCook
	except:
		jsonResponse = None
		recipeLinks = None
		timeToCook = None
		return 	jsonResponse, statusCode, recipeLinks, timeToCook			

@app.route('/' ,methods=['GET','POST'])
@app.route('/home' ,methods=['GET','POST'])
def home():
	recipesCalled = False
	form = IngredientsInput()
	if(form.validate_on_submit() and request.method=='POST'):
		recipesCalled = True
		inputIngredients = request.form
		ingredients = inputIngredients['ingredients']
		intolerances = inputIngredients['intolerances']
		try:
			vegetarian = inputIngredients['vegetarian']
		except:
			vegetarian = 'none'			
		print(ingredients)
		jsonResponse, statusCode, recipeLinks, timeToCook= apiCall(ingredients,intolerances, vegetarian)
		if(jsonResponse != None): #So that code doesn't break when jsonResponse is None as it cannot be subscripted
			return render_template('home.html', title='Home', form=form, recipesCalled = recipesCalled, statusCode=statusCode, jsonResponse_recipeLinks_timeToCook = zip(jsonResponse['results'],recipeLinks,timeToCook))
		else:
			return render_template('home.html', title='Home', form=form, recipesCalled = recipesCalled, statusCode=statusCode, jsonResponse=jsonResponse)	
	return render_template('home.html', title='Home', form=form, recipesCalled = recipesCalled)


#Make sure you set debug as False before uploading it on heroku!!
if(__name__=='__main__'):
	app.run(debug=True)    









