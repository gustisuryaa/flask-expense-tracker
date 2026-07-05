from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        title = request.form['title']
        amount = request.form['amount']
        new_expense = Expense(title=title, amount=amount)
        
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')
    
    
    expenses = Expense.query.all()
    total = sum(item.amount for item in expenses)
    return render_template('index.html', expenses=expenses, total=total)

if __name__ == "__main__":
    app.run(debug=True)