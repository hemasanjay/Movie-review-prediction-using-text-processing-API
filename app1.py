from flask import Flask, request, render_template
import numpy as np
import re
import requests
import json

app = Flask(__name__)
def check(output):
    url =  "https://japerk-text-processing.p.rapidapi.com/sentiment/"
    payload = {"text": output}
    print(payload)
    headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-key': "44a7c18307msh931d433113c080fp1b65a3jsn1dd6d955125e",
    'x-rapidapi-host': "japerk-text-processing.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    value = response.text
    output=json.loads(value)
    return response.json()
#home page
@app.route('/')
def summarizer():
    return render_template('summarizer.html')

#summarizer page
@app.route('/summarize',  methods=['POST'])
def summarize():
    output = request.form['output']
    output=re.sub("[^a-zA-Z.,]"," ",output)
    print(output)
    essay = check(output)
    print(type(essay['label']))
    if essay['label'] == "pos":
        output="Positive review"
    elif essay['label'] == "neg":
        output="Negative review"
    else:
        output="Neutral Review"
    #print(max(essay['probability'], key=essay.get))
    return render_template('summary.html',essay=essay,prediction_text='{}'.format(output))
    
if __name__ == "__main__":
    app.run(debug=True)
