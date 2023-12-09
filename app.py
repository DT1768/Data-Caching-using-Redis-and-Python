from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
import os
import redis 
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(
    host= os.getenv('REDIS_HOST'), 
    port=os.getenv('REDIS_PORT'), 
    password=os.getenv('REDIS_PASSWORD'))

client = MongoClient(os.getenv('MONGO_URL'))
db = client['sample_mflix']
comments_collection = db['comments']

@app.route('/topcomments', methods=['GET'])
def get_top_comments():
    year_from = int(request.args.get('year_from'))
    year_to = int(request.args.get('year_to'))
    top_n = int(request.args.get('top_n'))

    cache_key = f'top-{top_n}-{year_from}-{year_to}'

    cached_data = redis_client.hget('savedComments',cache_key)
    if cached_data:
        print('cached')
        return cached_data
    else:
        print('not cached')
        pipeline = [
            {
                '$lookup': {
                    'from': 'movies',
                    'localField': 'movie_id',
                    'foreignField': '_id',
                    'as': 'movie'
                },
            },
            {
                '$match': {
                    'movie.year': { '$gte': year_from, '$lte': year_to }
                }
            },
            {
                '$group': {
                    '_id': '$movie.title',
                    'total_comments': { '$sum': 1 },
                },
            },
            {
                '$sort': {
                    'total_comments': -1
                },
            },
            {
                '$limit': top_n,
            },
        ]

        result = list(comments_collection.aggregate(pipeline))

        result_json = json.dumps(result, default=str)


        redis_client.hset('savedComments',cache_key, result_json)

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)