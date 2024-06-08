from flask import Flask
from flask import render_template
from flask import request
from simplejustwatchapi.justwatch import search
from simplejustwatchapi.justwatch import details
from simplejustwatchapi.justwatch import offers_for_countries
import pycountry

app = Flask(__name__)

@app.route("/")
def hello():
    data = search("house")
    return render_template("index.html", data=data)

@app.route("/result", methods = ['GET'])
def result():
    if request.method == 'GET':
        name = request.args.get("name")
        data = search(name)
        return render_template("result.html", data=data, name=name)

@app.route("/show", methods = ['GET'])
def show():
    if request.method == 'GET':
        countries = set()
        for country in pycountry.countries:
            countries.add(country.alpha_2)
        id = request.args.get("id")
        data = offers_for_countries(id, countries=countries)
        out = {}
        for country in countries:
            ctr = pycountry.countries.get(alpha_2=country)
            for offer in data[country]:
                key = offer.package.technical_name + "_" + offer.monetization_type
                if key in out:
                    out[key]["countries"].append({
                        "name": ctr.name,
                        "flag": ctr.flag,
                        "price": offer.price_string,
                        "type": offer.type
                    })
                else:
                    out[key] = {
                        "provider_friendly": offer.package.name + " (" + offer.monetization_type + ")",
                        "provider_id": offer.package.technical_name,
                        "monetization_type": offer.monetization_type,
                        "countries": [{
                            "name": ctr.name,
                            "flag": ctr.flag,
                            "price": offer.price_string,
                            "type": offer.type
                        }],
                        "url": offer.url,
                        "icon": offer.package.icon
                    }
        return render_template("show.html", data=out, name=details(id).title)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')