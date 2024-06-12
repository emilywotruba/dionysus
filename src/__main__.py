from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from simplejustwatchapi import justwatch
import pycountry
import yaml

app = Flask(__name__)


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

        return render_template(
            "show.html",
            providers_known=providers_known,
            providers_unknown=providers_unknown,
            name=justwatch.details(id).title,
        )


def create_entry(ctr, offer):
    return dict(
        {
            "name": ctr.name,
            "flag": ctr.flag,
            "price": offer.price_string,
            "type": offer.type,
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
    with open("./static/config.yaml", "r") as f:
        settings = yaml.safe_load(f)

    country_codes = set()
    for country in pycountry.countries:
        country_codes.add(country.alpha_2)

    app.run(
        debug=True,
        port=5000,
        host=settings["host"]
    )
