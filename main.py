from flask import Flask, render_template,redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired,URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def choice_arr(i):
    return [ i*n for n in range(1,6)]

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location',validators=[DataRequired(),URL()])
    open = TimeField('Opening',validators=[DataRequired()])
    close = TimeField('Closing',validators=[DataRequired()])
    cofeeRating = SelectField('Choose',choices=choice_arr("☕️"),validators=[DataRequired()])
    powerRating = SelectField('Choose',choices=choice_arr("💪"),validators=[DataRequired()])
    wifiRating = SelectField('Choose',choices=choice_arr("🔌"),validators=[DataRequired()])

    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    #turn values in to array
    row = list(form.data.values())[:-1]
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='') as csv_file:
            writer_obj = csv.writer(csv_file, delimiter=",")
            writer_obj.writerow(row)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)

@app.route('/remove/<int:variable>',methods=["DELETE","GET"])
def remove_cafe(variable):
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        list_of_rows.pop()
    with open('cafe-data.csv', 'w', newline='') as csv_file:
        writer_obj = csv.writer(csv_file, delimiter=",")
        writer_obj.writerows(list_of_rows)
    return redirect(url_for('cafes'))


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
