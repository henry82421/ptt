#coding=utf-8
import pyes
import json
import codecs
import sys


conn = pyes.es.ES('http://220.133.19.103:9200')


file_tianya= codecs.open('D://ptt1.json', 'w', 'utf8')

bq = pyes.query.BoolQuery() 
bq.add_must(pyes.query.TermQuery("Author","webster1112")) 



total=0
pos=0.0
neg=0.0
test=0



result = conn.search(query=bq , indices='ptt' , doc_types='reply',fields='PageLink,Tag,Author,TopicId,Content')



for data in result:
   total+=1
   bbq = pyes.query.BoolQuery() 
   bbq.add_must(pyes.query.QueryStringQuery("'"+'"'+data['PageLink'][0]+'"'+"'"))
   result1 = conn.search(query=bbq , indices='ptt' , doc_types='topic',fields='push_count,hate_count,PageLink') 
   for data1 in result1:     
       if data['PageLink'][0] == data1['PageLink'][0] : 
            if int(data1['push_count'][0])>int(data1['hate_count'][0]) and data['Tag'][0] ==u'推 ':
                test+=1
                pos+=1              
                break
            elif int(data1['push_count'][0])<int(data1['hate_count'][0]) and data['Tag'][0] ==u'推 ':             
                file_tianya.write(json.dumps(data['TopicId'][0]) + ",\n")
                print  data['Content'][0]          
                test+=1
                neg+=1
                break
            elif int(data1['push_count'][0])<int(data1['hate_count'][0]) and data['Tag'][0] ==u'噓 ':              
                test+=1
                pos+=1
                break
            elif int(data1['push_count'][0])>int(data1['hate_count'][0]) and data['Tag'][0] ==u'噓 ':
                file_tianya.write(json.dumps(data['TopicId'][0]) + ",\n")
                print  data['Content'][0]                   
                test+=1
                neg+=1
                break            
            else:
                test+=1
                break
         
file_tianya.flush()     
print total
print pos    
print neg    
print neg/(pos+neg)
print test

