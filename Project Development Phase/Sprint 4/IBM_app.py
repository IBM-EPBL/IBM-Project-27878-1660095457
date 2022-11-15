from flask import Flask, render_template, redirect, url_for, request
import pickle
#import sklearn
import requests
API_KEY = "I5Gjqyr7Xvr46D-UieXVKehhCHj8FyaMruGt48hk_Lhf"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("index.html"))
            arr.append(float(val))
        Serial_No =1
        gre = float(request.form['gre'])
        tofel = float(request.form['tofel'])
        university_rating = float(request.form['university_rating'])
        sop = float(request.form['sop'])
        lor = float(request.form['lor'])
        cgpa = float(request.form['cgpa'])
        yes_no_radio = float(request.form['yes_no_radio'])

        X =[[gre,tofel,university_rating,sop,lor,cgpa,yes_no_radio]]

        payload_scoring = {"input_data": [{"field": [ "GRE Score",
                                "TOEFL Score",
                                "University Rating",
                                "SOP",
                                "LOR ",
                                "CGPA",
                                "Research"], "values": X}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5c4cbda7-5cf7-47a9-9a9a-a68d255aa19e/predictions?version=2022-11-14', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print(response_scoring)
        finaloutput=response_scoring.json()
        result=finaloutput['predictions'][0]['values'][0][0]
        #print(finaloutput)
        #result =finaloutput['values'][0][0]
        #print(result)
        if result == True:
            return render_template('chance.html')
        else:
            return render_template('noChance.html')
    else:
        return render_template("index.html")

@app.route("/home")
def demo():
    return render_template("index.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
