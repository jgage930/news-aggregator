from ast import keyword
from flask_wtf import FlaskForm
from wtforms import DateField, StringField
from wtforms.validators import optional


class SearchForm(FlaskForm):
	# search by date
	start_date = DateField('Start Date', validators=[optional()])
	end_date = DateField('End Date', validators=[optional()]) 
	# search by keyword
	keywords = StringField('Keywords ', validators=[optional()])
