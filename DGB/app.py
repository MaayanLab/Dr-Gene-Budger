# coding=utf-8
from flask import Flask, render_template, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS, cross_origin
from forms import *
from config import BASE_URL, SECRET_KEY, DATABASE
from helpers import *
import pdb

app = Flask(__name__, static_url_path=BASE_URL + '/static')
# cors = CORS(app, resources={r"/api/": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SECRET_KEY'] = SECRET_KEY
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

            queries = get_rows(db.session, symbol)
            cmap_query = queries["cmap_query"]
            l1000_query = queries["l1000_query"]
            creeds_query = queries["creeds_query"]

            cmap_results = filter_by_expression(cmap_query, CmapAssociation, expression)
            l1000_results = filter_by_expression(l1000_query, L1000Association, expression)
            # min_max_p_val = l1000_result[1]

            creeds_results = filter_by_expression(creeds_query, CreedsAssociation, expression)

            return render_template('output.html',
            symbol=symbol,
            expression=expression,
            cmap_results=cmap_results,
            l1000_results=l1000_results,
            creeds_results=creeds_results
            )
            # return render_template('output.html',
            #     symbol=symbol,
            #     expression=expression,
            #     l1000_rows=l1000_rows,
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

# --------------------- Mobile API endpoint ---------------------
@app.route(BASE_URL + '/api/v1/', methods = ['POST'])
def api_res():
    if request.method == 'POST':
        jsonData = request.get_json()
        symbol = jsonData['symbol'].upper()

        queries = get_rows(db.session, symbol)
        cmap_query = map(lambda x: x.to_json(), queries["cmap_query"])
        l1000_query = map(lambda x: x.to_json(), queries["l1000_query"])
        creeds_query = map(lambda x: x.to_json(), queries["creeds_query"])

        return jsonify(l1000=l1000_query, creeds=creeds_query, cmap=cmap_query)

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
