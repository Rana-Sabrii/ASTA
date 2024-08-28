from flask import Flask, render_template, redirect , request , jsonify, url_for, session , flash 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import io
import base64
from datetime import datetime




app = Flask(__name__, template_folder='../User History222/templates', static_url_path='/static')
# app.config['SECRET_KEY'] ="67b74762fed8e0dASTA41fb970"
#security password salt

app.secret_key = '67b74762fed8e0d541fb970a6374dda0'
DATABASE = 'test4.db'



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


brain_model = tf.keras.models.load_model('Brain Tumors(94t).h5')

DR_model = tf.keras.models.load_model('Retinopathy(95).h5')

Lung_model = tf.keras.models.load_model('Lung Cancer EFF.h5')

Leukemia_model = tf.keras.models.load_model('Leukemia Cancer EFF 99.h5')



###Brain Tumor ###
# Preprocessing
def preprocess(image):
    img = image.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.expand_dims(img, 0)

    return img

classes =['Glioma Tumor', 'Meningioma Tumor', 'No Tumor detected', 'Pituitary Tumor']

def classify_image(image):
    image = preprocess(image)
    # Make prediction
    prediction = brain_model.predict(image)
    class_indices = np.argmax(prediction[0])
    
    return classes[class_indices]
##############################################
### Diabetic Retinopathy ###
# Preprocessing
def preprocess_DR(image):
    img = image.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0  # Normalize pixel values to be between 0 and 1
    img = tf.expand_dims(img, 0)
    return img


def classify_DR(image):
    image = preprocess_DR(image)
    prediction = DR_model.predict(image)
    predicted_class = np.argmax(prediction[0])
    classes_DR = ['Diabetic Retinopathy' ,'No Diabetic Retinopathy']
    return classes_DR[predicted_class]
#############################################################
####Lung Cancer ##########
# preprocessing 
def preprocess_lung(image):
    img = image.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0 
    img = tf.expand_dims(img, 0)
    return img

lung_classes =['Lung squamous cell carcinoma' ,'Lung Adenocarcinoma','Benign Lung tissues']

def classify_lung(image):
    image = preprocess_lung(image)
    prediction = Lung_model.predict(image)
    predicted_class = np.argmax(prediction[0])
    return lung_classes[predicted_class]

