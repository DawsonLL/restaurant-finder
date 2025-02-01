# Based off Yelp API sample code
import os
from flask import Flask, request, jsonify, render_template
import requests
import pprint
import random
import logging

app = Flask(__name__)

# Grab the environment variable created during deployment
API_KEY = os.getenv('YELP_API_KEY')

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
SEARCH_LIMIT = 3


# Sends GET request to yelp API
def request_to_yelp(api_key, host, path, url_params=None):
	url_params = url_params or {}
	url = f"{host}{path}"
	headers = {
	'Authorization': f'Bearer {api_key}',
	}

	print(f"Querying {url} ...")

	response = requests.get(url, headers=headers, params=url_params)
	return response.json()


# Queries the yelp API based on user provided search term and location
def search(api_key, term, location):
	url_params = {
	'term': term.replace(' ', '+'),
	'location': location.replace(' ', '+'),
	'categories': 'restaurants', # Ensures that we only return restaurants when a user searches
	'limit': SEARCH_LIMIT
	}
	return request_to_yelp(api_key, API_HOST, SEARCH_PATH, url_params=url_params)

# Grab restaurant information
def get_business(api_key, business_id):
	business_path = BUSINESS_PATH + business_id
	return request_to_yelp(api_key, API_HOST, business_path)

# Renders the web page
@app.route('/')
def home():
	return render_template('index.html')


# Take user search term + location to return a restaurant
@app.route('/search', methods=['GET'])
def search_business():
	term = request.args.get('term', 'dinner')
	location = request.args.get('location', 'Portland, OR')
	response = search(API_KEY, term, location)
	businesses = response.get('businesses', [])

	if not businesses:
	    logging.warning("No restaurants found")
	    return jsonify({'error': 'No restaurants found'}), 404

	random_business = random.choice(businesses)
	business_id = random_business['id']
	business_info = get_business(API_KEY, business_id)

	# Pulling additional fields not originally in business info	
	business_info['description'] = random_business.get('categories', [{}])[0].get('title', 'No description available')     
	business_info['address'] = ', '.join(random_business['location']['display_address'])

	return jsonify(business_info)

if __name__ == '__main__':
	# Debugger left on to debug program
	app.run(debug=True)
