from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from simplejustwatchapi import justwatch
import pycountry
import yaml
import os

app = Flask(__name__)

default_settings = {
        "host": "0.0.0.0",
        "port": "5000"
    }

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/result", methods=["GET"])
def result():
    if request.method == "GET":
        name = request.args.get("name")
        language = request.args.get("lang", default=settings["language"])
        
        data = justwatch.search(
            name,
            language=language,
            country=settings["country"],
            count=settings["result_count"],
        )

        return render_template(
            "result.html",
            data=data,
            name=name
        )


@app.route("/show", methods=["GET"])
def show():
    if request.method == "GET":
        id = request.args.get("id")
        language = request.args.get("lang", default=settings["language"])

        data = justwatch.offers_for_countries(
            id,
            countries=country_codes,
            language=language
        )

        providers_known = {}
        providers_unknown = {}

        for country in country_codes:
            ctr = pycountry.countries.get(alpha_2=country)

            for offer in data[country]:
                key = "{}_{}".format(
                    offer.package.technical_name,
                    offer.monetization_type
                )

                if offer.package.technical_name in settings["providers"]:
                    providers = providers_known
                else:
                    providers = providers_unknown

                if key in providers:
                    providers[key]["countries"].append(create_entry(ctr, offer))
                else:
                    providers[key] = dict(
                        {
                            "provider_friendly": "{} ({})".format(
                                offer.package.name, 
                                offer.monetization_type
                            ),
                            "provider_id": key,
                            "monetization_type": offer.monetization_type,
                            "countries": [create_entry(ctr, offer)],
                            "url": offer.url,
                            "icon": offer.package.icon,
                        }
                    )

        for providers in [providers_known, providers_unknown]:
            providers = dict(
                sorted(
                    providers.items(),
                    key=lambda item: item[1]["provider_friendly"]
                )
            )

            for key in providers:
                providers[key]["countries"] = sorted(
                    providers[key]["countries"],
                    key=lambda item: (-item["elements"], item["name"]),
                )
                
                providers[key]["has_price"] = False
                providers[key]["has_elements"] = False
                
                for ctr in providers[key]["countries"]:
                    if ctr["price"] != None and ctr["price"] != 0:
                        providers[key]["has_price"] = True
                    if ctr["elements"] != None and ctr["elements"] != 0:
                        providers[key]["has_elements"] = True

        return render_template(
            "show.html",
            providers_known=providers_known,
            providers_unknown=providers_unknown,
            name=justwatch.details(id).title
        )


def create_entry(ctr, offer):
    return dict(
        {
            "name": ctr.name,
            "flag": ctr.flag,
            "price": offer.price_string,
            # "type": offer.type,
            "elements": offer.element_count,
        }
    )


@app.route("/api/search/", methods=["GET"])
def api_search():
    if request.method == "GET":
        name = request.args.get("name", default="")
        country = request.args.get("country", default="US")
        language = request.args.get("lang", default="en")

        result = justwatch.search(
            name,
            country=country,
            language=language
        )
        
        data = [r._asdict() for r in result]
        for i in range(1, len(data)):
            data[i].update({"raw": result[i].__repr__()})

        return jsonify(data)


if __name__ == "__main__":
    settings = {}

    # load default settings
    settings.update(default_settings)

    # load settings from config file
    with open("./static/config.yaml", "r") as f:
        settings.update(yaml.safe_load(f))

    # override settings by environment variables, if exists
    if 'DIONYSUS_HOST' in os.environ:
        settings["host"] = os.environ['DIONYSUS_HOST']
    if 'DIONYSUS_PORT' in os.environ:
        settings["port"] = os.environ['DIONYSUS_PORT']

    country_codes = set(
        [country.alpha_2 for country in pycountry.countries]
    )

    app.run(
        debug=True,
        port=settings["port"],
        host=settings["host"]
    )
