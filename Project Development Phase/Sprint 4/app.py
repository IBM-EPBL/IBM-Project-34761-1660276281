from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from twilio.rest import Client
import math

app = Flask(__name__)

dic = {0 : 'forest', 1 : 'with fire'}

model = load_model('forests.h5')

model.make_predict_function()

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(128,128))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 128,128,3)
    account_sid='AC33e4f23328753859047817ac8815083b'
    auth_token ='ec85f2a8b7e067400404fd9c0c565797'
    client=Client(account_sid,auth_token)
    pred= model.predict(i)
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