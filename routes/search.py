from flask import request, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
from modules.parse import parse_flibusta

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    
    if not isinstance(data, dict) or 'books' not in data or not isinstance(data['books'], list):
        return jsonify({"error": "Ожидался массив строк"}), 400

    results = []

    for query in data["books"]:
        result = parse_flibusta(query)

        if not isinstance(query, str):
            continue

        
        results.append({"query": query, "result": f"Тут запросы {result}"})


    return jsonify(results)