import pickle
import lxml.html as html
import numpy as np
import pandas as pd
from warnings import warn
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from xml.etree import ElementTree

from time import time
from time import sleep
from bs4 import BeautifulSoup
from requests import get #from requests.exceptions import ParseError


from random import randint
from IPython.display import clear_output
import re



runfile('M:/f_RetrieveLinks.py', wdir='M:')
runfile('M:/f_ParseContent.py', wdir='M:')
runfile('M:/f_MetacriticContent.py', wdir='M:')
runfile('M:/f_download.py', wdir='M:')
runfile('M:/f_dicdic.py', wdir='M:')
runfile('M:/f_tomatoes.py', wdir='M:')


#ratings=[]  #rtng=pd.read_csv("D:\\py\\rtng.csv")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}



Missing             = {}
ttitle              = {}
#CRTC={}
USER = {}
wrong={}

#columns=ia.get_movie(row, info=print(ia.get_movie_infoset())).infoset2keys.get('main')


#tt0299658 tt1019452 54  
start_time = time()
TIME=time()
tts=list(set(pd.read_csv('E:\\#CREATIVITY\\rtng.csv', sep='\t', encoding='utf-8').tconst))#pd.read_csv("M:\\AOM2019.txt", sep="\t").iloc[0:107,0:11]
for tt in tts[4246:4247]:    #tts['Const'].iloc[105:106]: #107 {'tt0114614','tt0096251','tt0088258','tt0072285','tt0067866','tt0090190','tt0067893','tt0058694','tt0096163','tt0086541','tt0080120','tt0063285','tt0094336','tt0032138'}:     #'tt0062622','tt0094625','tt0094294','tt0092610','tt0249380','tt0101420','tt0038348','tt0118715','tt0083658','tt0074226','tt0088846','tt0026138','tt0078908','tt0010323','tt0034583','tt0069897','tt0067690','tt0077402','tt0069952','tt0092890','tt0060315','tt0246578','tt0069019','tt0099487','tt0075984','tt0071464','tt0074486','tt0083907','tt0137523','tt0054880','tt0082414','tt0022913','tt0210070','tt0080801','tt0047034','tt0070155','tt0067185','tt0013257','tt0093177','tt0071615','tt0074287','tt0036027','tt0296042','tt0780536','tt0049366','tt0038650','tt0097202','tt0095483','tt0120737','tt0082694','tt0103905','tt0060666','tt0058333','tt0071853','tt0093605','tt0093608','tt0078087','tt0052077','tt0089885','tt0028346','tt0087995','tt0178868','tt0075152','tt0368226','tt0073650','tt0066104','tt0114436','tt0073735','tt0059742','tt0076759','tt0097648','tt0076786'  #'tt0073629', 'tt0063350', 'tt0070034', 'tt0078935', 'tt0069089', 'tt0072271', 'tt0065466'
    print(tt)

    user_reviews        = {}    
    imdb_reviews        = {}
    metacritic_reviews  = {}
    tomato_reviews      = {}
    user_source        = {}    
    imdb_source        = {}
    metacritic_source  = {}
    tomato_source      = {}
        
    '''colleting information:
    1a-make a request
    1b-parse html
    2-extract the user reviews
        a-extract each review table
        b-convert result to bs4 object
        c-extract [review text, rating (except missing=NA)]
    4-extract the key for next page
    5-if the keys exist, substitute the existing key, sleep, and go back to first step
      if not, exit loop
    '''

    path = 'https://www.imdb.com/title/'
    key  = '/reviews?ref_=tt_urv' #icl  = '/externalreviews?ref_=tt_ov_rt'

    e=0
    while key:
        sleep(randint(3,7))
        e+=1
        #1a-Make a get request
        
        try:
            response = get(path + tt + key, headers=headers) #get('https://www.imdb.com/title/' + tt + '/reviews?ref_=tt_urv', headers=headers) #get('https://www.imdb.com/search/title?title_type=feature&release_date=1970-01-01,2010-12-31&countries=us&runtime=60,&count=250&sort=num_votes,desc&page=' + page)
            if int(re.findall(r'\d+',str(response))[0]) ==200:
                while e<2:
                    #print('stuck')
                    imdb=[tt, response.text]
                    e+=1
                
                #1b- Parse html
                html_soup = BeautifulSoup(response.text, "html.parser")
                
                #2-extract the reviews
                #a-extract each review table
                
                for i in html_soup.find_all('div', class_="lister-item-content"):            
                    #print(1)                
                    #b-convert result to bs4 object
                    k=BeautifulSoup(str(i), "html.parser")
                    #c-extract [review text, rating (except missing=NA)]
    
                    try:
                        #print(2)
                        user_reviews.update({k.find('span', {'class':'display-name-link'}).a['href'].split('/')[2]:[
                                        {'subject'    : k.find_all('a', class_="title")[0].text[1:-1]},
                                        {'content'  : k.find_all('div', class_="text show-more__control")[0].text},
                                        {'helpful'  : k.find_all('div', class_="actions text-muted")[0].text[21:-153]},
                                        {'rating'   : k.find_all('span', class_="rating-other-user-rating")[0].text[6:8]},
                                        {'date'     : k.find('span', {'class':'review-date'}).text},
                                        {'ur'       : k.find('span', {'class':'display-name-link'}).a['href'].split('/')[2]}
                                        #str(k.find_all('span', class_="display-name-link")[0])[41:-25],
                                        #re.search(r'(\d+)', str(k.find_all('span', class_="display-name-link")[0])[41:-25])[0]
                                        ]})
    
                    except:
                        
                        #print(3)
                        
                        user_reviews.update({k.find('span', {'class':'display-name-link'}).a['href'].split('/')[2]:[
                                        {'subject'    : k.find_all('a', class_="title")[0].text[1:-1]},
                                        {'content'  : k.find_all('div', class_="text show-more__control")[0].text},
                                        {'helpful'  : k.find_all('div', class_="actions text-muted")[0].text[21:-153]},
                                        {'rating'   : None},
                                        {'date'     : k.find('span', {'class':'review-date'}).text},
                                        {'ur'       : k.find('span', {'class':'display-name-link'}).a['href'].split('/')[2]}
                                        #str(k.find_all('span', class_="display-name-link")[0])[41:-25],                                
                                        ]})
        
                
                    
                #3-extract the key for next page
                #4-if the keys exist, substitute the existing key, sleep, and go back to first step if not, exit loop      if not, exit loop
                url=html_soup.find_all('div', class_="load-more-data")
                #print(6)
                try:
                    #print(4)
                    key  = '/reviews/_ajax?paginationKey='+str(url[0]['data-key']) #path =url[0]['data-ajaxurl']
                    #print(key)
                except:
                    #print(5)
                    key  = False   
                #key = False
            else:
                wrong.update({tt:'ConnectionError'})
                print(wrong.keys())
                sleep(randint(60,300))
                key  = False 
                
        except ConnectionError as e: 
            wrong.update({tt:'ConnectionError'})
            print(wrong.keys())
            sleep(randint(60,300))            
            key  = False     
        except: 
            wrong.update({tt:'UnknownError'})
            print(wrong.keys())
            sleep(randint(60,300))
            key  = False         
    else:
        print('nononononono!')   

        
    html_soup = BeautifulSoup(imdb[1], "html.parser")    
    title= html_soup.find('h3',{'itemprop':'name'}).a.text
    year = html_soup.find('span',{'class':'nobr'}).text
    
    try:
        year = re.search('\d+',year)[0]
    except:
        year = None

    ttitle.update({tt:title})    
    USER.update({tt:dicdic(user_reviews)})

    

    elapsed= time()-start_time
    print('USER> elapsed: ',round((time()-TIME)/3600), len(USER), 'request-time: ', round(elapsed/60))    
    start_time = time()
    sleep(randint(5,15))       

