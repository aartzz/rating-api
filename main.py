from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GRAPHQL_URL = "https://graph.imdbapi.dev/v1" # imdb unofficial api (imdbapi.dev)

@app.route('/rating', methods=['GET'])
def get_rating():
    title_id = request.args.get('id')
    if not title_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    query = """
    query titleById($id: ID!) {
      title(id: $id) {
        rating {
          aggregate_rating
        }
      }
    }
    """

    variables = {"id": title_id}

    try:
        response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables})
        response.raise_for_status()  # http error check
        data = response.json()

        if 'errors' in data:
            return jsonify({"error": data['errors']}), 500

        rating = data['data']['title']['rating']['aggregate_rating']
        return jsonify({"rating": rating})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid response from GraphQL API"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
