# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 21:35:16 2019
f_tomatoes
@author: u811717
"""
def tomatoes(gooneh, onvan, saal):
    
    onvan=re.sub(r'(^the\ )', r'', onvan)
    vaziyat = 0

    goje_ratings = {} 
    while vaziyat <2:
        #print('while')

        goje_url =      "https://www.rottentomatoes.com/m/" + onvan.lower().replace(" ","_") + "/reviews?sort="+gooneh
    
        goje  =          get(goje_url, headers=headers)
    
        try: 
            release = int(re.search('(\\d{4})', BeautifulSoup(goje.text, "html.parser").find('span', text='In Theaters:').parent.text).group(1))
            #print(release)
            if int(saal)== release:
                #print('parsing')
            
                try: 
                    goje_pgnum = int(BeautifulSoup(goje.text, "html.parser").find('span', {'class':"pageInfo"}).text[-2:])
                except:
                    goje_pgnum = None
                
            
            
            
                pp     = '&page='
            
                path   = goje_url
                num    = goje_pgnum
                
            
                
                   
                soup=  BeautifulSoup(goje.text, "html.parser") 
                for s,a,p,r,d, in zip(soup.find_all('div', class_="small subtle review-link"),
                                              soup.find_all('a', class_='unstyled bold articleLink'),
                                              soup.find_all('em', class_='subtle critic-publication'),
                                              soup.find_all('div', class_='the_review'),
                                              soup.find_all('div', class_='review-date subtle small')):
                                                            
                    if s.a is not None:
                        #print(s.a['href'])                
                        try: goje_ratings.update({s.a['href'] : [p.text, a.text, r.text, re.search('\:(.*)', s.text).group(1), d.text ]})
                        except: goje_ratings.update({s.a['href'] : [p.text, a.text, r.text, d.text ]})
                    else: 
                        try:
                            goje_ratings.update({'missing:'+p.text : [a.text, r.text, re.search('\:(.*)', s.text).group(1), d.text ]})
                        except:
                            goje_ratings.update({'missing:'+p.text : [a.text, r.text, d.text ]})
                        else:   pass
            
                            
            
            
            
                if  num is not None:
                    for i in range(1,num+1):
                        #print(i)
            
            
                        sleep(randint(2,5))
            
            
                        soup=BeautifulSoup(get(path+pp+str(i), headers=headers).text, "html.parser")
                        for s,a,p,r,d, in zip(soup.find_all('div', class_="small subtle review-link"),
                                              soup.find_all('a', class_='unstyled bold articleLink'),
                                              soup.find_all('em', class_='subtle critic-publication'),
                                              soup.find_all('div', class_='the_review'),
                                              soup.find_all('div', class_='review-date subtle small')):
                            
                            
                            
                            if s.a is not None:
                                #print(s.a['href'])                
                                try: goje_ratings.update({s.a['href'] : [p.text, a.text, r.text, re.search('\:(.*)', s.text).group(1), d.text ]})
                                except: goje_ratings.update({s.a['href'] : [p.text, a.text, r.text, d.text ]})
                            else: 
                                try:
                                    goje_ratings.update({'missing:'+p.text : [a.text, r.text, re.search('\:(.*)', s.text).group(1), d.text ]})
                                except:
                                    goje_ratings.update({'missing:'+p.text : [a.text, r.text, d.text ]})
                                else:   pass
                vaziyat += 2
    
            else:
                #print('rename')
                onvan=onvan+'_'+str(saal)
                vaziyat += 1                
        except:
            #print('no release')
            goje_ratings.update({'missing: ' + onvan  : [goje]})
            vaziyat+=2
            
                
    return goje_ratings