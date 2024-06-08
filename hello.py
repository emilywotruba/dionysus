from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from simplejustwatchapi.justwatch import (
    search,
    details,
    offers_for_countries
)
import pycountry
import yaml

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
        id = request.args.get("id")

        data = offers_for_countries(id, countries=country_codes)

        providers_known = {}
        providers_unknown = {}

        for country in country_codes:
            ctr = pycountry.countries.get(alpha_2=country)

            for offer in data[country]:
                key = offer.package.technical_name + "_" + offer.monetization_type
                is_my_service = offer.package.technical_name in settings["providers"]

                if key in (providers_known if is_my_service else providers_unknown):
                    (providers_known if is_my_service else providers_unknown)[key]["countries"].append({
                        "name": ctr.name,
                        "flag": ctr.flag,
                        "price": offer.price_string,
                        "type": offer.type
                    })
                else:
                    (providers_known if is_my_service else providers_unknown)[key] = {
                        "provider_friendly": offer.package.name + " (" + offer.monetization_type + ")",
                        "provider_id": key,
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

        providers_known = dict(sorted(
            providers_known.items(), 
            key=lambda item: item[1]["provider_friendly"]))
        providers_unknown = dict(sorted(
            providers_unknown.items(),
            key=lambda item: item[1]["provider_friendly"]))
        
        return render_template(
            "show.html", 
            providers_known=providers_known, 
            providers_unknown=providers_unknown,
            name=details(id).title)

@app.route("/api", methods=['GET'])
def api():
    return jsonify({})

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        settings = yaml.safe_load(f)

    country_codes = set()
    for country in pycountry.countries:
        country_codes.add(country.alpha_2)

    app.run(debug=True, port=5000, host='0.0.0.0')