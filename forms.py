from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired

class SearchByDateForm(FlaskForm):
	start_date = DateField('Start Date', validators=[DataRequired()])
	end_date = DateField('End Date', validators=[DataRequired()]) 