from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from tag_list_field import TagListField
from wtforms.validators import InputRequired

class IngredientsInput(FlaskForm):
	ingredients = TagListField("Ingredients",separator=",",validators=[InputRequired()])
	intolerances = SelectField('Allergies', choices=[('none','None'),('dairy', 'Dairy'), ('egg', 'Egg'), ('gluten', 'Gluten'),('grain','Grain'),
    	('peanut','Peanut'),('seafood','Seafood'),('sesame','Sesame'),('shellfish','Shellfish'),('soy','Soy'),
    	('sulfite','Sulfite'),('treeNut','Tree Nut'),('wheat','Wheat')],validators=[InputRequired()])
	vegetarian = BooleanField('Vegetarian Only')




	submit = SubmitField('Find recipes!')
