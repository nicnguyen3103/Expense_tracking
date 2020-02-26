from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, DecimalField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a_secret_key. You may change it later'

db = SQLAlchemy(app)

# our real data base 

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)


# you should choose Field corresponding to your expected datatype.
class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    date = DateField('Date')
    submit = SubmitField('Submit')


# assign home route and / route to home 
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    all_expenses = []    
    all_expenses = Expense.query.all()
    return render_template('home.html', expenses=all_expenses)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ExpenseForm()
    form.date.data = datetime.utcnow()
    if form.validate_on_submit():
        expense = Expense(title=form.title.data, category=form.category.data, amount=form.amount.data, date=form.date.data)
        db.session.add(expense)
        db.session.commit()
        return redirect('home')
    return render_template('add.html', form=form,  title='Add New Expense')

@app.route("/update/<int:expense_id>", methods=['GET', 'POST'])
def update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm()
		# if the form is validated and submited, update the data of the item
		# with the data from the field
    if form.validate_on_submit():
        expense.title = form.title.data
        expense.category = form.category.data
        expense.amount = form.amount.data
        expense.date = form.date.data
        db.session.commit()
        return redirect(url_for('home'))
		# populate the field with data of the chosen expense 
    elif request.method == 'GET':
        form.title.data = expense.title
        form.category.data = expense.category
        form.amount.data = expense.amount
        form.date.data = expense.date
    return render_template('add.html', form=form, title='Edit Expense')

@app.route("/delete/<int:expense_id>", methods=['POST'])
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


