from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField

from wtforms import validators  # ValidationError


class GeneForm(Form):
    symbol = StringField("Gene Symbol", [validators.DataRequired("Please enter a gene symbol.")])
    expression = RadioField("Change in Expression?", [validators.data_required("Please choose up or down")],
                            choices=[('Up', 'Up-Regulated'), ('Down', 'Down-Regulated')])
    dataset = RadioField("Dataset", [validators.data_required("Please choose an option")],
                         choices=[('L1000', 'L1000'), ('CREEDS', 'CREEDS'), ('Both', 'Both')])
    submit = SubmitField("Send")
