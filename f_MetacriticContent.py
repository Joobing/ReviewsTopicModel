# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 20:49:51 2019
f_MetacriticContent
@author: u811717
"""
def MTCRTC(positive_url,sentiment,title,year):
        try:
            positive  = get(positive_url, headers=headers)
            if int(positive.status_code)==200:
                #print('code200')
                html_soup = BeautifulSoup(positive.text, "html.parser")
                try:
                    release = int(next(re.finditer(r'\d+$', html_soup.find("span", {'class':'release_date'}).text)).group(0))
                    #print(release)
                    if int(year) == release: 
                        #print('parsing')
                        positive_links   = geturl(BeautifulSoup(positive.text, "html.parser").find_all('a', class_="read_full"))                    
                        positive_summary = [x.text for x in html_soup.find_all('div', class_="summary")]
                        positive_author  = [x.text for x in html_soup.find_all('span', class_="author")]
                        positive_source  = [html.fromstring(str(x.a)).xpath('//@title')[0]  if html.fromstring(str(x.a)).xpath('//@title') else x.a.text for x in html_soup.find_all('span', class_="source")  ]
                        
                    else:
                        #print('rename')
                        positive_url  = 'https://www.metacritic.com/movie/'+ title.lower().replace(" ","-") +'-'+str(year)+ '/critic-reviews?dist='+str(sentiment)
                        try:
                            sleep(randint(2,7))
                            positive  = get(positive_url, headers=headers)
                            if int(positive.status_code)==200:
                                
                                html_soup = BeautifulSoup(positive.text, "html.parser")
                                positive_links =  geturl(html_soup.find_all('a', class_="read_full"))
                                positive_summary = [x.text for x in html_soup.find_all('div', class_="summary")]
                                positive_author  = [x.text for x in html_soup.find_all('span', class_="author")]
                                positive_source  = [html.fromstring(str(x.a)).xpath('//@title')[0]  if html.fromstring(str(x.a)).xpath('//@title') else x.a.text for x in html_soup.find_all('span', class_="source")  ]

                            else:
                                #print('year mismatch')
                                positive_links =  [None]
                                positive_summary = [None]
                                positive_source = [None]
                                positive_author = ['year mismatch']       
                    
                        except ConnectionError as e:             
                            positive_links =  [None]
                            positive = 'ConnectionError' 
                            positive_summary = [None]
                            positive_source = [None]
                            positive_author = [None]       
                                                        
                except ConnectionError as e: 
                    #print('connect')
                    positive_links =  [None]
                    positive = 'ConnectionError'
                    positive_summary = [None]
                    positive_source = [None]
                    positive_author = [None]       
                                            
                except:
                    #print('no release')                    
                    positive_links =   [None]
                    positive_summary = [None]
                    positive_source = [None]
                    positive_author = [None]       
                    
            else:
                #print('404')
                positive_links =   [None]
                positive_summary = [None]
                positive_source = [None]
                positive_author = [None]       
                
        except ConnectionError as e:
            #print('connect')
            
            positive_links =  [None]
            positive = 'ConnectionError' 
            positive_summary = [None]
            positive_source = [None]
            positive_author = [None]
            
                       
        except:
            #print('no release')
            positive_links =   [None]
            positive_summary = [None]
            
        return [[x,y,z] for x,y,z in zip(positive_source,positive_author,positive_links)], positive, {x:[y,z] for x,y,z in zip(positive_source,positive_author,positive_summary)}

            