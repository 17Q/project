# -*- coding: utf-8 -*-
import requests
import json
# from davidmeta.utils import logger

API_ENDPOINT = "https://api-v2launch.trakt.tv"
CLIENT_ID = "fc6d05ba4dd54c123e95cf19bee045d9c1dc4c799a4d47c18f8a583a2edd3e2b"
CLIENT_SECRET = "d96eac963563939e91608bc26064494bf483f2a2e180e88c1f5704ed66cb26ef"

def traktGetIDs(db_type, id_type, media_id):
    from davidmeta.metacache import cache_function
    if '_id' in id_type:
        id_type = id_type.split('_id')[0]
    string = "%s_%s_%s_%s" % ('traktGetIDs', db_type, id_type, str(media_id))
    url = "/search/%s/%s?type=%s" % (id_type, media_id, db_type)
    response = cache_function(getTrakt, string, url, 168)
    response = response[0].get(db_type, {}).get('ids', [])
    return response

def getTrakt(path):
    headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
    return requests.get("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=10)
