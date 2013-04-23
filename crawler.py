# -*- coding: utf-8 -*-

from lib.graph import *
import io, os, argparse, urllib, urllib2, json, pickle
import pprint

TOPLEVEL_CATEGORY = "Category:History of computer science"
TOPLEVEL_CATEGORY_ID = 30730499

CATEGORY_PATH = 'data/categories.pkl'

endpoint = 'http://en.wikipedia.org/w/api.php'
parameters = {'format' : 'json',
              'action' : 'parse',
              'prop' : 'links',
              'section' : 0,
              'redirects' : True}

crawled_articles = []
restrict_categories = set([TOPLEVEL_CATEGORY])

def main(args):
    global restrict_categories
    if os.path.exists(CATEGORY_PATH):
        restrict_categories = pickle.load(open(CATEGORY_PATH, 'rb'))
    else:
        get_child_categories(TOPLEVEL_CATEGORY_ID)
        pickle.dump(restrict_categories, open(CATEGORY_PATH, 'wb'), -1)

    graph = Graph(crawl(args.start))

    pickle.dump(graph, open('data/wikipedia.pkl', 'wb'), -1)

def crawl(title):
    parameters["page"] = title.encode('utf8')
    crawled_articles.append(title)

    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(parameters))))[u'parse']

    adjacent_nodes = []
    for link in response[u'links']:
        if link[u'*'] not in crawled_articles and link[u'ns'] == 0 and link[u'exists'] == u'':
            print link[u'*']
            query_parameters = {'format': 'json',
                                'action': 'query',
                                'prop': 'categories',
                                'titles': link[u'*'].encode('utf8'),
                                'cllimit': 500}
            categories = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(query_parameters))))[u'query'][u'pages'].values()[0]

            if u'categories' in categories and is_in_categories(categories[u'categories']):
                print "ACCEPTED"
                node = crawl(link[u'*'])
                if node:
                    adjacent_nodes.append(crawl(link[u'*']))
            else:
                print "REJECTED"

    return Node({"title": response[u'title']}, adjacent_nodes)

def is_in_categories(categories):
    for category in categories:
        if category[u'title'] in restrict_categories:
            return True
    return False

def get_child_categories(category_id):
    global restrict_categories
    query_parameters = {'format': 'json',
                        'action': 'query',
                        'list': 'categorymembers',
                        'cmpageid': category_id,
                        'cmtype': 'subcat',
                        'cmlimit': 500}
    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(query_parameters))))

    #pprint.pprint(response)

    for category in response[u'query'][u'categorymembers']:
        if category[u'title'] not in restrict_categories:
            #print category[u'title']
            restrict_categories.add(category[u'title'])
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
