# -*- coding: utf-8 -*-

import io, os, argparse, urllib, urllib2, json, pickle
#import pprint

endpoint = 'http://en.wikipedia.org/w/api.php'

crawled_categories = set()
graph = dict()

def main(args):
    # Make sure the passed category has "Category:" in front of it
    if args.category[:9] == "Category:":
        get_subcat_articles(args.category)
    else:
        get_subcat_articles("Category:" + args.category)


    parameters = {'format' : 'json',
                  'action' : 'parse',
                  'prop' : 'links',
                  'section' : 0,
                  'redirects' : True}

    for title, adjacent in graph.iteritems():
        parameters["page"] = title.encode('utf8')
        response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(parameters))))[u'parse']

        print u'Adding adjacent nodes for article ' + title
        for link in response[u'links']:
            if link[u'ns'] == 0 and u'exists' in link:
                adjacent.add(link[u'*'])
        #pprint.pprint(graph)

    pickle.dump(graph, open('data/wikipedia.pkl', 'wb'), -1)

def get_subcat_articles(category):
    if category in crawled_categories:
        return
    else:
        crawled_categories.add(category)

    query_parameters = {'format': 'json',
                        'action': 'query',
                        'list': 'categorymembers',
                        'cmtitle': category.encode('utf8'),
                        #'cmtype': 'subcat',
                        'cmlimit': 500}
    response = json.load(urllib2.urlopen(urllib2.Request(endpoint, urllib.urlencode(query_parameters))))

    for member in response[u'query'][u'categorymembers']:
        if member[u'ns'] == 0:
            if member[u'title'] not in graph:
                graph[member[u'title']] = set()
        elif member[u'ns'] == 14:
            print u'Fetching articles from ' + member[u'title']
            get_subcat_articles(member[u'title'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("category", help="category to restrict to graph to")
    args = parser.parse_args()

    main(args)
