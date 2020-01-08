from flask import render_template, url_for, flash, redirect
from budget_app.forms import RegistrationForm, LoginForm

from budget_app import app
from budget_app.models import User, Expense, Category

EXPENSES = [
    {
        'category': 'Food',
        'comment': '',
        'date': '2020-01-08',
        'price': 100.0
    },
    {
        'category': 'Internet',
        'comment': '2kom',
        'date': '2020-01-08',
        'price': 390.0
    },
    {
        'category': 'Other',
        'comment': 'палеонтологический музей',
        'date': '2020-01-08',
        'price': 600.0
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/expenses')
def expenses():
    return render_template('expenses.html', expenses=EXPENSES, title='Expenses')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('expenses'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Successful login', 'success')
        return redirect(url_for('expenses'))
    # else:
    #     flash('Login failed. Check email or password.', 'danger')
    return render_template('login.html', title='Login', form=form)