from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']= '818a3da9a9af6c628fbe9e5e0c6e9815'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(20), unique=True, nullable =False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Addresses', backref = 'customerdata', lazy= True)

    def  __repr__(self):
        return f"Customer('{self.first_name}','{self.last_name}','{self.image_file}')"

class Addresses(db.Model):
    cust_id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.Text, nullable= True)
    date_posted = db.Column(db.DateTime, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), nullable= False)

    def  __repr__(self):
        return f"Addresses(''{self.address}','{self.date_posted}')"

customers_date = [
    {
        'cust_id': '1',
        'First_name': 'John',
        'Last_name': 'M',
        'Address': '123 Washington'
    },
    {
        'cust_id' : '2',
        'First_name' : 'Ron',
        'Last_name' : 'K',
        'Address' : '321 Newyork'
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html', posts= customers_date)

@app.route("/register", methods= ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title = 'Register', form= form)

@app.route("/login", methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abc@xyz.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsucessful attempt. Please chec username or password', 'danger')
    return render_template('login.html',title = 'Login', form= form)

if __name__ == "__main__":
    app.run(debug=True)