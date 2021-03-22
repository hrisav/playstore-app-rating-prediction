from flask import Flask, render_template, request
import pickle
import numpy as np
import datetime
import pandas as pd

model = pickle.load(open('playstore_rating.pkl', 'rb'))  # opening pickle file in read mode

app = Flask(__name__)  # initializing Flask app


@app.route("/",methods=['GET'])
def hello():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        d1 = request.form['Category']
        if d1 == 'ART_AND_DESIGN':
            d1 = 0
        elif (d1 == 'AUTO_AND_VEHICLES'):
            d1 = 1
        elif (d1 == 'BEAUTY'):
            d1 = 2
        elif (d1 == 'BOOKS_AND_REFERENCE'):
            d1 = 3
        elif (d1 == 'BUSINESS'):
            d1 = 4
        elif (d1 == 'COMICS'):
            d1 = 5
        elif (d1 == 'COMMUNICATION'):
            d1 = 6
        elif (d1 == 'DATING'):
            d1 = 7
        elif (d1 == 'EDUCATION'):
            d1 = 8
        elif (d1 == 'ENTERTAINMENT'):
            d1 = 9
        elif (d1 == 'EVENTS'):
            d1 = 10
        elif (d1 == 'FAMILY'):
            d1 = 11
        elif (d1 == 'FINANCE'):
            d1 = 12
        elif (d1 == 'FOOD_AND_DRINK'):
            d1 = 13
        elif (d1 == 'GAME'):
            d1 = 14
        elif (d1 == 'HEALTH_AND_FITNESS'):
            d1 = 15
        elif (d1 == 'HOUSE_AND_HOME'):
            d1 = 16
        elif (d1 == 'LIBRARIES_AND_DEMO'):
            d1 = 17
        elif (d1 == 'LIFESTYLE'):
            d1 = 18
        elif (d1 == 'MAPS_AND_NAVIGATION'):
            d1 = 19
        elif (d1 == 'MEDICAL'):
            d1 = 20
        elif (d1 == 'NEWS_AND_MAGAZINES'):
            d1 = 21
        elif (d1 == 'PARENTING'):
            d1 = 22
        elif (d1 == 'PERSONALIZATION'):
            d1 = 23
        elif (d1 == 'PHOTOGRAPHY'):
            d1 = 24
        elif (d1 == 'PRODUCTIVITY'):
            d1 = 25
        elif (d1 == 'SHOPPING'):
            d1 = 26
        elif (d1 == 'SOCIAL'):
            d1 = 27
        elif (d1 == 'SPORTS'):
            d1 = 28
        elif (d1 == 'TOOLS'):
            d1 = 29
        elif (d1 == 'TRAVEL_AND_LOCAL'):
            d1 = 30
        elif (d1 == 'VIDEO_PLAYERS'):
            d1 = 31
        else:
            d1 = 32
        d2 = request.form['Reviews']
        d3 = request.form['Installs']
        d4 = request.form['Price']
        d4 = d4.strip('$')
        d4 = float(d4)
        d5 = request.form['Current_Ver_Upd']
        d6 = request.form['Android_Ver_Upd']
        d7 = request.form['Size_Upd']
        d8 = request.form['Last_Updated_Days']
        temp = pd.to_datetime(d8)
        result = datetime.datetime.now() - temp
        d8 = result.days
        d9 = request.form['Content_Rating']
        if d9 == 'Everyone':
            d9 = 1
        elif (d9 == 'Everyone 10+'):
            d9 = 2
        elif (d9 == 'Teen'):
            d9 = 3
        else:
            d9 = 4
        d10 = request.form['Type']
        if (d10 == 'Free'):
            d10 = 0
        else:
            d10 = 1

        arr = np.array([[d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]])
        pred = model.predict(arr)
        appname = request.form['App_Name']
        return render_template('index.html', prediction_text='RESULT - Rating for the app {0} is {1}.'.format(appname, round(pred[0],2)))
    else:
        return render_template('index.html')

#app.run(debug=True)             #run on local system
app.run(host="0.0.0.0")          #deploy
