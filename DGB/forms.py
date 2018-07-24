from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms import validators  # ValidationError

class GeneForm(Form):
    symbol = StringField("Gene Symbol", [validators.DataRequired("Please enter a gene symbol.")])
    # expression = SelectField("In which direction would you like to affect expression of the target gene?",
    #                         [validators.data_required("Please choose up or down")],
    #                         choices=[('Up-Regulate', 'Up-Regulate'), ('Down-Regulate', 'Down-Regulate')],
    #                         default='Up-Regulate')
    submit = SubmitField("Find a list of prioritized small molecules")
