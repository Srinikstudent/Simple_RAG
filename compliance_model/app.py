import psycopg2
import json
import numpy as np
import nlp
from flask import Flask, request
from numpy import nan
import joblib
import pandas as pd

# temporary database
cust_data = {
    'Sophia Campbell': {
        'CUSTOMER TYPE': ['INDIVIDUAL'],
        'CUSTOMER ACTIVITY': ['REMITTANCE'],
        'VALUE OF TRANSACTION': ['ABOVE 10,000 (NO LIMIT to an Account Transfer)'],
        'MEASURES REQUIRED': ['CDD AND EDD NEEDS TO BE PERFORMED'],
        'full_cust_names': ['Sophia Campbell'],
        'residential_address': ['51 boulevard Brune\n\n75689 Paris Cedex 14'],
        'source_of_funds': ['business'],
        'occ_business_act': nan,
        'purpose_of_transaction': ['Salary recieved'],
        'country_of_citizenship': ['USA'],
        'country_of_residence': ['USA'],
        'address_of_company': nan,
        'principal_place_of_operation': nan,
        'nature_of_business_by_the_company': nan,
        'type_of_company': nan,
        'type_of_trust': nan,
        'country_of_establishment': nan,
        'any_trustee_is_individual_or_company': nan,
        'full_address_of_head_office': nan,
        'unique_identification_number': nan,
        'State_Country_Territory_of_incorporation': nan,
        'date_of_incorporation': nan,
        'objects_of_entity': nan,
        'name_of_chairman': nan,
        'info_in_official_exchange': nan,
        'info_in_domestic_exchange': nan
    },
    #166
    'Verma Industries': {
        'CUSTOMER TYPE': ['A TRADER/BUSINESS ENTITY'],
        'CUSTOMER ACTIVITY': ['REMITTANCE'],
        'VALUE OF TRANSACTION': ['ANY AMOUNT'],
        'MEASURES REQUIRED': ['CDD AND EDD NEEDS TO BE PERFORMED'],
        'full_cust_names': ['Verma Industries'],
        'residential_address': nan,
        'source_of_funds': nan,
        'occ_business_act': nan,
        'purpose_of_transaction': nan,
        'country_of_citizenship': nan,
        'country_of_residence': nan,
        'address_of_company': ['3/3 Park Street, Kolkata, West Bengal, 700016'],
        'principal_place_of_operation': ['Hong Kong'],
        'nature_of_business_by_the_company': ['Telephone Answering Services'],
        'type_of_company': ['proprietary'],
        'type_of_trust': nan,
        'country_of_establishment': nan,
        'any_trustee_is_individual_or_company': nan,
        'full_address_of_head_office': nan,
        'unique_identification_number': nan,
        'State_Country_Territory_of_incorporation': nan,
        'date_of_incorporation': nan,
        'objects_of_entity': nan,
        'name_of_chairman': nan,
        'info_in_official_exchange': nan,
        'info_in_domestic_exchange': nan
    },

    'Isabella Martinez': {
        'CUSTOMER TYPE': ['INDIVIDUAL'],
        'CUSTOMER ACTIVITY': ['REMITTANCE'],
        'VALUE OF TRANSACTION': ['ABOVE 10,000 (NO LIMIT to an Account Transfer)'],
        'MEASURES REQUIRED': ['CDD AND CDD NEEDS TO BE PERFORMED'],
        'full_cust_names': ['Isabella Martinez'],
        'residential_address': ['Summer Colony, Mussoorie, Uttarakhand, India'],
        'source_of_funds': ['carpentary services'],
        'occ_business_act': nan,
        'purpose_of_transaction': ['Funding home renovations'],
        'country_of_citizenship': ['australia'],
        'country_of_residence': ['United Kingdom'],
        'address_of_company': nan,
        'principal_place_of_operation': nan,
        'nature_of_business_by_the_company': nan,
        'type_of_company': nan,
        'type_of_trust': nan,
        'country_of_establishment': nan,
        'any_trustee_is_individual_or_company': nan,
        'full_address_of_head_office': nan,
        'unique_identification_number': nan,
        'State_Country_Territory_of_incorporation': nan,
        'date_of_incorporation': nan,
        'objects_of_entity': nan,
        'name_of_chairman': nan,
        'info_in_official_exchange': nan,
        'info_in_domestic_exchange': nan
    },
    #282
    'Kuznetsov Holdings': {
        'CUSTOMER TYPE': ['AN INCORPORATED ASSOCIATION'],
        'CUSTOMER ACTIVITY': ['REMITTANCE'],
        'VALUE OF TRANSACTION': ['ANY AMOUNT'],
        'MEASURES REQUIRED': ['CDD AND EDD NEEDS TO BE PERFORMED'],
        'full_cust_names': ['Kuznetsov Holdings'],
        'residential_address': nan,
        'source_of_funds': nan,
        'occ_business_act': nan,
        'purpose_of_transaction': nan,
        'country_of_citizenship': nan,
        'country_of_residence': nan,
        'address_of_company': nan,
        'principal_place_of_operation': nan,
        'nature_of_business_by_the_company': nan,
        'type_of_company': nan,
        'type_of_trust': nan,
        'country_of_establishment': nan,
        'any_trustee_is_individual_or_company': nan,
        'full_address_of_head_office': ['The Co-operative Bank - Balloon Street, Manchester, M60 4EP, United Kingdom'],
        'unique_identification_number': [5670956474],
        'State_Country_Territory_of_incorporation': ['France'],
        'date_of_incorporation': ['24/07/2003'],
        'objects_of_entity': ['Advancing the cooperative movement and promoting its values and principles.'],
        'name_of_chairman': ['Charlotte Myers'],
        'info_in_official_exchange': nan,
        'info_in_domestic_exchange': nan
    }
}

