from django.http import JsonResponse
from rest_framework.reverse import reverse as api_reverse

from product.models import ArticleGroup, Article, ArticleImage
from account.models import Stars

def get_article_group_json_obj(obj, request):
    if obj is not None:
        res = {
            "id": obj.id,
            "group_name": obj.group_name,
            "description": obj.description,
            "articles": [],
            "link": obj.link,
            "uri": api_reverse("product:article_group", kwargs={"id": obj.id}, request=request)
        }

        res['articles'] = get_article_detail(obj, request)

    return JsonResponse(res, status=200)

def get_article_detail(obj, request):
    articles = []

    for art in obj.article_ids.all():
        art = Article.objects.get(id=art.id)
        qs_images = ArticleImage.objects.filter(article_id=art.id)

        profile_image = None
        for img in qs_images:
            if profile_image is None:
                profile_image = request.get_host() + img.image.url
            if img.purpose == '#profile_image':
                profile_image = request.get_host() + img.image.url
                break

        qs_stars = Stars.objects.filter(article_id=art.id)
        avg_rate = 0
        if qs_stars.exists():
            for q in qs_stars:
                avg_rate = avg_rate + q.value
            avg_rate = avg_rate / len(qs_stars)

        art_ser = {
            "article_code": art.article_code,
            "article_name": art.article_name,
            "profile_picture": profile_image,
            "uri": api_reverse("product:article", kwargs={"id": obj.id}, request=request),
            "avg_rate": avg_rate,
            "price": art.price
        }

        articles.append(art_ser)
    
    return articles