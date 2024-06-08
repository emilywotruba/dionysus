from flask import Flask
from flask import render_template
from flask import request
from simplejustwatchapi.justwatch import search
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
        return render_template("result.html", data=data)

@app.route("/show", methods = ['GET'])
def show():
    if request.method == 'GET':
        countries = {
            "AF", "AL", "DZ", "AD", "AO",
            "AG", "AR", "AM", "AU", "AT",
            "AZ", "BS", "BH", "BD", "BB",
            "BY", "BE", "BZ", "BJ", "BT",
            "BO", "BA", "BW", "BR", "BN",
            "BG", "BF", "BI", "CV", "KH",
            "CM", "CA", "CF", "TD", "CL",
            "CN", "CO", "KM", "CG", "CR",
            "HR", "CU", "CY", "CZ", "KP",
            "CD", "DK", "DJ", "DM", "DO",
            "EC", "EG", "SV", "GQ", "ER",
            "EE", "SZ", "ET", "FJ", "FI",
            "FR", "GA", "GM", "GE", "DE",
            "GH", "GR", "GD", "GT", "GN",
            "GW", "GY", "HT", "HN", "HU",
            "IS", "IN", "ID", "IR", "IQ",
            "IE", "IL", "IT", "JM", "JP",
            "JO", "KZ", "KE", "KI", "KW",
            "KG", "LA", "LV", "LB", "LS",
            "LR", "LY", "LI", "LT", "LU",
            "MG", "MW", "MY", "MV", "ML",
            "MT", "MH", "MR", "MU", "MX",
            "FM", "MC", "MN", "ME", "MA",
            "MZ", "MM", "NA", "NR", "NP",
            "NL", "NZ", "NI", "NE", "NG",
            "MK", "NO", "OM", "PK", "PW",
            "PA", "PG", "PY", "PE", "PH",
            "PL", "PT", "QA", "KR", "MD",
            "RO", "RU", "RW", "KN", "LC",
            "VC", "WS", "SM", "ST", "SA",
            "SN", "RS", "SC", "SL", "SG",
            "SK", "SI", "SB", "SO", "ZA",
            "SS", "ES", "LK", "SD", "SR",
            "SE", "CH", "SY", "TW", "TJ",
            "TZ", "TH", "TL", "TG", "TO",
            "TT", "TN", "TR", "TM", "TV",
            "UG", "UA", "AE", "GB", "US",
            "UY", "UZ", "VU", "VE", "VN",
            "YE", "ZM", "ZW"
        }
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
                        "provider_friendly": offer.package.name + " " + offer.monetization_type,
                        "provider_id": offer.package.technical_name,
                        "monetization_type": offer.monetization_type,
                        "countries": [{
                            "name": ctr.name,
                            "flag": ctr.flag,
                            "price": offer.price_string,
                            "type": offer.type
                        }],
                        "url": offer.url
                    }
        return render_template("show.html", data=out)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')