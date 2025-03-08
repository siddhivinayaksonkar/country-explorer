from flask import Flask, render_template, request, jsonify
from country import CountryExplorer
import os

app = Flask(__name__)
explorer = CountryExplorer()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/compare', methods=['POST'])
def compare_countries():
    """API endpoint to compare two countries."""
    try:
        data = request.get_json()
        first_country = data.get('country1', '').strip()
        second_country = data.get('country2', '').strip()

        if not first_country or not second_country:
            return jsonify({
                'error': 'Please provide both country names'
            }), 400

        # Clean country names
        first_country = explorer.clean_country_name(first_country)
        second_country = explorer.clean_country_name(second_country)

        # Fetch country data
        first_data = explorer.fetch_country_info(first_country)
        second_data = explorer.fetch_country_info(second_country)

        if not first_data or not second_data:
            return jsonify({
                'error': 'Could not fetch data for one or both countries'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'country1': {
                    'name': first_country,
                    'data': first_data
                },
                'country2': {
                    'name': second_country,
                    'data': second_data
                }
            }
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    # Run the app, listening on all available interfaces
    app.run(host='0.0.0.0', port=port) 