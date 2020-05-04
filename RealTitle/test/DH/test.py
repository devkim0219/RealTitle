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
