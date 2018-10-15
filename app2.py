import numpy as np
import pandas as pd
import operator
import math

querys = []
with open('query_list.txt') as f:
    for line in f:
        querys.append(line.strip())


docs = []
with open('doc_list.txt') as f:
    for line in f:
        docs.append(line.strip())

# print(docs)


# read all docs
doc_series = []
for doc in docs:
    doc_array = []
    with open('Document/'+doc) as f:
        next(f)
        next(f)
        next(f)
        for line in f:
            words = line.split(' ')
            for word in words:
                if word != '-1\n':
                    doc_array.append(word)

    x = pd.value_counts(doc_array)
    doc_series.append(x)




# read all querys
query_series = []

# max_tfq = 0
for query in querys:

    query_array = []
    with open('Query/'+query) as f:
        for line in f:
            words = line.split(' ')
            for word in words:
                if word != '-1\n':
                    query_array.append(word)

    x = pd.value_counts(query_array)
    
    # #clac max tf in query
    # if x[0] > max_tfq:
    #     max_tfq = x[0]
    #     # print('update max_tfq -> %d' % max_tfq)

    query_series.append(x)



history_idf = {}
def idf(word):
    #find history
    if word in history_idf:
        return history_idf[word]

    df = 0
    for s in doc_series:
        if word in s.index:
            df += 1
    if df == 0:
        df = 0.5
    idf = math.log(2265/df)

    #save
    history_idf[word] = idf
    return idf

history_tf = {}
def tf(index, word, series):
    series_no = 2
    if series == doc_series:
        series_no = 1

    #find history
    if '%d%s%d' %(index, word, series_no) in history_tf:
        return history_tf['%d%s%d' %(index, word, series_no)]

    tf = 0
    if word in series[index].index:
        f = series[index].get_value(word)
        tf = 1+math.log2(f)
        #try ineerfnc log

    #query tf tuning
    # if series_no == 2:
    #     tf = ( 0.5 + 0.5*(tf/series[index][0]) )
    #     print('max tf in this query -> %d' % series[index][0])

    #save
    history_tf['%d%s%d' %(index, word, series_no)] = tf
    return tf

history_tfidf = {}
def tf_idf(index, word, series):
    series_no = 1
    if series == query_series:
        series_no = 2

    #find history
    if '%d%s%d' %(index, word, series_no) in history_tf:
        return history_tfidf['%d%s%d' %(index, word, series_no)]
    
    #origin
    tf_idf = tf(index, word, series) * idf(word)
    

    #scheme 2
    # if series_no ==1:
    #     tf_idf = 1+tf(index, word, series)
    # else:
    #     tf_idf = math.log10(1+ 16/idf(word))

    #scheme 3
    # tf_idf = (1+ tf(index, word, series)) * idf(word)


    #save 
    history_tfidf['%d%s%d' %(index, word, series_no)] = tf_idf
    
    return tf_idf

# print submission title
with open('submission.txt', 'w') as t:
    t.write('Query,RetrievedDocuments\n')


for query_i in range(16):
    print("in query %d" % query_i)

    # dist of query
    print('compute dist query')
    dist_query = 0
    for word in query_series[query_i].index:
        dist_query += math.pow(tf_idf(query_i, word, query_series), 2)
    # print(dist_query)

    sim_array = {}
    for doc_j in range(2265):
        print("in doc %d" % doc_j)

        dot = 0
        print('compute dot')
        for word in query_series[query_i].index:
            dot +=  tf_idf(query_i, word, query_series) * tf_idf(doc_j, word, doc_series)
        # print(dot)
        
        # dist of doc
        print('compute dist doc')
        dist_doc = 0
        for word in doc_series[doc_j].index:
            dist_doc += math.pow(tf_idf(doc_j, word, doc_series), 2)

        sim = dot / ( math.sqrt(dist_query) * math.sqrt(dist_doc) )
        sim_array[docs[doc_j]] = sim


    # sort dict
    print('compute sorting')
    result_turple = sorted(
        sim_array.items(), key=lambda kv: kv[1], reverse=True)

    # print this query result:
    with open('submission.txt', 'a') as t:
        t.write('%s,' % querys[query_i])

        for rt in result_turple:
            t.write('%s ' % rt[0])
        t.write('\n')

    # print(query_series[0])
    # break
    