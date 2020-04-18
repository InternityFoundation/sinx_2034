import pandas as pd
import flask
import json
from flask import jsonify # <- `jsonify` instead of `json`


def get_data():
    population=pd.read_csv("input_file_v1_dashboard.csv")
    ward_wise=pd.read_csv("Facilities_in_Mumbai_COVID_19_Cases.csv")
    ward_wise["Date Entered"]=ward_wise["Date Entered"].fillna(method='ffill')
    ward_wise=ward_wise.fillna(0)
    merged_data=ward_wise.merge(population[["Ward","Population"]],on="Ward",how="left")
    merged_data=merged_data.fillna(0)
    def probability_area(n1,n2,n3,p1):
        if p1==0:
            return 0
        else:
            return ((n1*1.5+n2*2.6+n3*3.6)/p1)*100
        
    merged_data["probability"]=merged_data.apply(lambda x: probability_area(x["Number of Cases- Standalone Structure"],x["Number of Cases- Medium Congested"],x["Number of Cases- Very Congested Area"],x["Population"]),axis=1)

    final_data=merged_data[merged_data["Date Entered"]=="11th April or Earlier"][["Ward","probability","Population"]][1:]
    return json.loads(final_data.to_json(orient='records'))

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return jsonify(get_data())

app.run(host="0.0.0.0",port="1234")