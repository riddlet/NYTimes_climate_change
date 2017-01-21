import json
import urllib2
import sys
from math import ceil
import time

def get_articles(api_key, query, begin_date, end_date, page='0'):
    """
    Get one page of article data. 
    Feed in your api key, your query term, the dates to filter by, and the page number.

    query is formatted as 'foo+bar'

    dates are formatted YYYYMMDD
    
    returns json formatted data.
    """
    
    baseurl = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    req = baseurl + '?q=' + query + '&page=' + page + '&begin_date=' + begin_date + '&end_date=' + end_date + '&api-key=' + api_key
    resp = request_until_succeed(req)
    dat = json.loads(resp)
    
    return(dat)

def get_comment_count(api_key, url):
    """
    Get comment counts from NYTimes api
    """
    
    baseurl = 'http://api.nytimes.com/svc/community/v3/user-content/url.json'
    req = baseurl + '?api-key=' + api_key + '&url=' + url    
    resp = request_until_succeed(req)
    dat = json.loads(resp)
    time.sleep(0.1)
    
    return(dat['results']['totalCommentsFound'])

def build_data(api_key, query, begin_date, end_date, page='0'):
    """
    pages through the results, building up the json results of the query.
    Pauses adjust for rate limits
    """
    
    dat = get_articles(api_key, query, begin_date, end_date, page='0')
    time.sleep(1)
    articles_data = dat['response']['docs']
    pages = ceil(dat['response']['meta']['hits']/10)
    for page in range(1, int(pages)):
        print('Gathering article page {} of {}'.format(page, pages))
        p = get_articles(api_key, query, begin_date, end_date, page=str(page))
        articles_data.extend(p['response']['docs'])
        time.sleep(0.75)
        
    return(articles_data)

def request_until_succeed(url):
    """
    handles potential errors when sending a request
    """
    
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

    return response.read()

def main(argv):
    api_key = argv
    query = 'climate+change'
    begin_date = '20161101'
    end_date = '20161201'
    dat = build_data(api_key, query, begin_date, end_date, page='0')
    for i,j in enumerate(dat):
        print('getting comments - article {} of {}'.format(i, len(dat)))
        j[u'comments']=get_comment_count(api_key, j['web_url'])

    with open('output/article_search.json', 'w') as outfile:
        json.dump(dat, outfile)

if __name__=='__main__':
    main(sys.argv[1])

