import urllib2
import json
import datetime
import time
import re
import csv
import sys

def get_page(app_id, app_secret):
    """
    initial query to nyt facebook 
    app_id and app_secret are concatenated for an access token
    see documentation here: https://developers.facebook.com/docs/facebook-login/access-tokens
    """
    
    baseurl = 'https://graph.facebook.com/v2.8/nytimes/feed/'
    access_token = '&access_token=' + app_id + '|' + app_secret
    fields = '?fields=id,name,link,created_time,reactions.summary(true),comments.summary(true),shares&limit=25'
    url = baseurl+fields+access_token
    dat = json.loads(request_until_succeed(url))
    
    return(dat)

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

def page_through(app_id, app_secret):
    """
    pages through the nyt facebook page until there are no more pages, or the posts occur before 11/1
    """
    has_next_page = True
    in_date_range = True
    
    #we only want to keep the articles that were returned from the NYtimes api, so this creates a list of target urls
    with open('output/article_search.json') as f:
        nyt_dat = json.load(f)
    nyt_urls = []
    for i in nyt_dat:
        nyt_urls.append(core_url(i['web_url']))

    items = get_page(app_id, app_secret)
    process_items(items, nyt_urls)

    while has_next_page & in_date_range:
        if 'paging' not in items.keys():
            has_next_page=False

        if items['data'][0]['created_time'][0:7]=='2016-10':
            in_date_range = False

        items = json.loads(request_until_succeed(items['paging']['next']))
        process_items(items, nyt_urls)

def process_items(json_dat, target_urls):
    """
    json_dat is the data returned from the fb graph api query
    target_urls is the list of urls returned from our nytimes api query
    The function checks the link for each facebook post - if the link is in the NYT data, it writes the metadata into a csv file
    """
    print('********Writing file for posts at %s' % json_dat['data'][0]['created_time'])
    with open('output/fb_dat/%s_facebook_dat.csv' % datetime.datetime.now(), 'wb') as outfile:
        w = csv.writer(outfile)
        w.writerow(['id', 'link', 'reactions', 'shares', 'can_comment', 'comments'])
        for item in json_dat['data']:
            try:
                if core_url(item['link']) in target_urls:
                    w.writerow([item['id'],
                               item['link'],
                               item['reactions']['summary']['total_count'],
                               item['shares']['count'],
                               item['comments']['summary']['can_comment'],
                               item['comments']['summary']['total_count']])
            except:
                pass
                        
def core_url(url):
    """
    quick function to extract just the base part of the url. 
    """
    m = re.search('(http(s)?://(((www|.+\.blogs)\.nytimes\.com.+)(roomfordebate/.+|/$|.html)))', url)
    if m:
        return(m.group(3))
    else:
        return('********url %s not pulled' % url)
        
def main(argv1, argv2):
    app_id = argv1
    app_secret = argv2
    dat = page_through(app_id, app_secret)
    
if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])
