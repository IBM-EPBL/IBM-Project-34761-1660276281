from flask import Flask, render_template, request
from keras.models import load_model
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from twilio.rest import Client
import math

app = Flask(__name__)

dic = {0 : 'forest', 1 : 'with fire'}

model = load_model('forests.h5')

model.make_predict_function()

def predict_label(img_path):
    i = cv2.imread(img_path)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    img = Image.open(img_path)
    img = img.resize((128,128))
    x = img_to_array(img)
    x = np.expand_dims(x,axis=0)
    account_sid='AC33e4f23328753859047817ac8815083b'
    auth_token ='778340e32fc81ce5fc2f1061ad1791f9'
    client=Client(account_sid,auth_token)
    pred= model.predict(x)
    if(pred==[[1.]]):
      message=client.messages \
      .create(
          body='FOREST FIRE IS DECTECTED IN AREA,stay alert',
          #use twilio free number
          from_='+12535288281',
          #to number
          to='+918610505460')
      msg= " FOREST FIRE DETECTED" 
    else:
      msg= "NO FOREST FIRE DETECTED" 
    return msg


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("home.html")

@ app.route('/index', methods=['GET', 'POST']) # routes to the index html
def index():
    return render_template("index.html")

@app.route("/about")
def about_page():
	return "This website helps in forest fire detection..!!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)