df=pd.concat(USER)
df.reset_index(inplace=True)
df.columns=df.columns.str.replace('level_0', 'tt')
df.ur=df.ur.str.replace('ur', '').astype(int)*3
len(set(USER.keys())-set([str(s) for s in df.tt]))
df.columns

df[['tt', 'ur', 'date', 'helpful', 'rating']].to_csv('M:\\IMDBreviews3.csv', sep='\t', encoding='utf-8')
df.to_csv('E:\\#CULT\\IMDBreviews3.csv', sep='\t', encoding='utf-8')
with open("E:\\#CULT\\IMDBreviews3.txt", "wb") as fp:   #Pickling
    pickle.dump(df, fp)

        
    '''                         External review pages:
        1-append [4:text from IMDB external page]
        2-save all tokens
    '''

    imdb_external =     get(path + tt + '/externalreviews?ref_=tt_ov_rt', "html.parser") #ctrv.append(get('https://www.imdb.com/title/tt0069089/externalreviews?ref_=tt_ov_rt', "html.parser").text)        

    author =            [a.text for a in BeautifulSoup(imdb_external.text, "html.parser").find_all('a', onclick="window.imdb.trackOffsiteLink(this)")]
    lang   =            [re.search('\(([^)]+)(?!.*\()', s) for s in author]
    for i in range(len(lang)):
        try:            
            lang[i]   = lang[i].group(1)
        except:
            lang[i]   = 'English'


    tokens =            BeautifulSoup(imdb_external.text, "html.parser").find_all('ul', class_="simpleList")[0].find_all('a')    
    imdb_links          =   redir(tokens)


    imdb_links['content']=[]    
    imdb_links['author']=   author
    imdb_links['lang']  =   lang

    


    for i in range(len(imdb_links['link_number'])):
        
        #print('__________________',i)

        if imdb_links['status'][i] in ['Timeout','ConnectionError']:
                imdb_links['content'].append(None)            
        
        elif imdb_links['status'][i].status_code==200:
            if 'see:' in str(imdb_links['URL'][i]):
                imdb_links['content'].append(parse(BeautifulSoup(imdb_links['status'][i].text, 'html.parser').find_all('p')))
            else:
                try:
                    imdb_links['status'][i]=get(imdb_links['URL'][i], headers=headers, timeout=5)                    
                    imdb_links['content'].append(parse(BeautifulSoup(imdb_links['status'][i].text, "html.parser").find_all('p')))

                except Timeout:
                    imdb_links['content'].append(None)
                    imdb_links['status'][i]='TIMEOUT: '+str(imdb_links['URL'][i])

                except:
                    imdb_links['content'].append(None)
                    imdb_links['status'][i]=imdb_links['URL'][i]
                    
                    
        else:
                imdb_links['content'].append(None)
            


    imdb_reviews.update({title:diclis(imdb_links)})
    #Missing.update({title:pd.DataFrame([[title,tt,y.keys(),list(y.values())[0]] for y in imdb_links['content'] if list(y.values())[0]==None or len(list(y.values())[0])<100])})
    

    elapsed= time()-start_time
    print('EXTERNAL     : ',round(elapsed/60))    
    start_time = time()




    '''                     RESET URL path defaults'''                
    
    
    '''                         METACRITIC:
        1-URL: extract METACRITIC url
        2-SAVE? save [tt, metacritic_url, imdb~metacritic, ]
        3-LINKS: append [3:metacritic review links]  
    '''
    
            #1- url|class_="see-more:tt"
    '''
    imdb_metacritic = get('https://www.imdb.com/title/' + tt + '/criticreviews?ref_=tt_ov_rt', headers=headers) #get('https://www.imdb.com/title/' + tt + '/reviews?ref_=tt_urv', headers=headers) #get('https://www.imdb.com/search/title?title_type=feature&release_date=1970-01-01,2010-12-31&countries=us&runtime=60,&count=250&sort=num_votes,desc&page=' + page) 
    html_soup       = BeautifulSoup(imdb_metacritic.text, "html.parser")
    title           = html_soup.find('h3', itemprop="name").text[1:-40]
    metacritic_url  = 'https://www.metacritic.com/movie'+html_soup.find_all('div', class_="see-more")[0].a['href'].split('?')[0]+'/critic-reviews'
    '''

    positive_url  = 'https://www.metacritic.com/movie/'+ title.lower().replace(" ","-") + '/critic-reviews?dist=positive'    
    positive_links  =   MTCRTC(positive_url,'positive',title,year)

    
    sleep(randint(1,3)) 
    
    negative_url  = 'https://www.metacritic.com/movie/'+ title.lower().replace(" ","-") + '/critic-reviews?dist=negative'    
    negative_links  =   MTCRTC(negative_url,'negative',title,year)


    sleep(randint(1,3)) 
    
    neutral_url  = 'https://www.metacritic.com/movie/'+ title.lower().replace(" ","-") + '/critic-reviews?dist=neutral'    
    neutral_links  =   MTCRTC(neutral_url,'neutral',title,year)

    
    metacritic_reviews.update({title:
        {'positive':diclis(download([x[2] for x in positive_links[0] if x[2] is not None])),
         'negative':diclis(download([x[2] for x in negative_links[0] if x[2] is not None])),
         'neutral':diclis(download([x[2] for x in neutral_links[0] if x[2] is not None]))        }})

    metacritic_source.update({title:
        {'positive':{'source' : positive_links[1], 'excerps' :  positive_links[2]},
         'negative':{'source' : negative_links[1], 'excerps' :  negative_links[2]},
         'neutral':{'source' : neutral_links[1], 'excerps' :  neutral_links[2]}        }})
    
    elapsed= time()-start_time
    print('METACRITIC   : ',round(elapsed))
    start_time = time()    
    
    
    '''                         ROTTENTOMATOES :
        1-URL: extract METACRITIC url
        2-SAVE? save [tt, metacritic_url, imdb~metacritic, ]
        3-LINKS: append [3:metacritic review links]  
    '''
    
    fresh_ratings   = tomatoes('fresh', title, year)
    rotten_ratings  = tomatoes('rotten', title, year)


    tomato_reviews.update({title:
        {'fresh':diclis(download([x for x in list(fresh_ratings.keys()) if x is not None])),
         'rotten':diclis(download([x for x in list(rotten_ratings.keys()) if x is not None]))        }})
    
    tomato_source.update({title:
    {'fresh':fresh_ratings.values(),
     'rotten':fresh_ratings.values()    }})
    


    elapsed= time()-start_time
    print('TOMATO       : ',round(elapsed)) 
    
    
    
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:22:55 2019
@author: Joobing



