from main import db, Expense 

db.create_all()

expense_1 = Expense(title='IphoneX', category='Electronics', amount='1000')
expense_2 = Expense(title='Samsung Galaxy', category='Electronics', amount='1200')
expense_3 = Expense(title='Restaurant', category='Food', amount='50')
expense_4 = Expense(title='Watch', category='Gift', amount='50')

db.session.add(expense_1)
db.session.add(expense_2)
db.session.add(expense_3)
db.session.add(expense_4)

db.session.commit()