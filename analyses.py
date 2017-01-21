import json
import pandas as pd
import numpy as np
import re
import glob

def core_url(url):
    """
    quick function to extract just the base part of the url. 
    """
    m = re.search('(http(s)?://(((www|.+\.blogs)\.nytimes\.com.+)(roomfordebate/.+|/$|.html)))', url)
    if m:
        return(m.group(3))
    else:
        return('********url %s not pulled' % url)

def get_keywords(dat):
    """
    pull out data from json object (dat) for keywords analysis
    """
    out = []
    for art in dat:
    	if art.get('keywords'):
	        for child in art.get('keywords'):
	            out.append([art['_id'], art['section_name'], child['value'], child['name'],])
        else:
	    	out.append([art['_id'], art['section_name'], np.nan, np.nan])
    
    df = pd.DataFrame(out, columns = ['id', 'section', 'keyword', 'entity_type'])
    return(df)

def count_keywords(df):
    """
    count keywords by entity type
    """
    df['keyword_count'] = df.groupby(['entity_type', 'keyword'])['id'].transform('count')
    df['section_count'] = df.groupby(['section'])['id'].transform('nunique')
    return(df)

def compute_influence(nyt_dat, fb_dat):
    """
    computes one standardized measure of influence given the new york times json data and the facebook data.
    returns a single data frame
    """
    out = []
    for art in nyt_dat:
        out.append([art['pub_date'], art['comments'], art['web_url'], art['_id'],])
    
    df = pd.DataFrame(out, columns = ['pub_date', 'nyt_comments', 'web_url', 'id'])
    df = df.drop_duplicates(subset='id') #one article is listed twice
    df['clean_url'] = df.web_url.apply(core_url)
    fb_dat['clean_url'] = fb_dat.link.apply(core_url)
    fb_dat = fb_dat.groupby('clean_url')[['reactions', 'shares', 'comments']].sum().reset_index() #one article was shared twice
    df = pd.merge(df, fb_dat.loc[:,['reactions', 'shares', 'comments', 'clean_url']], 
                  how='left', on='clean_url')
    #articles with commenting not allowed return a zero, so we replace all zeros with nan
    df.nyt_comments.replace(0, np.nan, inplace=True)
    df['nyt_comments_std'] = (df.nyt_comments-df.nyt_comments.mean())/df.nyt_comments.std()
    df['reactions_std'] = (df.reactions-df.reactions.mean())/df.reactions.std()
    df['shares_std'] = (df.shares-df.shares.mean())/df.shares.std()
    df['comments_std'] = (df.comments-df.comments.mean())/df.comments.std()
    col_list = ['nyt_comments_std', 'reactions_std', 'shares_std', 'comments_std']
    df['influence'] = df[col_list].mean(axis=1)
    
    return(df)

def main():
    with open('output/article_search.json') as f:
    	dat = json.load(f)
	
	df = get_keywords(dat)
	df = count_keywords(df)
    files = glob.glob('output/fb_dat/*facebook_dat.csv')
    fb_dat = pd.DataFrame()
    for f in files:
        d = pd.read_csv(f)
        fb_dat = pd.concat([fb_dat, d])
        
    df_infl = compute_influence(dat, fb_dat)
    df.to_csv('output/counts.csv', index=False, encoding='utf-8')
    df_infl.to_csv('output/infl.csv', index=False, encoding='utf-8')

if __name__=='__main__':
    main()