##############################################################
#### Leukemia Cancer ##########
# preprocessing 
def preprocess_leukemia(image):
    img = image.resize((224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0 
    img = tf.expand_dims(img, 0)
    return img

leukemia_classes =['Benign Lymphoblasts' ,'Malignant Lymphoblasts  Early  Pre-B ALL','Malignant Lymphoblasts Pre-B ALL' ,'Malignant Lymphoblasts Pro-B ALL']

def classify_leukemia(image):
    image = preprocess_leukemia(image)
    prediction = Leukemia_model.predict(image)
    predicted_class = np.argmax(prediction[0])
    return leukemia_classes[predicted_class]

@app.route('/')
@app.route('/index') #, methods=['GET', 'POST']
def index():
    if 'user_id' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')
    

@app.route('/registration')
def registration():
    return render_template('regisraion.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data['username']
    email = data['email']
    password = data['password']
    phone_number = data['phoneNum']
    age = data['Age']
    gender = data['genderSelect']
    user_type = data['statusSelect']
    specialization = data.get('specialization')  # Use .get() to handle missing values

    conn = get_db()
    cursor = conn.cursor()

    try:
        # If user_type is 'Pathologist', specialization is required, so check if it's None
        if user_type == 'Pathologist' and specialization is None:
            return 'Specialization is required for Pathologists.', 400

        hashed_password = generate_password_hash(password)  # Hash the password!

        cursor.execute(
            'INSERT INTO USERS (username, email, password, phonenum, Age, genderSelect, statusSelect, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (username, email, hashed_password, phone_number, age, gender, user_type, specialization)
        )
        conn.commit()
        conn.close()

        if user_type != 'patient':
            if 'id_card' not in request.files:
                return 'No file part'
            file = request.files['id_card']
            if file.filename == '':
                return 'No selected file'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('regisraion.html')  # Or redirect to a success page

    except sqlite3.IntegrityError:
        return 'Email already exists', 400


@app.route('/forgot_password')
def forgot_password():
    return render_template('email_check.html') 
 

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Redirect on success, Flask will handle the rest
        return redirect(url_for('change_password', email=email))
    else:
        return jsonify({'status': 'error', 'message': 'User not found'})
    

@app.route('/change_password', methods=['GET', 'POST']) 
def change_password():
    if request.method == 'POST':
        # Handle form submission
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')  # Get email from form data 

        print("New Password:", new_password)
        print("Confirm Password:", confirm_password)
        print("Email:", email)
        print("Hashed Password:", generate_password_hash(new_password))

        if new_password != confirm_password:
            return jsonify({'status': 'error', 'message': 'Passwords don\'t match'})


        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('UPDATE USERS SET password = ? WHERE email = ?', 
                           (generate_password_hash(new_password), email))
            conn.commit()
            print("Password updated successfully in the database.")

        except Exception as e:
            print("Error updating password:", e)
            return jsonify({'status': 'error', 'message': 'Error updating password.'})

        finally:
            if conn:
                conn.close()

        return jsonify({'status': 'success'}) 

    else:  # request.method == 'GET'
        email = request.args.get('email')
        return render_template('change_password.html', email=email, success=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form 
        email = data.get('email')
        password = data.get('password')

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM USERS WHERE email = ?', (email,)) # Get user by email
            user = cursor.fetchone()

        if user and check_password_hash(user['password'], password): # Compare hashes
            session['user_id'] = user['User_id']
            session['username'] = user['username']
            return redirect('/')
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login')) 

    else: # request.method == 'GET'
        return render_template('regisraion.html') 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/registration')



@app.route('/check-login-status', methods=['GET'])
def check_login_status():
    if 'user_id'  in session:
        
     return jsonify({'loggedIn': True, 'username': session['username'] ,'redirect_url': url_for('index')})
    
    else:
        return jsonify({'loggedIn': False})
    
    
@app.route('/get-user-data', methods=['GET'])
def get_user_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    user_id = session['user_id']

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE User_id = ?', (user_id,))
        user = cursor.fetchone()

    user_data = {
        'username': user['username'],
        'email': user['email'],
        'phoneNum': user['phonenum'],
        'Age': user['Age'],
        'genderSelect': user['genderSelect'],
        'statusSelect': user['statusSelect'],
        'specialization': user['specialization']
    }

    return jsonify(user_data)
        



@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    user_id = session['user_id']
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']  # Assuming 'password' is provided in the request
    phone_num = data['phoneNum']
    age = data['Age']
    gender = data['genderSelect']
    status = data['statusSelect']
    specialization = data['specialization']

    

    with get_db() as conn:
        cursor = conn.cursor()

        # Fetch the existing password if provided
        cursor.execute('SELECT password FROM USERS WHERE User_id = ?', (user_id,))
        existing_password = cursor.fetchone()[0]

        # Hash the password if it's provided, otherwise use the existing password
        if password:
            hashed_password = generate_password_hash(password)  # Use generate_password_hash directly
        else:
            hashed_password = existing_password
        
        cursor.execute(
            'UPDATE USERS SET username = ?, email = ?, password = ?, phonenum = ?, Age = ?, genderSelect = ?, statusSelect = ?, specialization = ? WHERE User_id = ?',
            (username, email, hashed_password, phone_num, age, gender, status, specialization, user_id)
        )
        
        conn.commit()

    return jsonify({'success': True})

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if not logged in

    user_id = session['user_id']
    results = []

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT 
                Results.Prediction_result, 
                Results.timestamp, 
                Disease.Disease_name
               FROM Results
               JOIN Disease ON Results.Disease_name = Disease.Disease_name
               WHERE Results.User_id = ?
               ORDER BY Results.timestamp DESC''',
            (user_id,)
        )

        # Format timestamp here
        results = cursor.fetchall()
        formatted_results = []
        for row in results:
            formatted_timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            formatted_results.append({'Prediction_result': row['Prediction_result'], 
                                    'timestamp': formatted_timestamp,
                                    'Disease_name': row['Disease_name']})

    return render_template('UserHistory.html', results=formatted_results)


@app.route('/ContactDoc')
def ContactDoc():
    return render_template('ContactDoc.html')

@app.route('/get-doctors', methods=['GET'])
def get_doctors():
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, email, phonenum,statusSelect,specialization FROM USERS WHERE statusSelect IN ("Pathologist", "Multi Omics Analyst")')
        doctors = cursor.fetchall()
    
    doctor_list = []
    for doctor in doctors:
        doctor_list.append({
            'username': doctor['username'],
            'email': doctor['email'],
            'phonenum': doctor['phonenum'],
            'user_type': doctor['statusSelect'],
            'specialization': doctor['specialization']
            
        })

    return jsonify(doctor_list)

@app.route('/diseases')
def diseases():
    return render_template('diseases.html')


@app.route('/MultiOmics')
def MultiOmics():
    return render_template('MultiOmics.html')

############# Diseases Pages #########
@app.route('/BrainTumor' , methods=['GET', 'POST'])
def BrainTumor():
    
    return render_template('DiseasesPages/BrainTumer.html')

@app.route('/DiabeticRetin' , methods=['GET', 'POST'])
def DiabeticRetin():
    return render_template('DiseasesPages/DiabeticRetin.html')


@app.route('/LungCancer', methods=['GET', 'POST'])
def LungCancer():
    return render_template('DiseasesPages/LungCancer.html')

@app.route('/leukemia' , methods=['GET', 'POST'])
def leukemia():
    return render_template('DiseasesPages/leukemia.html')



######## Results Pages ###########
@app.route('/BrainTumerRes', methods=['POST'])
def BrainTumerRes():
    if 'user_id' not in session:
        return redirect('/login') 

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image file selected."
    image = Image.open(image_file)
    results = classify_image(image)

    # Image Processing to get Base64
    image_data = io.BytesIO()
    image.save(image_data, format='JPEG')  # Adjust format if needed (PNG, etc.)
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8') 

    # Save the result to the database
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            # Insert the disease name if it doesn't exist
            cursor.execute(
                'INSERT OR IGNORE INTO Disease (Disease_name) VALUES (?)',
                ('Brain Tumor',) 
            )
            # Save the prediction result
            cursor.execute(
                'INSERT INTO Results (User_id, Disease_name, Prediction_result) VALUES (?, ?, ?)',
                (session['user_id'], 'Brain Tumor', results)
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving result to database: {e}")
        return "An error occurred while saving the result." 

    return render_template('ResultsPages/BrainTumerRes.html', image=image_base64, results=results)

@app.route('/DiabeticRes', methods=['POST'])
def DiabeticRes():
    if 'user_id' not in session:
        return redirect('/login') 

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image file selected."
    image = Image.open(image_file)
    results = classify_DR(image)

    # Image Processing to get Base64
    image_data = io.BytesIO()
    image.save(image_data, format='PNG')  # Adjust format if needed (PNG, etc.)
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8') 

    # Save the result to the database
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            # Insert the disease name if it doesn't exist
            cursor.execute(
                'INSERT OR IGNORE INTO Disease (Disease_name) VALUES (?)',
                ('Diabetic Retinopathy',)  # Insert 'Diabetic Retinopathy' into the Disease table
            )
            # Save the prediction result
            cursor.execute(
                'INSERT INTO Results (User_id, Disease_name, Prediction_result) VALUES (?, ?, ?)',
                (session['user_id'], 'Diabetic Retinopathy', results) 
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving result to database: {e}")
        return "An error occurred while saving the result." 

    return render_template('ResultsPages/DiabeticRes.html', image=image_base64, results=results)

@app.route('/LungCancerRes', methods=['POST'])
def LungCancerRes():
    if 'user_id' not in session:
        return redirect('/login')  

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image file selected."
    image = Image.open(image_file)
    results = classify_lung(image)

    # Image Processing to get Base64
    image_data = io.BytesIO()
    image.save(image_data, format='JPEG')  # Adjust format if needed (PNG, etc.)
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8') 

    # Save the result to the database
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            # Insert the disease name if it doesn't exist
            cursor.execute(
                'INSERT OR IGNORE INTO Disease (Disease_name) VALUES (?)',
                ('Lung Cancer',)  # Insert 'Lung Cancer' into the Disease table
            )
            # Save the prediction result
            cursor.execute(
                'INSERT INTO Results (User_id, Disease_name, Prediction_result) VALUES (?, ?, ?)',
                (session['user_id'], 'Lung Cancer', results)  
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving result to database: {e}")
        return "An error occurred while saving the result." 

    return render_template('ResultsPages/LungCancerRes.html', image=image_base64, results=results)

@app.route('/LeukemiaRes', methods=['POST'])
def LeukemiaRes():
    if 'user_id' not in session:
        return redirect('/login') 

    image_file = request.files['image']
    if image_file.filename == '':
        return "No image file selected."
    image = Image.open(image_file)
    results = classify_leukemia(image)

    # Image Processing to get Base64
    image_data = io.BytesIO()
    image.save(image_data, format='JPEG')  # Adjust format if needed (PNG, etc.)
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')

    # Save the result to the database
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            # Insert the disease name if it doesn't exist
            cursor.execute(
                'INSERT OR IGNORE INTO Disease (Disease_name) VALUES (?)',
                ('Leukemia',)  # Insert 'Leukemia' into the Disease table
            )
            # Save the prediction result
            cursor.execute(
                'INSERT INTO Results (User_id, Disease_name, Prediction_result) VALUES (?, ?, ?)',
                (session['user_id'], 'Leukemia', results)  
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving result to database: {e}")
        return "An error occurred while saving the result."  

    return render_template('ResultsPages/LeukemiaRes.html', image=image_base64, results=results)





##################################Run Home ########################

if __name__ == '__main__':
    # Ensure the USERS table is created
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(150) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(150) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(10) NOT NULL,
            user_type VARCHAR(50) NOT NULL,
            reset_token TEXT
        )
        ''')

        # Populate Disease table
        diseases = [
            ('Brain Tumor',),
            ('Diabetic Retinopathy',),
            ('Lung Cancer',),
            ('Leukemia',)
        ]

        cursor.executemany("INSERT OR IGNORE INTO Disease (Disease_name) VALUES (?)", diseases)
        conn.commit()
    app.run(port=2000, debug=True)