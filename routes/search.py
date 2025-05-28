from flask import request, jsonify, Blueprint, Response
import requests
import json
from bs4 import BeautifulSoup
from modules.parse import parse_flibusta

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    
    if not isinstance(data, dict) or 'books' not in data or not isinstance(data['books'], list):
        return Response(
            json.dumps({"error": "Ожидался массив строк"}, ensure_ascii=False),
            status=400,
            content_type="application/json"
        )
    results = []

    for query in data["books"]:
        result = parse_flibusta(query)
        

        if not isinstance(query, str):
            continue

        results.append({
            "query": query, 
            "result": result.model_dump() if result else None
        })


    return Response(
        json.dumps(results, default=str, ensure_ascii=False),
        content_type="application/json"
    )

@search_blueprint.route("/search", methods=["GET"])
def test():
    return jsonify({"result": "hello world"})