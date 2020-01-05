import datetime

from flask import Flask, render_template, url_for, flash, redirect

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '3c4a39427e7e103f6fa0043631e06003'

EXPENSES = [
    {
        'category': 'Food',
        'comment': '',
        'date': datetime.date.today(),
        'price': 100.0
    },
    {
        'category': 'Internet',
        'comment': '2kom',
        'date': datetime.date.today(),
        'price': 390.0
    },
    {
        'category': 'Other',
        'comment': 'палеонтологический музей',
        'date': datetime.date.today(),
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


if __name__ == '__main__':
    app.run(debug=True)