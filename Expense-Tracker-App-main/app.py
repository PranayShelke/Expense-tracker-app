from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------------------
# Database Models
# ------------------------------

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

# Expense model associated with a user
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# ------------------------------
# Public Homepage
# ------------------------------

@app.route('/')
def home():
    # If user is logged in, redirect to their expense page
    if current_user.is_authenticated:
        return redirect(url_for('expenses'))
    return render_template('home.html')

# ------------------------------
# Authentication Routes
# ------------------------------

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('expenses'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# ------------------------------
# Expense Management Routes (Authenticated)
# ------------------------------

# Expenses route: display user-specific expenses with optional date filtering
@app.route('/expenses')
@login_required
def expenses():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = Expense.query.filter_by(user_id=current_user.id)
    if start_date:
        try:
            query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        except Exception as e:
            flash('Invalid start date format. Use YYYY-MM-DD.', 'danger')
    if end_date:
        try:
            query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        except Exception as e:
            flash('Invalid end date format. Use YYYY-MM-DD.', 'danger')
    expenses = query.order_by(Expense.date.desc()).all()
    return render_template('expenses.html', expenses=expenses)

# Route to add a new expense
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date_str = request.form['date']
        category = request.form['category']
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_expense = Expense(
                description=description,
                amount=float(amount),
                date=date_obj,
                category=category,
                user_id=current_user.id
            )
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses'))
        except Exception as e:
            flash('Error adding expense: ' + str(e), 'danger')
            return redirect(url_for('add_expense'))
    return render_template('add_expense.html')

# Route to edit an existing expense
@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('You are not authorized to edit this expense.', 'danger')
        return redirect(url_for('expenses'))
    if request.method == 'POST':
        expense.description = request.form['description']
        expense.amount = float(request.form['amount'])
        date_str = request.form['date']
        expense.category = request.form['category']
        try:
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expenses'))
        except Exception as e:
            flash('Error updating expense: ' + str(e), 'danger')
            return redirect(url_for('edit_expense', expense_id=expense_id))
    return render_template('edit_expense.html', expense=expense)

# Route to delete an expense
@app.route('/delete/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('You are not authorized to delete this expense.', 'danger')
        return redirect(url_for('expenses'))
    try:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting expense: ' + str(e), 'danger')
    return redirect(url_for('expenses'))

# ------------------------------
# Dashboard and Export Routes
# ------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    # Pie chart data: expenses grouped by category
    expense_data = db.session.query(
        Expense.category, db.func.sum(Expense.amount)
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
    labels = [row[0] for row in expense_data]
    values = [row[1] for row in expense_data]

    # Bar chart data: monthly expenses
    # (This example uses SQLite's strftime; adjust accordingly if using another DB)
    monthly_expenses = db.session.query(
         db.func.strftime('%m', Expense.date).label('month'),
         db.func.sum(Expense.amount)
    ).filter_by(user_id=current_user.id).group_by('month').all()
    
    # Convert month numbers to abbreviated names and ensure all 12 months are represented:
    from calendar import month_abbr
    monthly_dict = {int(month): total for month, total in monthly_expenses}
    monthlyLabels = [month_abbr[i] for i in range(1, 13)]
    monthlyData = [monthly_dict.get(i, 0) for i in range(1, 13)]

    return render_template('dashboard.html', labels=labels, values=values,
                           monthlyLabels=monthlyLabels, monthlyData=monthlyData)



# Route to export expenses as a CSV file
@app.route('/export')
@login_required
def export():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Description', 'Category', 'Amount'])
    for expense in expenses:
        cw.writerow([
            expense.date.strftime('%Y-%m-%d'),
            expense.description,
            expense.category,
            expense.amount
        ])
    output = si.getvalue()
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=expenses.csv"})

if __name__ == '__main__':
    app.run(debug=True)
