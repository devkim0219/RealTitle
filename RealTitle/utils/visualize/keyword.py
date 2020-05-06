from konlpy.tag import Hannanum
from collections import Counter
from . import wordcloud01
import numpy as np
import pandas as pd
import re

## 
def text_preprocessing(queryset):
    # print(queryset,len(queryset))
    hannanum = Hannanum()
    getNum = 5
    stopword = ['등','코','만','속보','최초','4억', '월요일']
    df = pd.DataFrame.from_records( queryset )
    # print(df, type(df))
    # df['title_nouns'] = df['article_title'].apply( lambda x : hannanum.nouns( wordcloud01.clean_text( x ) ) ); print(df['title_nouns']); print(df['title_nouns'].sum())
    # print('apply시작')
    df['title_nouns'] = df['article_title'].apply( lambda x : Counter( hannanum.nouns( wordcloud01.clean_text( x ) ) ) )
    # print('sum시작')
    total_counter = df['title_nouns'].sum()
    # print('stopword')
    for word in stopword:
        del total_counter[word] 
    # print(type(total_counter), total_counter.most_common( getNum ))
    result = total_counter.most_common( getNum )
    return result


def text_preprocessing_after(lists):
    hannanum = Hannanum()
    getNum = 5
    stopword = ['등','코','만','속보','최초','4억', '월요일']
    cleaning = lambda x: hannanum.nouns( wordcloud01.clean_text( x ) )
    nouns_list = list(map( cleaning, lists ))

    # print(nouns_list)

    texts = [ value for nouns in nouns_list for value in nouns ]
    total_counter = Counter( texts )
    for word in stopword:
        del total_counter[word] 
    result = total_counter.most_common( getNum )
    return result



## 명사 빈도 추출.
def nouns_frequency(text):
    print('Kkma 객체 생성')
    hannanum = Kkma()
    print('텍스트 처리중')
    clean_text = wordcloud01.clean_text(text)
    print('텍스트 명사 처리중')
    words = hannanum.nouns(clean_text)
    print('평평하게 만들기')
    word_list = wordcloud01.flatten(words)
    print('판다스 변환중')
    word_list = pd.Series([x for x in word_list if len(x)>1])
    print('result Counter 중')
    result = Counter(word_list)
    return result





# {% for v in keyword_list %}
#                                     <a href="/article_list?category={{ category.category_name }}&search_keyword={{v[0]}}">{{v[0]}}</a>
#                                     {% endfor  %}