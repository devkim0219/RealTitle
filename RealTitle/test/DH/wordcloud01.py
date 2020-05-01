# import seaborn as sns; sns.set(style='darkgrid', font='malgun', font_scale=1.5)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# !conda install -c anaconda cx_oracle
import cx_Oracle as oci

#!conda install -c conda-forge wordcloud
from wordcloud import WordCloud 
from collections import Counter
import pandas as pd

import platform
import os

from base64 import b64encode
import io
import urllib


## 폰트 경로 및 파일 확인
# fm.fontManager.ttflist
# [f.fname for f in fm.fontManager.ttflist]

def FontList():
    return [f.fname for f in fm.fontManager.ttflist]

def setFontPath():
    ## OS별 폰트 경로 잡기 및 설정
    OSNAME = platform.system()
    if OSNAME == 'Linux':
        # print(OSNAME,'True')
        os.putenv("NLS_LANG", "KOREAN_KOREA.KO16KSC5601")
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        return font_path
    else :
        # print(OSNAME,'False')
        font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
        return font_path

def setFont( font_path ):
    
    font_name = fm.FontProperties(fname=font_path, size=50).get_name()
    print(font_name)
    plt.rc('font', family=font_name)


### konlpy시작
from konlpy.tag import Hannanum


def flatten(I):
    flatList = []
    for elem in I:
        if type(elem) == list:
            for e in elem:
                flatList.append(e)
        else:
            flatList.append(elem)
    return flatList

def generate_wordCloud(text, font_path):
    hannanum = Hannanum()
    words = hannanum.nouns(text)
    word_list = flatten(words)
    word_list = pd.Series([x for x in word_list if len(x)>1])
    # print( word_list.value_counts().head(20) )
    stopwordList = ['’','”','‘','·','…','"',"'"]
    wordcloud = WordCloud(font_path=font_path
                        , stopwords=stopwordList
                        , width=800, height=800
                        , background_color='white')

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)
    array = wordcloud.to_array()

    fig = plt.figure(figsize=(10,10))
    plt.imshow(array, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return uri

    # plt.show()

if __name__ == "__main__":
    setFont( setFontPath() )




########################## TEST 용 #################################
def test():
    setFont()
    hannanum = Hannanum()
    #DB Connecion    
    # conn = oci.connect("test/1234@192.168.0.52:32764/xe", charset='utf8')
    conn = oci.connect('test','1234','192.168.0.52:32764/xe', encoding='utf-8')
    df = pd.read_sql('select * from article_sample', conn )
    sample1 = df['ARTICLE_CONTENT'][0].read()
    word = hannanum.nouns(sample1)
    word_list = flatten(word)
    word_list = pd.Series([x for x in word_list if len(x)>1])
    print( word_list.value_counts().head(20) )
    stopwordList = ''
    wordcloud = WordCloud(font_path=setFontPath()
                        , stopwords=stopwordList
                        , width=800, height=800
                        , background_color='white')

    count = Counter(word_list)
    wordcloud = wordcloud.generate_from_frequencies(count)
    array = wordcloud.to_array()

    fig = plt.figure(figsize=(10,10))
    plt.imshow(array, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    # plt.savefig('C:/Users/admin/Documents/IMG04.png', bbox_inches='tight')