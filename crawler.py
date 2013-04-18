# -*- coding: utf-8 -*-

from lib.graph import *
import io, argparse, urllib, urllib2, json
import pprint

endpoint = 'http://en.wikipedia.org/w/api.php'
parameters = {'format' : 'json',
              'action' : 'query',
              #'prop' : 'revisions',
              #'rvprop' : 'content',
              'prop' : 'links|categories',
              'cllimit' : 500,
              'pllimit' : 500,
              'pllimit' : 10,
              'plnamespace' : 0,
              #'prop' : 'extracts',
              #'exsectionformat' : 'raw',
              #'exintro' : '1',
              'redirects' : True}

crawled_articles = []
#categories = set([691117])
categories = set([33240744])

def main(args):
    # TODO: create list of category

    for category in categories:
        getChildCategories(category)

    print len(categories)

    #graph = Graph(crawl(args.start))

    #pickle.dump(graph, open('data/wikipedia.pkl', 'wb'), -1)

def crawl(title):
    #print title
    parameters["titles"] = title
    crawled_articles.append(title)

    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(parameters))))
    page = response[u'query'][u'pages'].values()[0]

    pprint.pprint(response)

    if u'missing' in page:
        return None
    else:
        adjacent_nodes = []

        for link in page[u'links']:
            if link[u'title'] not in crawled_articles:
                node = crawl(link[u'title'])
                if node:
                    adjacent_nodes.append(crawl(link[u'title']))

        return Node({"title": page[u'title'] , "id": page[u'pageid']}, adjacent_nodes)


def getChildCategories(category_id):
    #print category_id
    query_parameters = {'format': 'json',
                        'action': 'query',
                        'list': 'categorymembers',
                        'cmpageid': category_id,
                        'cmtype': 'subcat',
                        'cmlimit': 500}
    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(query_parameters))))

    #pprint.pprint(response)

    for category in response[u'query'][u'categorymembers']:
        if category[u'pageid'] not in categories:
            print category[u'title']
            categories.add(category[u'pageid'])
            getChildCategories(category[u'pageid'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="initial article to start crawling")
    args = parser.parse_args()

    main(args)
