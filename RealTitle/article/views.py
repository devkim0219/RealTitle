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


# Create your views here.
def index(request):
    if request.method == 'GET':
        file_name = 'total_article_ver1_20200427'
    
        # get_article.insertArticle(file_name)

        media_list = get_data.getMediaList()
        category_list = get_data.getCategoryList()

        media_list_arr = []

        for media in media_list:
            media_list_arr.append(media['media_name'])

        media_list_arr.remove('KBS 연예')
        media_list_arr.remove('MBC연예')

        # return render(request, 'index.html')
        return render(request, 'index.html', {'media_list': media_list_arr, 'category_list': category_list})

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', '')
        media = request.GET.get('media', '')
        category = request.GET.get('category', '')
        page = request.GET.get('page', 1)

        article_list = get_data.searchArticle(search_keyword=search_keyword, media=media, category=category)
        posts, total_count, p_range = pagination.pagination(data=article_list, page=page)

        media_list = get_data.getMediaList()
        category_list = get_data.getCategoryList()
        keyword_list = ['딥러닝맨', 'Real Title', '코로나', '날씨']

        return render(request, 'article_list.html', {'search_keyword': search_keyword, 
                                                    'media': media, 
                                                    'category': category, 
                                                    'posts': posts, 
                                                    'total_count': total_count, 
                                                    'p_range': p_range, 
                                                    'media_list': media_list, 
                                                    'category_list': category_list, 
                                                    'keyword_list': keyword_list})
    
    elif request.method == 'POST':
        search_keyword = request.POST.get('search_keyword', '')
        media = request.POST.get('media', '')
        category = request.POST.get('category', '')
        page = request.GET.get('page', 1)
        sort_method = request.POST.get('sort_method', '')

        print(search_keyword, media, category, page, sort_method, type(sort_method))

        if sort_method == 'desc':
            article_list = get_data.searchArticle(search_keyword=search_keyword, media=media, category=category)
        
        elif sort_method == 'asc':
            article_list = get_data.searchArticle(search_keyword=search_keyword, media=media, category=category, sort_method=sort_method)

        posts, total_count, p_range = pagination.pagination(data=article_list, page=page)

        media_list = get_data.getMediaList()
        print("media_list",media_list)
        category_list = get_data.getCategoryList()
        keyword_list = ['딥러닝맨', 'Real Title', '코로나', '날씨']

        return HttpResponse(json.dumps({'search_keyword': search_keyword, 
                                        'media': media, 
                                        'category': category, 
                                        'posts': serializers.serialize('json', posts), 
                                        'total_count': total_count, 
                                        'p_range': list(p_range), 
                                        'media_list': list(media_list), 
                                        'category_list': list(category_list), 
                                        'keyword_list': keyword_list, 
                                        'sort_method': sort_method}), 'application/json')

@csrf_exempt
def article_analysis(request):
    if request.method == 'GET':
        ### 넘어온 id를 받아서 사용.
        art_id = request.GET.get('article_id','') # print(" article_id >",art_id)
        
        ## raw 쿼리도 가능.
        # theArticle = article.objects.raw('select * from article_article where article_id = %s', [art_id])
        theArticle = Article.objects.filter(article_id = art_id)

        # print(dir(theArticle))
        # print(theArticle[0].article_content)
        content = theArticle[0].article_content
        print(content)
        wc, bar, count = wordcloud01.generate_wordCloud(content, wordcloud01.setFontPath())
        print("count >",count)
        return render(request, 'article_analysis.html', { "wordcloud":wc, "barchart":bar,"count":count })
    


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


##### render_to_string을 이용해서 맹글어서 보내기. ### test.html과 article_keyword_table_contents.html 필요
# @csrf_exempt
# def renderToStringTest(request):
#     if request.method == 'GET':
#         return render(request, 'test.html')
#     elif request.is_ajax():
#         ### querry = r""" select * from article_article """
#         ### test01 = article.objects.raw(querry)
#         ### print(test01[0])
#         ### print(dir(article.objects.all()[0]))
#         ### print(article.objects.all()[0])
#         ### querry = r""" select * from article_article where article_category=%s """
#         ### test = article.objects.raw(querry,['사회'] )
#         ### print(test[0])
#         ### dishes = json.dumps([{"article_title":"기사제목1", "article_content":"내용1"},{"article_title":"기사제목2", "article_content":"내용2"}], ensure_ascii=False, )
#         ### dishes = [{"article_title":"기사제목1", "article_content":"내용1"},{"article_title":"기사제목2", "article_content":"내용2"}]
#         ### dishes = article.objects.all().values()[0];dishes = [dishes]
#         dishes = article.objects.all().values()[:10]
#         print(dishes, type(dishes))
#         ### print(dishes['word'])
#         html = render_to_string('article_keyword_table_contents.html', {'dishes': dishes})
#         ### html = None
#         return HttpResponse(html)
#         pass