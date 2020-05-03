from django.db.models import Q
from django.db import connection
from article.models import Article, Media, Category
import pandas as pd

def getMediaList():
    # 언론사 리스트
    # media_list = Media.objects.raw('SELECT MEDIA_NAME FROM ARTICLE_MEDIA')
    media_list = Media.objects.values('media_name')
    return media_list

def getCategoryList():
    # 카테고리 리스트
    # category_list = Category.objects.raw('SELECT CATEGORY_NAME FROM ARTICLE_CATEGORY')
    category_list = Category.objects.values('category_name')
    return category_list

def searchArticle(search_keyword, media, category, sort_method='desc'):
    if sort_method == 'desc':
        order_by_val = '-article_date'
    
    elif sort_method == 'asc':
        order_by_val = 'article_date'

    if search_keyword != '':
        # 언론사, 검색어 둘 다 있을 때
        if media != '':
            article_list = Article.objects.filter(article_media = media).filter(article_title__icontains=search_keyword).order_by(order_by_val)

        # 카테고리, 검색어 둘 다 있을 때
        elif category != '':
            article_list = Article.objects.filter(article_category = category).filter(article_title__icontains=search_keyword).order_by(order_by_val)

        # 검색어만 있을 때
        else:
            # article_list = Article.objects.filter(Q(article_title__icontains=search_keyword) | Q(article_content__icontains=search_keyword)).order_by('-article_date')
            article_list = Article.objects.filter(article_title__icontains=search_keyword).order_by(order_by_val)

    else:
        # 언론사만 있을 때
        if media != '':
            article_list = Article.objects.filter(article_media = media).order_by(order_by_val)

        # 카테고리만 있을 때
        elif category != '':
            article_list = Article.objects.filter(article_category = category).order_by(order_by_val)

        # 전체 리스트
        else:
            # article_list = Article.objects.raw('SELECT * FROM ARTICLE_ARTICLE ORDER BY ARTICLE_DATE DESC')
            article_list = Article.objects.all().order_by(order_by_val)
            
    return article_list

def insertArticle(file_name):
    df = pd.read_sql('select article_id from article_article group by article_id', connection)

    df.columns = ['article_id']
    df['check'] = 1

    df2 = pd.read_csv('data/' + file_name + '.csv')

    df_merge = pd.merge(df, df2, how='outer')

    df_result = df_merge[df_merge['check'].isna()]
    df_result.drop('check', axis=1, inplace=True)

    print(df_result.head())
    print(df_result.columns)
    print(df_result.shape)

    # f = pd.read_csv('data/' + file_name + '.csv')
    # df = f[f [f['article_category'] == '사회' ].index[0]:]

    # print(df.head())
    # print(df.columns)
    # print(df.shape)

    df1 = df_result[['article_id', 'article_url', 'article_category', 'article_media', 'article_date', 'article_title', 'article_content']]
    rows = [tuple(x) for x in df1.to_records(index=False)]

    for line in rows:
        # print(line)
        article_id = line[0]
        article_url = line[1]
        article_category = line[2]
        article_media = line[3]
        article_date = line[4]
        article_title = line[5]
        article_content = line[6]

        article = Article(article_id=article_id, 
                        article_url=article_url, 
                        article_category=article_category, 
                        article_media=article_media, 
                        article_date=article_date, 
                        article_title=article_title, 
                        article_content=article_content)
        article.save()

        print(article_id, 'insert complete')