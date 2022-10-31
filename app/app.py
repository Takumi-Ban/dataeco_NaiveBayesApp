from flask import Flask, render_template, request, redirect, url_for
from flask import session as f_session
from model import Model
from initdb import ModelData
from dbsetting import session
import datetime

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/model', methods=['GET', 'POST'])
def model():
    model = Model()
    if request.method == 'GET':
        model.create_model()
        return render_template('model.html')
    else:
        global predtext
        predtext = str(request.form['predtext'])
        result = model.predict(predtext)
    return render_template('model.html', result=result)

@app.route('/insert', methods=['POST'])
def insert():
    global predtext
    label = request.form['cor_label']
    modeldb = ModelData()
    modeldb.class_ = str(label)
    modeldb.text = str(predtext)
    modeldb.time = datetime.datetime.now()
    session.add(modeldb)
    session.commit()
    session.close()
    return redirect(url_for('model'))

@app.route('/db', methods=['GET'])
def db():
    result = session.query(ModelData).all()
    result = [[i.id, i.class_, i.text, str(i.time)] for i in result]
    return render_template('history.html', results=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)