'Harold and Maude', 'The Masque of the Red Death', 'The Sound of Music', 'Brazil', 'Eraserhead', 'Baise-moi', 'Mad Max 2', 'The Wizard of Oz', 'Ringu', 'Emmanuelle'
[tomato_reveiws[x]['rotten']['data'][['link_number', 'site', 'status', 'URL', 'link','content']] for x in [ 'Harold and Maude','The Masque of the Red Death', 'The Sound of Music', 'Brazil', 'Eraserhead', 'Baise-moi', 'Mad Max 2', 'The Wizard of Oz', 'Ringu', 'Emmanuelle']]

pd.concat(tomato_reveiws[x][y]['data'] for x,y in zip(( 'Harold and Maude','The Masque of the Red Death', 'The Sound of Music', 'Brazil', 'Eraserhead', 'Baise-moi', 'Mad Max 2', 'The Wizard of Oz', 'Ringu', 'Emmanuelle'), ['fresh','rotten']), keys=y)


"""
'''
################to_json###########################
USER['Witchfinder General']=USER['De heksenjager']
USER['Enter the Dragon']=USER['In de klauwen van de draak']
del USER['In de klauwen van de draak']
del USER['De heksenjager']

i=0
for key in USER.keys():
    if key in tts['Title'].unique():
        i+=1
        print(i,"-",key)
        USER[key].to_json(tts[tts.Title==key].Const.values[0]+'.json', orient='records')
    else:
        print("!",key, tts[tts.Title==key].Const)
        
    #del USER[key]['tconst']
    #USER[key].tconst=tts.loc[tts.Title==key].Const

##############read_json########################

import glob
i=1
df=pd.read_json(tts.Const[0]+'.json', orient='records').assign(tconst=tt)
for tt in tts.Const[1:107]:
    if tt+".json" in [f.replace('M:\\','') for f in glob.glob("M:\*.json")]:
        i+=1
        print(i,"-",tt)
        df=df.append(pd.read_json(tt+'.json', orient='records').assign(tconst=tt))
    else:
        print("!",tt,"-", tts[tts.Const==tt].Title)

MSSD=tts.loc[tts.Title.isin([t for t in tts.Title[0:107] if t not in ' '.join(USER.keys())])].Const



#####################lie detector###################

difference_locations = np.where(df1 != df2)

changed_from = df1.values[difference_locations]

changed_to = df2.values[difference_locations]

pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index).drop_duplicates(keep='last')
'''
