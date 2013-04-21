# -*- coding: utf-8 -*-

from lib.graph import *
import io, argparse, urllib, urllib2, json, pickle
import pprint

TOPLEVEL_CATEGORY = "Category:History of computer science"
TOPLEVEL_CATEGORY_ID = 30730499

endpoint = 'http://en.wikipedia.org/w/api.php'
parameters = {'format' : 'json',
              'action' : 'query',
              #'prop' : 'revisions',
              #'rvprop' : 'content',
              'prop' : 'links|categories',
              'cllimit' : 500,
              'pllimit' : 500,
              'plnamespace' : 0,
              #'prop' : 'extracts',
              #'exsectionformat' : 'raw',
              #'exintro' : '1',
              'redirects' : True}

crawled_articles = []
categories = set([TOPLEVEL_CATEGORY])

def main(args):
    get_child_categories(TOPLEVEL_CATEGORY_ID)

    graph = Graph(crawl(args.start))

    pickle.dump(graph, open('data/wikipedia.pkl', 'wb'), -1)

def crawl(title):
    parameters["titles"] = title
    crawled_articles.append(title)

    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(encode_dict(parameters)))))
    page = response[u'query'][u'pages'].values()[0]

    #pprint.pprint(response)

    if u'missing' in page:
        return None
    else:
        adjacent_nodes = []

        for link in page[u'links']:
            print link[u'title']
            if link[u'title'] not in crawled_articles and is_in_categories(page[u'categories']):
                print "ACCEPTED"
                node = crawl(link[u'title'])
                if node:
                    adjacent_nodes.append(crawl(link[u'title']))
            else:
                print "REJECTED"

        return Node({"title": page[u'title'] , "id": page[u'pageid']}, adjacent_nodes)

def is_in_categories(page):
    for category in page:
        if category[u'title'] in categories:
            return True
    return False

def get_child_categories(category_id):
    query_parameters = {'format': 'json',
                        'action': 'query',
                        'list': 'categorymembers',
                        'cmpageid': category_id,
                        'cmtype': 'subcat',
                        'cmlimit': 500}
    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(query_parameters))))

    #pprint.pprint(response)

    for category in response[u'query'][u'categorymembers']:
        if category[u'title'] not in categories:
            #print category[u'title']
            categories.add(category[u'title'])
            get_child_categories(category[u'pageid'])

def encode_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="initial article to start crawling")
    args = parser.parse_args()

    main(args)
