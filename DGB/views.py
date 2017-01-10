# coding=utf-8
from flask import Flask, render_template, flash, request, jsonify
import json
from flask_cors import CORS, cross_origin
from forms import *
from orm import *
from flask_bootstrap import Bootstrap
from config import BASE_URL, SECRET_KEY
import pdb

app = Flask(__name__, static_url_path=BASE_URL + '/static')
cors = CORS(app, resources={r"/api/": {"origins": "*"}})
app.secret_key = SECRET_KEY
Bootstrap(app)

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
            dataset = request.form['dataset']

            # The following lines determine which tables get shown on the output page.
            # Here, we initially define L1000 and CREEDS as booleans that will tell us which output to display.
            L1000 = False
            CREEDS = False
            if dataset == 'L1000' or dataset == 'Both':
                L1000 = True
            if dataset == 'CREEDS' or dataset == 'Both':
                CREEDS = True

            if L1000:
                result = lincs_rows(symbol, expression)
                rows = result[0]
                ldeciles = result[1]
                pattern = result[2]
            if CREEDS:
                result = creeds_rows(symbol, expression)
                creedsrows = result[0]
                cdeciles = result[1]
                pattern = result[2]

            # Here, we create a boolean called upregulated because jinja if statements can only test true/false
            upregulated = False
            if pattern == 'Up-Regulated':
                upregulated = True

            # Concatenate a string which will hyperlink the gene symbol to its respective Harmonizome page.
            gene_url = 'http://amp.pharm.mssm.edu/Harmonizome/gene/' + symbol
            # Determine which datasets to send to the output page in order to draw the tables.

            if dataset == 'L1000':
                return render_template('output.html', form=form, symbol=symbol, rows=rows, pattern=pattern, L1000=L1000,
                                       CREEDS=CREEDS, gene_url=gene_url, upregulated=upregulated, ldeciles=ldeciles)
            elif dataset == 'CREEDS':
                return render_template('output.html', form=form, symbol=symbol,
                                       creedsrows=creedsrows, pattern=pattern, L1000=L1000, CREEDS=CREEDS,
                                       gene_url=gene_url, upregulated=upregulated, cdeciles=cdeciles)
            elif dataset == 'Both':
                return render_template('output.html', form=form, symbol=symbol, rows=rows, creedsrows=creedsrows,
                                       pattern=pattern, L1000=L1000, ldeciles=ldeciles, CREEDS=CREEDS,
                                       cdeciles=cdeciles, gene_url=gene_url, upregulated=upregulated)

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
@app.route(BASE_URL + '/api/v1/', methods = ['GET', 'POST'])
def api_res():
    if request.method == 'GET':
        myDict = {'a': 7, 'b': 6}
        return jsonify(**myDict)
    elif request.method == 'POST':
        jsonData = request.get_json()
        symbol = jsonData['symbol']
        expression = jsonData['expression']
        dataset = jsonData['dataset']

        if (dataset == 'L1000'):
            res = combined_dataset_query(symbol, expression, dataset)
        elif (dataset == 'CREEDS'):
            res = combined_dataset_query(symbol, expression, dataset)
        else:
            res = find_both(symbol, expression)

        return jsonify(results=res)

if __name__ == '__main__':
    app.run(debug=True)
