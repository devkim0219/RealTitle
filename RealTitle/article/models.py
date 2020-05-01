from django.db import models

# Create your models here.
class Article(models.Model):
    objects = models.Manager()  # VS code오류 제거용
    article_id = models.CharField(primary_key=True, max_length=20)	
    article_url	= models.CharField(max_length=100)
    article_category = models.CharField(max_length=50)
    article_media = models.CharField(max_length=50)
    article_date = models.CharField(max_length=20)
    article_title = models.CharField(max_length=200)
    article_content = models.TextField()

    def __str__(self):
        return (self.article_id) # 문자만 가능


#### Team 계정(실전) 에서 사용 할것.
# Create your models here.
# class article(models.Model):
#     objects = models.Manager()  # VS code오류 제거용
#     article_id = models.CharField(primary_key=True, max_length=20)	
#     article_url	= models.CharField(max_length=100)
#     article_category = models.CharField(max_length=50)
#     article_media = models.CharField(max_length=50)
#     article_date = models.CharField(max_length=20)
#     article_title = models.CharField(max_length=200)
#     article_content = models.TextField()
#     article_newtitle = models.CharField(max_length=200)
#     article_newsacc  = models.FloatField()
#     article_mediaacc = models.FloatField()

#     def __str__(self):
#         return (self.article_id) # 문자만 가능