from app import app
from flask import render_template, request, redirect, url_for, flash
from forms import EnterDrug
import json
import joblib

with open('tmp/drug_data.json', "r") as read_file:
    dict_of_drugs = json.load(read_file)

with open('tmp/targets_mappings.json', "r") as read_file:
    targets_mappings = json.load(read_file)

clf = joblib.load('tmp/model.pkl') 

@app.route('/', methods=['GET', 'POST'])
def enter_drug():
    form = EnterDrug()
    if form.validate_on_submit():
        drug = form.drug.data.upper()
        print(drug)
        # здесь логика базы данных
        print("\nData received. Now redirecting ...")
        if drug not in dict_of_drugs.keys():
            flash("Wrong drug name or no information about this drug in database")
            return redirect("/")
        return redirect(f"/{drug.replace(' ', '_')}")

    return render_template('enterdrug.html', form=form)

@app.route('/all_drugs')
def home():
    drugs = sorted(dict_of_drugs.keys())
    return render_template("all_drugs.html",
        title = 'All Drugs',
        drugs = drugs,
        links = {i: '/' + i.replace(' ', '_') for i in drugs}
    )


@app.route('/<drug_link>')
def drug_info(drug_link):
    drug = drug_link.replace('_', ' ')
    ADRs = dict_of_drugs[drug]['ADRs']
    return render_template("drug_ADRs.html",
        title = drug,
        drug = drug,
        link = 'predict/' + drug_link,
        ADRS = ADRs)

@app.route('/predict/<drug_link>')
def drug_prediction(drug_link):
    drug = drug_link.replace('_', ' ')
    vector = dict_of_drugs[drug]['ADR_vector']
    prediction = clf.predict([vector])
    targets = {}
    for target, num in zip(targets_mappings, prediction[0]):
        targets[target] = num
    return render_template("drug_prediction.html",
        title = f'{drug} targets',
        drug = drug,
        targets = targets)

