import os
from flask import Flask, request, session, render_template, jsonify
import pandas as pd
import threading
from PIL import Image
import PIL
import torch
from PrescriptionAnalysis import prescriptionanalysis
from pymongo import MongoClient
from TextProcessing import filter_word
from SideEffectThread import fetch_data_thread
from ReviewThread import process_reviews_thread
from DietPlan import generativedietplan
from PredictDisease import predictdisease
from transformers import BertModel

model = BertModel.from_pretrained("bert-base-uncased", torch_dtype=torch.float16, attn_implementation="sdpa")


client = MongoClient("mongodb+srv://vedesh:Vedeshsb003%40@user.8fwgqcw.mongodb.net/?retryWrites=true&w=majority&appName=user")
db = client.get_database('CTS_Hackathon')
users_collection = db.get_collection('User_Info')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')



def webdata(s):
    medicine=s
    s = filter_word(s)
    a = s[0]
    p = "https://www.drugs.com/sfx/" + a + "-side-effects.html"
    print(p)

    urls = [p, p]

    threads = []
    results = [None,[None,None]]
    for i, url in enumerate(urls):
        if i % 2 == 0:
            t = threading.Thread(target=lambda idx, u=url: results.__setitem__(idx, fetch_data_thread(u,a)), args=(i,))
        else:
            t = threading.Thread(target=lambda idx, u=url: results.__setitem__(idx, process_reviews_thread(u,a)), args=(i,))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    #visual=create_sentiment_bar_chart(results[1][1])
    return results[0], results[1][0],results[1][1],medicine

def dietplan(medicine_name,sideeffects,age,otherDiseases):
    return generativedietplan(medicine_name,sideeffects,age,otherDiseases)


@app.route('/home')
def home_main():
    return render_template('HomePage.html')

@app.route('/analyze', methods=['POST','GET'])
def analyze():
    drug_name = request.form.get("drug_name", "")
    side_effects, sentiment, review_summary,medicine = webdata(drug_name)
    results = {
        "side_effects": side_effects,
        "sentiment": sentiment,
        "review_summary": review_summary,
        "medicine": medicine
    }
    return render_template('Result.html', results=results)

@app.route('/blogpage')
def blog():
    return render_template('blog.html')

@app.route('/', methods=['GET', 'POST'])
def intro():
    return render_template('IntroPage.html')

@app.route('/login', methods=['GET','POST'])
def loginpage():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def login():
    msg = ''
    print(request.method)
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("hi")
        try:
            username = request.form['username']
            password = request.form['password']
            user = users_collection.find_one({'username': username})
            if user and user['password'] == password:
                session['loggedin'] = True
                session['username'] = user['username']
                print("hi")
                return render_template('HomePage.html')    
            else:
                msg = 'Incorrect username/password!'
        except:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')

@app.route('/Diet')
def diet():
    return render_template('DietPage.html')

@app.route('/dietresult', methods=['GET', 'POST'])
def dietresult():
    if request.method == 'POST':
        # Retrieve form data
        medicine_name = request.form.get('medicineName')
        sideeffects = request.form.get('sideEffects')
        age = request.form.get('age')
        otherDiseases = request.form.get('otherDiseases')

        # Print form data for debugging
        print(medicine_name, sideeffects, age, otherDiseases)

        # Assuming dietplan is a function that processes the data
        results = dietplan(medicine_name, sideeffects, age, otherDiseases)

        # Pass results to the HTML template
        return render_template('DietPage.html', results=results)
@app.route('/AnalyzePrescription',methods=['GET','POST'])
def analyzeprescription():
     if request.method == 'POST' and 'prescription' in request.files:
        input_file = request.files['prescription']
        
        # Define a path to save the uploaded file
        save_path = 'C:\\Users\\manas\\OneDrive\\Desktop\\Medview\\Prescriptionimg.png'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Create directory if it doesn't exist
        
        # Save the uploaded file
        input_file.save(save_path)
        
        # Analyze the saved prescription image
        results = prescriptionanalysis(save_path)
        
        # Render results on the page
        return render_template('Prescription Check Page.html', results=results)
     else:
         return "No prescription uploaded.", 400
    
@app.route("/doctor")
def doctor():
    return render_template('AI doc page.html')

@app.route("/predictdisease",methods=['GET','POST'])
def predictdiseaseroute():
    symptoms = request.form.getlist("inputs")
    if symptoms:
        print(symptoms)
        results= predictdisease(symptoms)
        return render_template('AI doc page.html',results=results)


@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('query', '')
    df = pd.read_csv('drug_name.csv') 
    suggestions = df[df['drugName'].str.contains(query, case=False, na=False)]['drugName'].tolist()
    return jsonify(suggestions)

@app.route('/logout')
def logout():
    """session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)"""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if users_collection.find_one({'username': username}) and users_collection.find_one({'password': password}):
            msg="User Already Exist!"
        else:
            users_collection.insert_one({'username': username, 'password': password,'email':email})
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('login.html', msg=msg)
@app.route('/Prescription')
def prescription():
    return render_template('Prescription Check Page.html')


@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    df = pd.read_csv("Disease_suggestion.csv")
    diseases = df['diseases'].tolist()
    query = request.args.get('query', '').lower()
    suggestions = [d for d in diseases if query in d.lower()]
    return jsonify(suggestions)



if __name__ == '__main__':
    app.run(debug=True)
