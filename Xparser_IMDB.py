# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:09:15 2022

@author: Joobing
"""

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

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def redir(tokens):  #[<a>]:[href].text #<link,rel=canonical,[0]>
    '''redir: takes in html tags (tokens) containing dynamic links to target (external) addresses, returns permanent link (and occasionaly, content of the linked webpage?)'''

    i=-1
    #j=-1

    site=[]#permanent url for the target site
    status=[]#whether target address retreived anything
    link_number=[]#nth target site from all the target addresses
    URL=[]#all canonical links within the target address, including it's (own) target address (usually that's all you get)
    
    unknown_redir_page=[]
    start_time =time()
    requests = 0
    for l in tokens:
        i=i+1
        try:
            site.append(l['href']) #(re.search('offsite-(.*)&', l['href']).group(1))
        except:
            pass#site.append(re.search('page-action=(.*)&', l['href']).group(1))
        
        link_number.append(i)
 
       
        try:
            page=get(l['href'], headers=headers, timeout=20)          
            status.append(page)
            #print([i,page.status_code])
            
            if int(page.status_code)==200:
                try: 
                    URL.append(BeautifulSoup(page.text, "html.parser").find_all('link', attrs={"rel":"canonical"})[0]['href'])
                except: 
                    URL.append("see: ['status'].text      status code : "+str(page.status_code)) #URL.append("see: ['unknown_redir_page']"+'['+str(j)+'],number:'+str(j))
            else:
                URL.append("see: ['status'].text "+str(page.status_code))   
                
            sleep(np.random.randint(3,6))     
        
             
        
        except Timeout:
            status.append('Timeout')
            URL.append('Timeout')            
            
            
        except ConnectionError as e:             
            status.append('ConnectionError')
            URL.append('NoResponse')
        
        except:
            status.append(page)            
            URL.append("see: ['status'].text "+str(page.status_code))   


    return {'link_number':link_number,'site':site,'status':status,'URL':URL} #,'unknown_redir_page':[unknown_redir_page]


def diclis(d):
    return pd.DataFrame.from_dict(d,orient='index').transpose()
def parse(allPs):
    '''extracts main body of an article from all (html) paragraphs of a given address (e.g. all the ads and warnings etc)
    also separates first and last paragraphs for cross checking'''
    first=''
    last_paragraph=''
    extra_paragraph=''
    extra_paragraph_2=''
    content=""
    parsed=0
    for i in range(len(allPs)):
        
        if len(allPs[i].text.replace(" ", "")) > 250:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()
            parsed=1

        elif i+2 in range(len(allPs)) and len(allPs[i+1].text.replace(" ", "")) > 450:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()               
            parsed=1
            
        elif i+2 in range(len(allPs)) and len(allPs[i+2].text.replace(" ", "")) > 450: 
            first=first+'\n'+allPs[i].text.strip()               
            parsed=1

        else:
            if parsed == 1:
                last_paragraph= last_paragraph + allPs[i].text.strip()
                if i+2 in range(len(allPs)): 
                    extra_paragraph= extra_paragraph + allPs[i+1].text.strip()
                    extra_paragraph_2= extra_paragraph_2 + allPs[i+2].text.strip()                                   
                elif i+1 in range(len(allPs)): 
                    extra_paragraph= extra_paragraph + allPs[i+1].text.strip()                    
                else:
                    extra_paragraph= None
                #print('\nlast\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
                #print('\nlatest\n'+allPs[i+1].text.strip(),'\n',str(i+1),':',str(len(allPs[i+1].text.replace(" ", ""))))            
                break
            else: pass
    return [first, content, last_paragraph, extra_paragraph, extra_paragraph_2]





#ratings=[]  #rtng=pd.read_csv("D:\\py\\rtng.csv")



Missing             = {}
ttitle              = {}
#CRTC={}
USER = {}
wrong={}

#columns=ia.get_movie(row, info=print(ia.get_movie_infoset())).infoset2keys.get('main')


#tt0299658 tt1019452 54  
start_time = time()
TIME=time()
tts=['tt0114614','tt0096251','tt0088258']#list(set(pd.read_csv('E:\\#CREATIVITY\\rtng.csv', sep='\t', encoding='utf-8').tconst))#pd.read_csv("M:\\AOM2019.txt", sep="\t").iloc[0:107,0:11]
for tt in tts:    #tts['Const'].iloc[105:106]: #107 {'tt0114614','tt0096251','tt0088258','tt0072285','tt0067866','tt0090190','tt0067893','tt0058694','tt0096163','tt0086541','tt0080120','tt0063285','tt0094336','tt0032138'}:     #'tt0062622','tt0094625','tt0094294','tt0092610','tt0249380','tt0101420','tt0038348','tt0118715','tt0083658','tt0074226','tt0088846','tt0026138','tt0078908','tt0010323','tt0034583','tt0069897','tt0067690','tt0077402','tt0069952','tt0092890','tt0060315','tt0246578','tt0069019','tt0099487','tt0075984','tt0071464','tt0074486','tt0083907','tt0137523','tt0054880','tt0082414','tt0022913','tt0210070','tt0080801','tt0047034','tt0070155','tt0067185','tt0013257','tt0093177','tt0071615','tt0074287','tt0036027','tt0296042','tt0780536','tt0049366','tt0038650','tt0097202','tt0095483','tt0120737','tt0082694','tt0103905','tt0060666','tt0058333','tt0071853','tt0093605','tt0093608','tt0078087','tt0052077','tt0089885','tt0028346','tt0087995','tt0178868','tt0075152','tt0368226','tt0073650','tt0066104','tt0114436','tt0073735','tt0059742','tt0076759','tt0097648','tt0076786'  #'tt0073629', 'tt0063350', 'tt0070034', 'tt0078935', 'tt0069089', 'tt0072271', 'tt0065466'
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
    #key  = '/reviews?ref_=tt_urv' #icl  = '/externalreviews?ref_=tt_ov_rt'


        
    '''                         External review pages:
        1-append [4:text from IMDB external page]
        2-save all tokens
    '''

    imdb_external =     get(path + tt + '/externalreviews?ref_=tt_ov_rt', "html.parser") #ctrv.append(get('https://www.imdb.com/title/tt0069089/externalreviews?ref_=tt_ov_rt', "html.parser").text)        
    html_soup =         BeautifulSoup(imdb_external.text, "html.parser")
    author =            [a.text for a in html_soup.find_all('a', onclick="window.imdb.trackOffsiteLink(this)")]
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
            

    title= html_soup.find('h3',{'itemprop':'name'}).a.text
    def dicdat(d):
        return pd.DataFrame.from_dict(d,orient='index').transpose()
    imdb_reviews.update({title:dicdat(imdb_links)})
    #Missing.update({title:pd.DataFrame([[title,tt,y.keys(),list(y.values())[0]] for y in imdb_links['content'] if list(y.values())[0]==None or len(list(y.values())[0])<100])})
    

    elapsed= time()-start_time
    print('EXTERNAL     : ',round(elapsed/60))    
    start_time = time()