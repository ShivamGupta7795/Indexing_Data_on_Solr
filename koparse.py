# --*-- Encoding: UTF-8 --*--
import re
import json
from ttp import ttp
from nltk.corpus import stopwords
import string
import jsonpickle
from many_stop_words import get_stop_words
import time
import pytz
from datetime import datetime
from time import time
from dateutil import parser

# stop_corpus = set(stopwords.words('english'))

#from konlpy.tag import Twitter; t = Twitter()
stop_corpus = get_stop_words('kr')
p = ttp.Parser()

def remove_remaining_punctuations(text):
    for c in string.punctuation:
        text = text.replace(c, '')

    return text

def remove_stop_words(text, stop_corpus):
    # text = ' '.join([i for i in text.lower().split() if i not in stop_corpus])
    text = ' '.join([i for i in text.lower().split() if i not in stop_corpus])
    return text


def emo_recognizer(text):
    emoji_pattern = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])+', 
        re.UNICODE)

    emojis = re.findall(emoji_pattern, text)
    text = emoji_pattern.sub(r'',text)
    emoticons = re.findall(r'(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
    text = remove_remaining_punctuations(text)
    text = remove_stop_words(text, stop_corpus)
    return emojis, emoticons, text

def remove_twitter_entities(text):
    result = p.parse(text)
    for entity in result.users:
        text = text.replace('@'+entity, '')
    for entity in result.tags:
        text = text.replace('#'+entity, '')
    for entity in result.urls:
        text = text.replace(entity, '')
    return result.users, result.tags, result.urls, text

def remove_entities_korean(text, entities):
    hashtags = [] 
    if entities['hashtags']:
        for entity in entities['hashtags']:
            hashtag = entity['text']
            hashtags.append(hashtag) 
            text = text.replace(hashtag, '')
    return hashtags, text

def main():
    duplicate_list = []
    with open('politics_ko.json', 'r') as f:
        for line in f:
            data = json.loads(line)
            if data['id'] not in duplicate_list:
                duplicate_list.append(data['id'])
                user_mentions, hashtags, urls, tweet_txt = remove_twitter_entities(data['text'])
                hashtags_ko, tweet_txt = remove_entities_korean(tweet_txt, data['entities'])
                emojis, emoticons, tweet_txt = emo_recognizer(tweet_txt)
                date_str = data['created_at']
                date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
                date_obj = date_obj.strftime('%Y-%m-%dT%H:00:00Z')
                #date_obj = time.strftime("%Y-%m-%d", time.strptime(date_str,'%a %b %d %H:%M:%S +0000 %Y'))
                #date_obj = datetime.datetime.strptime(date_obj, '%Y-%m-%d').date()
                data['tweet_date'] = date_obj
                data['tweet_lang'] = data.pop('lang')
                data['tweet_text'] = data.pop('text')
                data['text_ko'] = tweet_txt
                data['hashtags'] = list(set(hashtags + hashtags_ko))
                data['mentions'] = user_mentions
                data['tweet_urls'] = urls
                data['tweet_emoticons'] = emojis + emoticons
                data['topic'] = 'politics'
                with open('politics_ko_indexer.json', 'a') as fw:
                    fw.write(jsonpickle.encode(data, unpicklable=False) + '\n')
                print ("Original: ")
                print (data['tweet_text'])
                print ("Formatted: ")
                print (tweet_txt + '\n')
  #  print len(duplicate_list)

main()