import pyes
import json
import FormatTranslator
import FileTools

conn=pyes.es.ES('localhost:9200')
q = pyes.MatchAllQuery()

tagg = pyes.aggs.TermsAgg('name', field= 'name', sub_aggs=[]) 
tagg1 = pyes.aggs.TermsAgg('link', field= 'link')  
tagg.sub_aggs.append(tagg1) 
qsearch = pyes.query.Search(q) 
qsearch.agg.add(tagg)

rs = conn.search(query=qsearch , indices='ooooo' ,type="type" )
print json.dumps(rs.aggs,indent=2)

formatTranslator = FormatTranslator.FormatTranslator()
result = formatTranslator.ES_Aggs_2_Layer_to_Matrix_and_indice(rs.aggs, agg1_name="name", agg2_name="link")

# 使用工具將結果儲存起來
fileTools = FileTools.FileTools()
fileTools.List_to_CSV(result['colIndexList'], "co.csv")
fileTools.List_to_CSV(result['rowIndexList'], "row.csv")
fileTools.Matrix_to_CSV(result['matrix'], "matrixx.csv")



