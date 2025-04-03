from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GRAPHQL_URL = "https://graph.imdbapi.dev/v1"

# set your custom port
PORT = 5005

@app.route('/')
def index():
    return render_template('index.html')

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
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            return jsonify({"error": data['errors']}), 500

        rating = data['data']['title']['rating']['aggregate_rating']
        return jsonify({"rating": rating})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except (KeyError, TypeError) as e:
        return jsonify({"error": f"Invalid response from GraphQL API: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
