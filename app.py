from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, DecimalField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


app = Flask(__name__)
# postgresql://user:password@hostname/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nguyen:Dragonball1@localhost/expense_app'
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

    def __repr__(self):
        return f"Expense('{self.title}', '{self.category}', {self.amount}, {self.date})"

# you should choose Field corresponding to your expected datatype.
class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], 
                            choices=[('Person', 'Person'), ('Electronics', 'Electronics'), ('Services', 'Services'), 
                                    ('Travel', 'Travel'), ('Others', 'Others'), ('Food', 'Food')])
    amount = DecimalField('Amount', validators=[DataRequired()])
    date = DateField('Date')
    submit = SubmitField('Submit')

    def __repr__(self):
        return f"ExpenseForm('{self.title}', '{self.category}', {self.amount}, {self.date})"

class SearchForm(FlaskForm):
    search = StringField('Search', render_kw={"placeholder": "Search Category"})
    submit = SubmitField('Search')


# assign home route and / route to home 
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    all_expenses = []
    search_string = form.search.data
    if request.method == 'POST' and search_string:
        all_expenses = Expense.query.filter(Expense.category.contains(search_string))
        return render_template('home.html', expenses=all_expenses, form=form)
    else:     
        all_expenses = Expense.query.all()
        return render_template('home.html', expenses=all_expenses, form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(title=form.title.data, category=form.category.data, amount=form.amount.data, date=form.date.data)
        db.session.add(expense)
        db.session.commit()
        return redirect('home')
    form.date.data = datetime.utcnow()
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


