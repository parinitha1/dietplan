from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.Date, nullable=False)

    # Relationship with the Details table
    details = db.relationship('Details', backref='user', lazy=True)

# Details Model
class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

def calculate_bmi(age, gender, height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        status = "Normal weight"
    elif 25 <= bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"
    
    return {
        "age": age,
        "gender": gender,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": round(bmi, 2),
        "status": status
    }

@app.route('/')
def create_account():
    return render_template('create_account.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['name_mother']
    dob = datetime.strptime(request.form['dob_mother'], '%Y-%m-%d')
    
    new_user = User(username=username, password=password, full_name=full_name, dob=dob)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Account created successfully! Please log in.')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id  # Save user session
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('submit'))
    return render_template('home1.html')

@app.route('/submit', methods=['POST'])
def submit():
    age = int(request.form['age'])
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    gender = request.form['gender']
    
    result = calculate_bmi(age, gender, height, weight)
    
    # Save the details to the database
    user_id = session.get('user_id')
    new_details = Details(age=age, height_cm=height, weight_kg=weight, bmi=result['bmi'], status=result['status'], user_id=user_id)
    db.session.add(new_details)
    db.session.commit()
    
    return render_template('result.html', result=result)

@app.route('/dietplan', methods=['GET'])
def diet_plan():
    return render_template('dietplan.html')

# Routes for diet plan details
@app.route('/underweight_veg')
def underweight_veg():
    return render_template('underweight_veg.html')

@app.route('/normal_veg')
def normal_veg():
    return render_template('normal_veg.html')

@app.route('/overweight_veg')
def overweight_veg():
    return render_template('overweight_veg.html')

@app.route('/obese_veg')
def obese_veg():
    return render_template('obese_veg.html')

@app.route('/underweight_nonveg')
def underweight_nonveg():
    return render_template('underweight_nonveg.html')

@app.route('/normal_nonveg')
def normal_nonveg():
    return render_template('normal_nonveg.html')

@app.route('/overweight_nonveg')
def overweight_nonveg():
    return render_template('overweight_nonveg.html')

@app.route('/obese_nonveg')
def obese_nonveg():
    return render_template('obese_nonveg.html')

@app.route('/underweight_vegan')
def underweight_vegan():
    return render_template('underweight_vegan.html')

@app.route('/normal_vegan')
def normal_vegan():
    return render_template('normal_vegan.html')

@app.route('/overweight_vegan')
def overweight_vegan():
    return render_template('overweight_vegan.html')

@app.route('/obese_vegan')
def obese_vegan():
    return render_template('obese_vegan.html')

@app.route('/update_details', methods=['GET', 'POST'])
def update_details():
    user_id = session.get('user_id')
    user_details = Details.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = request.form['gender']
        
        # Recalculate BMI and status
        result = calculate_bmi(age, gender, height, weight)
        
        # Update the existing details record
        user_details.age = age
        user_details.height_cm = height
        user_details.weight_kg = weight
        user_details.bmi = result['bmi']
        user_details.status = result['status']
        
        db.session.commit()
        flash('Details updated successfully!')

        # Redirect to the result page with updated details
        return render_template('result.html', result=result)

    return render_template('update_details.html', details=user_details)


if __name__ == '__main__':
    app.run(debug=True)
