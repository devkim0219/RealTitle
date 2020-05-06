from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.template.loader import render_to_string
import json
from .models import Article
from utils.oracleDB import get_data, pagination
from utils.visualize import wordcloud01
import os
import pickle
import time


# Create your views here.

def index(request):
    if request.method == 'GET':
        file_name = 'total_article_ver1_20200427'
    
        # get_article.insertArticle(file_name)
        media_list = get_data.getMediaList()
        # category_list = get_data.getCategoryList()
        # keyword_list = get_data.getKeywordsPerCategory()
        
        # category_list = {'IT과학':['a','b','c','d','e'], '경제':['a','b','c','d','e'], '사회':['a','b','c','d','e'], '생활문화':['a','b','c','d','e'], '세계':['a','b','c','d','e'], '오피니언':['a','b','c','d','e'], '정치':['a','b','c','d','e']}
        dirPath = './output/keyword_logs/'
        fileName_keywordlist = 'category_list_'+time.strftime("%Y%m%d")+'.pickle'
        if os.path.exists(dirPath):
            print('폴더가 있음')
        else :
            os.mkdir(dirPath)
        if os.path.exists(dirPath + fileName_keywordlist):
            with open(dirPath+fileName_keywordlist, 'rb') as f :
                category_list = pickle.load(f)
        else :
            category_list = get_data.getKeywordsPerCategory()
            with open(dirPath+fileName_keywordlist, 'wb') as f:
                pickle.dump(category_list, f, protocol=pickle.HIGHEST_PROTOCOL)

        media_list_arr = []

        for media in media_list:
            media_list_arr.append(media['media_name'])

        media_list_arr.remove('KBS 연예')
        media_list_arr.remove('MBC연예')
        media_list_arr.remove('AP연합뉴스')
        media_list_arr.remove('EPA연합뉴스')
        media_list_arr.remove('일다')
        media_list_arr.remove('참세상')
        media_list_arr.remove('헤럴드POP')

        # return render(request, 'index.html')
        return render(request, 'index.html', {'media_list': media_list_arr, 'category_list': category_list})
        # return render(request, 'index.html', {'media_list': media_list_arr, 'category_list': category_list, 'keyword_list':keyword_list})

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', '')
        media = request.GET.get('media', '')
        category = request.GET.get('category', '')
        page = request.GET.get('page', 1)

        article_list = get_data.searchArticle(search_keyword=search_keyword, media=media, category=category)

        posts, total_count, p_range = pagination.get_pagination(data=article_list, page=page)

        media_list = get_data.getMediaList()
        category_list = get_data.getCategoryList()
        keyword_list = ['딥러닝맨', 'Real Title', '코로나', '날씨']

        return render(request, 'article_list.html', {'search_keyword': search_keyword,
                                                    'media': media,
                                                    'category': category,
                                                    'posts': posts,
                                                    'data': serializers.serialize('json', posts),
                                                    'total_count': total_count,
                                                    'p_range': p_range,
                                                    'media_list': media_list,
                                                    'category_list': category_list,
                                                    'keyword_list': keyword_list})

@csrf_exempt
def article_analysis(request):
    if request.method == 'GET':
        ### 넘어온 id를 받아서 사용.
        art_id = request.GET.get('article_id','') #; print(" article_id >",art_id)
        
        ## raw 쿼리도 가능.
        # theArticle = article.objects.raw('select * from article_article where article_id = %s', [art_id])
        theArticle = Article.objects.filter(article_id = art_id)

        url = theArticle[0].article_url
        content = theArticle[0].article_content
        # print(content)
        wc, bar, count = wordcloud01.generate_wordCloud(content, wordcloud01.setFontPath())
        # print("count >",count)
        return render(request, 'article_analysis.html', { "wordcloud":wc, "barchart":bar,"count":count, "article_url":url })
    


@csrf_exempt
def aritcle_keyword_visualization(request): # 키워드 시각화 페이지
    if request.method == 'GET':
        return render(request, 'aritcle_keyword_visualization.html')
    elif request.is_ajax():
        # print('POST key 값 >', request.POST)
        contents = request.POST['article_content']
        # print('받은 텍스트 >', contents)
        wcURI, barURI, count = wordcloud01.generate_wordCloud( contents, wordcloud01.setFontPath() )
        return HttpResponse(json.dumps({"wordcloudURI":wcURI, "barURI":barURI, "wordCount":count}), "application/json")

@csrf_exempt
def article_chart(request):
    return render(request, 'article_chart.html')

