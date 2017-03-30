# coding=utf-8
from flask import Flask, render_template, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS, cross_origin
from forms import *
# from flask_bootstrap import Bootstrap
from config import BASE_URL, SECRET_KEY, DATABASE
from helpers import *
import pdb

app = Flask(__name__, static_url_path=BASE_URL + '/static')
# cors = CORS(app, resources={r"/api/": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SECRET_KEY'] = SECRET_KEY
# Bootstrap(app)
db = SQLAlchemy(app)

from models import *

@app.route(BASE_URL + '/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Create form and handle submissions.
        form = GeneForm(request.form)
        if not form.validate_on_submit():
            flash('All fields are required.')
            return render_template('home.html', form=form)
        elif symbol_validate(request.form['symbol']) is False:
            flash('Enter a valid gene symbol.')
            return render_template('home.html', form=form)
        else:
            symbol = request.form['symbol']
            expression = request.form['expression']

            cmap_result = get_cmap_rows(db.session, symbol, expression)
            # cmap_rows = cmap_result[0]

            lincs_result = get_lincs_rows(db.session, symbol, expression)
            # lincs_rows = lincs_result[0]
            # min_max_p_val = lincs_result[1]

            creeds_result = get_creeds_rows(db.session, symbol, expression)
            # creeds_rows = creeds_result[0]
            
            return render_template('results.html',
            cmap_length=len(cmap_result),
            l1000_length=len(lincs_result),
            creeds_length=len(creeds_result)
            )
            # return render_template('output.html',
            #     symbol=symbol,
            #     expression=expression,
            #     lincs_rows=lincs_rows,
            #     creeds_rows=creeds_rows,
            #     cmap_rows=cmap_rows,
            #     min_max_p_val=min_max_p_val #Used to calculate the opacity of dot
            # )

    else:
        form = GeneForm()
        return render_template('home.html', form=form)


@app.route(BASE_URL + '/layout/')
def layout():
    return render_template('layout.html')

@app.route(BASE_URL + '/documentation/')
def documentation():
    return render_template('documentation.html')

@app.route(BASE_URL + '/statistics/')
def statistics():
    return render_template('statistics.html')

# NOTE
# Mobile Side
# Accepts GET and POST requests and returns JSON
# Mobile App needs to send POST request to this app in JSON format
@app.route(BASE_URL + '/api/v1/', methods = ['POST'])
def api_res():
    if request.method == 'POST':
        jsonData = request.get_json()
        symbol = jsonData['symbol'].upper()
        expression = jsonData['expression'].upper()
        dataset = jsonData['dataset'].upper()

        if (dataset == 'L1000'):
            l1000 = dataset_query(symbol, expression, dataset)
            creeds = []
        elif (dataset == 'CREEDS'):
            l1000 = []
            creeds = dataset_query(symbol, expression, dataset)
        else:
            l1000 = dataset_query(symbol, expression, "L1000")
            creeds = dataset_query(symbol, expression, "CREEDS")
        return jsonify(l1000=l1000, creeds=creeds)

@app.route(BASE_URL + '/api/test/', methods = ['POST'])
def api_res2():
    if request.method == 'POST':
        return jsonify(hi=1, bye=2)

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