# function to check if prediction is 1 or 0
def is_value_present(memmap, value):
  for i in range(memmap.shape[0]):
    if memmap[i] == value:
      return True

  return False


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    target_id = request.headers.get('ID')

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="nocobase",
        user="postgres",
        password="binarySearchTree"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM compliance;")
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()

    feature_names = ['full_cust_names',
                     'residential_address',
                     'source_of_funds',
                     'occ_business_act',
                     'purpose_of_transaction',
                     'country_of_citizenship',
                     'country_of_residence',
                     'address_of_company',
                     'principal_place_of_operation',
                     'type_of_company',
                     'type_of_trust',
                     'country_of_establishment',
                     'full_address_of_head_office',
                     'State_Country_Territory_of_incorporation',
                     'date_of_incorporation',
                     'objects_of_entity',
                     'name_of_chairman',
                     'info_in_official_exchange',
                     'info_in_domestic_exchange',
                     'nature_of_business_by_the_company',
                     'any_trustee_is_individual_or_company']

    # convert tuple-data into dictionaries
    data_dict = []
    for vals in data:
        val = {}
        for col, value in zip(columns, vals):
            val[col] = value
        data_dict.append(val)
        
    nlp_output = []
    target_name = ""
    for vals in data_dict:
        if vals['id'] == int(target_id):
            compliance_input = vals['rules']
            output = nlp.extract_rules(compliance_input)
            nlp_output = output[0]
            target_name = output[1]

            df = pd.DataFrame(cust_data[target_name])

            for col in feature_names:
                if col not in nlp_output:
                    df[col] = 'NA'

            # drop the unnecessary columns
            df.drop(columns=['unique_identification_number',
            'VALUE OF TRANSACTION', 'CUSTOMER TYPE', 'CUSTOMER ACTIVITY'], axis=1, inplace=True)

            # replace all NA values with 'Not Available
            df.replace(to_replace=['NA', None],
                    value='Not Available', inplace=True)

            # reorder if necessary
            df = df.reindex(columns=feature_names)

            # map to label encoded values
            with open(f'/home/lab/compliance/compliance_model/models/label_encoders.joblib', 'rb') as file:
                le = joblib.load(file)
            for column in df.columns:
                df[column] = df[column].map(
                    lambda s: '<unknown>' if s not in le[column].classes_ else s)
                le[column].classes_ = np.append(
                    le[column].classes_, '<unknown>')
                df[column] = le[column].transform(df[column])

            # predict
            with open(f'/home/lab/compliance/compliance_model/models/compliance_le.sav', 'rb') as model_file:
                model = joblib.load(model_file)
            x = model.predict(df)

            # reconfigure the output
            is_fraud = ""
            if(is_value_present(x, 1)):
                is_fraud = "This transaction is not being processed"
            else:
                is_fraud = "This transaction is being processed"

            cursor.execute("UPDATE compliance SET flag = %s WHERE id = %s", (is_fraud, target_id))
            conn.commit()

    return "Predicted"


if __name__ == '__main__':
    app.run()
