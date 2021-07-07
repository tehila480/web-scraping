from os import truncate
from types import ClassMethodDescriptorType
from typing import ClassVar, Literal, TypedDict
from bs4 import BeautifulSoup
from urllib.request import *
import json
import requests
import re
import string
import io
import unicodedata as ucd
def detailsOfMovie(item, index,f,s) :
    url="https://www.imdb.com/"+item+"?ref_=fn_tt_tt_"+str(index)
    #url="https://www.imdb.com/title/tt1578957/?ref_=fn_tt_tt_3"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.findAll('script', attrs={'type': "application/ld+json"})
    info_data = spans[0]
    #print(info_data)
    info_data_dict = json.loads(info_data.string)
    title=info_data_dict.get('name')
    flag='true'
    str1=s.split('+')
    for x in str1:
        if(title.lower().find(x.lower())==-1):
            flag='false'
    if(flag=='true'):
        f.write(info_data_dict.get('name'))
        f.write('|')
        genres = info_data_dict.get('genre')
        #print(type(genres))
        if(type(genres)==list):
            g=""
            for x in genres:
                 g=g+x+', '
            g=g[:len(g)-2]
            f.write(g)    
        elif(type(genres)==str):
            f.write(genres)
        f.write('|')    
        rating=info_data_dict.get('contentRating')
        if(rating!=None):
            f.write(rating)
        f.write('|') 
        directors=info_data_dict.get('director')
        if(type(directors)==list):
            namesD=""
            for x in directors:
                namesD=namesD+x["name"]+", "
            namesD=namesD[:len(namesD)-2]
            i=namesD.rfind(",") 
            namesD=namesD[:i]
            if(namesD.isascii()):
                f.write(namesD)
            else:
                f.write(str(namesD.encode('utf-8')))
        elif(type(directors)==dict):
            if(directors['name'].isascii()):
                f.write((directors['name']))
            else:
                f.write(str(directors['name'].encode('utf-8')))
        f.write('|')
        actors=info_data_dict.get('actor')
        if(type(actors)==list):
            namesA=""
            for x in actors:
                namesA=namesA+x["name"]+", "
            namesA=namesA[:len(namesA)-2]
            i=namesA.rfind(",") 
            namesA=namesA[:i]
            if(namesA.isascii()):
                f.write(namesA)
            else:
                
                f.write(str(namesA.encode('utf-8')))
        elif(type(actors)==dict):
            if(actors['name'].isascii()):
                f.write((actors['name']))
            else:
                f.write(str(actors['name'].encode('utf-8')))
    
    

        f.write('\n')
    
   
    






def main():
    f=open("listOfMovies.txt","w") 
    

    term_search=input("enter a term serch:\n")
    term_search=term_search.replace(' ','+')
    url = "https://www.imdb.com/find?s=tt&q="+term_search+"&ref_=nv_sr_sm"

    
    #url ="https://www.imdb.com/find?s=tt&q=the+russia+house&ref_=nv_sr_sm"
    #print(url)
    page = urlopen(url)
    #print(page)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.find_all('a',{'class':'/title/tt0310455/?ref_=fn_al_tt_3a'}))
    #print(soup)
    result = soup.find_all('td', {'class': 'result_text'})

   
    i=0
    for item in result:
        i=i+1
        #print(type(item.find("a")))
        detailsOfMovie(item.find("a")["href"],i,f,term_search)
        #f.write(name+"|")
       # genre=genreOfMovie()
        
    f.close()
if __name__ == '__main__':
    main()

