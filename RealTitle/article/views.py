from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from test.JH import get_article, pagination
from test.DH import wordcloud01

# Create your views here.
def index(request):
    if request.method == 'GET':
        file_name = 'total_article_ver1_20200427'
        
        get_article.insertArticle(file_name)

        # media_list = get_article.getMediaList()
        # category_list = get_article.getCategoryList()

        return render(request, 'index.html')
        # return render(request, 'index.html', {'media_list': media_list, 'category_list': category_list})

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', '')
        media = request.GET.get('media', '')
        category = request.GET.get('category', '')
        page = request.GET.get('page', 1)

        article_list = get_article.searchArticle(search_keyword=search_keyword, media=media, category=category)
        posts, total_count, p_range = pagination.pagination(data=article_list, page=page)

        media_list = get_article.getMediaList()
        category_list = get_article.getCategoryList()
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
            article_list = get_article.searchArticle(search_keyword=search_keyword, media=media, category=category)
        
        elif sort_method == 'asc':
            article_list = get_article.searchArticle(search_keyword=search_keyword, media=media, category=category, sort_method=sort_method)

        posts, total_count, p_range = pagination.pagination(data=article_list, page=page)

        # for post in posts:
        #     print(post.article_title)
        # print('*'*100)
        # for post in reversed(posts):
        #     print(post.article_title)
        # print("post",posts.object_list.values())

        media_list = get_article.getMediaList()
        print("media_list",media_list)
        category_list = get_article.getCategoryList()
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

def article_analysis(request):
    if request.method == 'GET':
        return render(request, 'article_analysis.html')


@csrf_exempt
def aritcle_keyword_visualization(request): # 키워드 시각화 페이지
    if request.method == 'GET':
        return render(request, 'aritcle_keyword_visualization.html')
    elif request.is_ajax():
        # print('POST key 값 >', request.POST)
        contents = request.POST['article_content']
        # print('받은 텍스트 >', contents)
        uri = wordcloud01.generate_wordCloud( contents, wordcloud01.setFontPath() )
        return HttpResponse(json.dumps({"wordcloudURI":uri}), "application/json")