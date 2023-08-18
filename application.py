from flask import Flask, render_template, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import pandas as pd
from main import recommend

data = pd.read_csv('zomato_cleaned.csv')
loc_list = list(set(data['location'].tolist()))
loc_list.insert(0, 'Choose....')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf603aefb078ed6650460e3f'


class LocationForm(FlaskForm):
    location = SelectField(choices=loc_list, default='Choose....',
                           validators=[DataRequired(message='Select a valid option')])
    book_table = SelectField(choices=['Choose...', 'Yes', 'No'], default='Choose...',
                             validators=[DataRequired(message='Select a value')])
    online_order = SelectField(choices=['Choose...', 'Yes', 'No'], default='Choose...',
                               validators=[DataRequired(message='Select a value')])
    rating = FloatField(validators=[NumberRange(min=1, max=5)])
    votes = IntegerField(validators=[NumberRange(min=1, max=17000)])
    approx_cost = IntegerField(validators=[DataRequired(), NumberRange(min=50, max=6000)])
    res_type = SelectField(choices=['Choose...', 'Quick Bites', 'Casual Dining', 'Desert Parlour', 'Cafe', 'Beverage Shop', 'Bakery', 'Sweet Shop', 'Food court', 'Kiosk', 'Pub', 'Takeaway', 'Delivery', 'Lounge', 'Microbrewery'])
    submit = SubmitField(label='Submit')


@app.route('/', methods=["GET", "POST"])
def main():
    form = LocationForm()
    if form.validate_on_submit():
        if form.location.data == 'Choose....' or form.book_table.data == 'Choose...' or form.online_order.data == 'Choose...' or form.res_type.data == 'Choose...':
            flash(message='Select all valid options.', category='danger')
        else:
            recommended_rest = recommend(location=form.location.data, data=data, book_table=form.book_table.data, online_order=form.online_order.data, rating=form.rating.data, reviews=form.votes.data, cost=form.approx_cost.data, type=form.res_type.data)
            recommended_rest_list = []
            for i in range(0, 5):
                li = recommended_rest.iloc[i, :].values.flatten().tolist()
                recommended_rest_list.append(li)
            return render_template('home.html', form=form, list=recommended_rest_list, visibility='visible')
    if form.errors != {}:
        for error in form.errors.values():
            flash(error, category='danger')
    return render_template('home.html', form=form, visibility='hidden')


if __name__ == '__main__':
    app.run(debug=True)
