from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)    

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    note = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    expenses = Expense.query.all()
    total = sum(e.amount for e in expenses)
    return render_template('index.html', expenses=expenses ,
total=total)



@app.route('/add', methods=['POST'])
def add_expense():
    new_expense = Expense(
        amount=float(request.form['amount']),
        category=request.form['category'],
        date=request.form['date'],
        note=request.form['note']
    )
    db.session.add(new_expense)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_expense(id):
    expense = Expense.query.get(id)
    return render_template('edit.html', expense=expense)

@app.route('/update/<int:id>', methods=['POST'])
def update_expense(id):
    expense = Expense.query.get(id)
    expense.amount = float(request.form['amount'])
    expense.category = request.form['category']
    expense.date = request.form['date']
    expense.note = request.form['note']
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)