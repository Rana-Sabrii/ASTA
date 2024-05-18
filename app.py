from flask import Flask, render_template, redirect , request , jsonify, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import io
import base64



app = Flask(__name__, template_folder='../Final graduation-main/templates', static_url_path='/static')

app.secret_key = '67b74762fed8e0d541fb970a6374dda0'
DATABASE = 'userdata.db'

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
###############################################
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
##############################################################
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

@app.route('/register' , methods=['POST'])
def register():   
    data = request.form
    username = data['username']
    email = data['email']
    password = data['password']
    phone_number = data['phoneNum']
    age = data['Age']
    gender = data['genderSelect']
    user_type = data['statusSelect']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO USERS (username, email, password, phonenum, Age, genderSelect, statusSelect) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (username, email, password, phone_number, age, gender, user_type)
    )
    conn.commit()
    conn.close()
    if (user_type!='patient'):
        if 'id_card' not in request.files:
            return 'No file part'
        file = request.files['id_card']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('regisraion.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data['email']
    password = data['password']

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM USERS WHERE email = ? AND password = ?',
            (email, password)
        )
        user = cursor.fetchone()

    if user:
        session['user_id'] = user['User_id']
        session['username'] = user['username']
        return redirect('/')
    

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
        cursor.execute('SELECT * FROM users WHERE User_id = ?', (user_id,))
        user = cursor.fetchone()

    user_data = {
        'username': user['username'],
        'email': user['email'],
        'phoneNum': user['phonenum'],
        'Age': user['Age'],
        'genderSelect': user['genderSelect'],
        'statusSelect': user['statusSelect']
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
    password = data['password'] 
    phone_num = data['phoneNum']
    age = data['Age']
    gender = data['genderSelect']
    status = data['statusSelect']

    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE USERS SET username = ?, email = ?, password = ?, phonenum = ?, Age = ?, genderSelect = ?, statusSelect = ? WHERE User_id = ?',
            (username, email, password, phone_num, age, gender, status, user_id)
        )
        
        conn.commit()

    return jsonify({'success': True})

@app.route('/results')
def results():
    return render_template('UserHistory.html')

@app.route('/ContactDoc')
def ContactDoc():
    return render_template('ContactDoc.html')

@app.route('/get-doctors', methods=['GET'])
def get_doctors():
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, email, phonenum,statusSelect FROM USERS WHERE statusSelect IN ("Pathologist", "Multi Omics Analyst")')
        doctors = cursor.fetchall()
    
    doctor_list = []
    for doctor in doctors:
        doctor_list.append({
            'username': doctor['username'],
            'email': doctor['email'],
            'phonenum': doctor['phonenum'],
            'user_type': doctor['statusSelect']
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
@app.route('/BrainTumerRes' , methods=['POST'])
def BrainTumerRes():
    image_file = request.files['image']
    image = Image.open(image_file)

    image_data = io.BytesIO()
    image.save(image_data, format='JPEG')
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf8')

    results = classify_image(image)
    return render_template('ResultsPages/BrainTumerRes.html', image=image_base64, results=results)


@app.route('/DiabeticRes' , methods=['POST'])
def DiabeticRes():
    image_file = request.files['image']
    image = Image.open(image_file)

    image_data = io.BytesIO()
    image.save(image_data, format='PNG')
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf8')

    results = classify_DR(image)
    return render_template('ResultsPages/DiabeticRes.html', image=image_base64, results=results)

@app.route('/LungCancerRes' , methods=['POST'])
def LungCancerRes():
     image_file = request.files['image']
     image = Image.open(image_file)

     image_data = io.BytesIO()
     image.save(image_data, format='JPEG') 
     image_base64 = base64.b64encode(image_data.getvalue()).decode('utf8')

     results = classify_lung(image)
     return render_template('ResultsPages/LungCancerRes.html' , image=image_base64, results=results)

@app.route('/LeukemiaRes' , methods=['POST'])
def LeukemiaRes():
    image_file = request.files['image']
    image = Image.open(image_file)

    image_data = io.BytesIO()
    image.save(image_data, format='JPEG') 
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf8')

    results = classify_leukemia(image)

    return render_template('ResultsPages/LeukemiaRes.html' , image=image_base64, results=results)





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
            user_type VARCHAR(50) NOT NULL
        )
        ''')
        conn.commit()
    app.run(port=2000, debug=True)