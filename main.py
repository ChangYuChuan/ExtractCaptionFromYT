from flask import Flask, request, Response
from flask_cors import CORS
import ytCaptionReader
from mysqlObj import mysqlObj
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/YoutubeCaption', methods=['POST'])
def get_vocabularies_by_video_id():
    '''get the vocabularies by video id'''
    try:
        print('get_vocabularies_by_video_id has been called ')
        body = request.get_json()

        # In comprison with the query, the format of the body is originaly json. Therefore, there is no need of transforming it to json.
        user_id = body['user_id']
        video_id = body['video_id']
        if(user_id is None or user_id == '' or video_id is None or video_id == ''):
            return Response("Input values are invalid.", status=400, mimetype='application/json')
        
        result = ytCaptionReader.extract_vocabularies_from_yt(user_id, video_id)

        if(len(result) == 0):
            return Response("Data not found", status=404, mimetype='application/json')
        #return result
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response("Receive exception. {0}".format(ex), status=500, mimetype='application/json')

@app.route('/api/YoutubeCaption/Stopwords', methods=['POST'])
def set_stop_words_with():
    '''Upload stopwords to database. stopwords are the words that user have learned and don't need to be extract from video.'''
    try:
        body = request.get_json()
        # In comprison with the query, the format of the body is originaly json. Therefore, there is no need of transforming it to json.
        user_id = body['user_id']
        stopwords = body['stopwords']
        if(user_id is None or user_id == '' or stopwords is None or stopwords == ''):
            return Response("Input values are invalid.", status=400, mimetype='application/json')
        
        mydb = mysqlObj()
        mydb.set_customized_stopwords(stopwords,user_id)
        mydb.close()
        
        return Response('Stopwords has been created', status=201, mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response("Receive exception. {0}".format(ex), status=500, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)