from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import URLField
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    opening = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g. 6PM', validators=[DataRequired()])
    wifi = StringField('Wifi Password', validators=[DataRequired()])
    coffee = SelectField('Sarah\'s Cafe Rating', choices=['☕️','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'])
    socket = SelectField('Power Socket Availability', choices=['✘','🔌','🔌🔌','🔌🔌🔌'])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = [value for (key,value) in form.data.items() if not key in ['submit', 'csrf_token']]
        print(new_row)
        with open('cafe-data.csv', "a") as csv_file:
            csv_file.write("\n")
            for item in new_row:
                csv_file.write(item + ",")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
