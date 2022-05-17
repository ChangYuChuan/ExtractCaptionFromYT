from youtube_transcript_api import YouTubeTranscriptApi
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import STOPWORDS
from collections import defaultdict
import re
from mysqlObj import mysqlObj


def extract_vocabularies_from_yt(user_id, video_id):
    if(video_id is None or video_id == ''):
        return {}
    # get traanscript, using youtube_transcript_api.
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    if(srt is None or len(srt) == 0):
        return {}
    # get customized_stopwords from database
    db = mysqlObj()
    customized_stopwords = db.get_customized_stopwords(user_id)
    db.close()
    my_stop_words = STOPWORDS.union(set(customized_stopwords))

    # declare default dictionary.
    list_result = []
    dict_result = defaultdict(list)

    for data in srt :
        # return the set called key_words which contains the non-stopwords vocabulariesc
        key_words = set(data['text'].split(' ')).difference(my_stop_words)
        # filter out the key_words which doesn't consist of characteristics.
        key_words = list(filter(lambda x: re.search("^[a-zA-Z]+$",x),key_words))

        # remove the number after point.
        timeStamp = int(data['start'])
        for word in key_words:
            dict_result[word].append(timeStamp)
            
    #transform from dictionary to list with word and timeStamp attributes
    for key in dict_result:
        list_result.append({'word':key,'timeStamp':dict_result[key]})
    return {'vocabularies':list_result, 'video_url': 'https://www.youtube.com/watch?v={0}'.format(video_id)}



def main():
    db = mysqlObj()
    db.set_customized_stopwords('winds','jimmychangtw')
    db.close()
    result = extract_vocabularies_from_yt('jimmychangtw','i9p-a8YJO-o')
    print(result)

if(__name__ == '__main__'):
	main()