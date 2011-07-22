from django.http import HttpResponse
from tagging.models import Tag
from cmsplugin_news.models import News
from django.utils import simplejson
from django.core import serializers
from datetime import datetime

def pull(request, **kwargs):
    #raise Exception("Got arguments: %s, %s" % (request, kwargs))
    response = HttpResponse(content_type="application/json")
    delimiter = "_"
    tail = kwargs['tagnames']
    tags = []
    
    
    #explode URL to tag list
    while delimiter != '':
        (tag, delimiter, tail) = tail.partition(delimiter)
        tags += [tag]
    existing_tags = Tag.objects.all()
    
    #test, which tags exist 
    tags_found = []
    for existing_tag in existing_tags:
        for tag in tags:
            if existing_tag.name == tag:
                tags_found += [existing_tag]
                tags.remove(tag)
                break
    #response.write("<h3>Found tags:</h3> <br />")    
    
    #search for related news
    tag_ids = []
    for tag in tags_found:
        #response.write("%s <br />" % tag.name)    
        tag_ids += [tag.id]
    news_found = News.objects.filter(tags__id__in = tag_ids)
    #news_found.order_by("pub_date")
    #news_found = news_found.reverse()
    news_found = news_found.distinct()
    news_found = list(news_found)
    
    def compare_news(item1, item2):
        if item1.pub_date > item2.pub_date:
            return 1
        elif item1.pub_date < item2.pub_date:
            return -1
        else:
            return 0
    #print news
    #response.write("<h3>Found news:</h3> <br />")    
    #news_found.sort(compare_news,reverse=True)
    if len(news_found):
        #news_simple = []
        #for news_item in news_found:
        #    #response.write("%s %s <br />" % (news_item.pub_date, news_item.title))
        #    news_item_simple = {
        #        "pub_date":news_item.pub_date,
        #        "title":news_item.title,
        #        "excerpt":news_item.excerpt,
        #        "content":news_item.content,
        #        "url":"newsurl"}
        #    news_simple += [news_item_simple]
        news = []
        for news_item in news_found:
            news_item.url = "news_url"
            news += [news_item]
        #news_json = simplejson.dumps(news_simple)
        news_serialized = serializers.serialize("json", news)
        response.write(news_serialized)
    else:
        raise Exception("No records found for tags specified")
    
    return response
    
def pull_simple(request, **kwargs):
    """
        Дергает новости не в виде объектов CMSPluginNews,
        а в виде dict'ов
    """
    #raise Exception("Got arguments: %s, %s" % (request, kwargs))
    response = HttpResponse(content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    delimiter = "_"
    tail = kwargs['tagnames']
    tags = []
    
    
    #explode URL to tag list
    while delimiter != '':
        (tag, delimiter, tail) = tail.partition(delimiter)
        tags += [tag]
    existing_tags = Tag.objects.all()
    
    #test, which tags exist 
    tags_found = []
    for existing_tag in existing_tags:
        for tag in tags:
            if existing_tag.name == tag:
                tags_found += [existing_tag]
                tags.remove(tag)
                break
    #response.write("<h3>Found tags:</h3> <br />")    
    
    #search for related news
    tag_ids = []
    for tag in tags_found:
        #response.write("%s <br />" % tag.name)    
        tag_ids += [tag.id]
    news_found = News.objects.filter(tags__id__in = tag_ids)
    #news_found.order_by("pub_date")
    #news_found = news_found.reverse()
    news_found = news_found.distinct()
    news_found = list(news_found)
    
    def compare_news(item1, item2):
        if item1.pub_date > item2.pub_date:
            return 1
        elif item1.pub_date < item2.pub_date:
            return -1
        else:
            return 0
    #print news
    #response.write("<h3>Found news:</h3> <br />")    
    #news_found.sort(compare_news,reverse=True)
    if len(news_found):
        #news_simple = []
        #for news_item in news_found:
        #    #response.write("%s %s <br />" % (news_item.pub_date, news_item.title))
        #    news_item_simple = {
        #        "pub_date":news_item.pub_date,
        #        "title":news_item.title,
        #        "excerpt":news_item.excerpt,
        #        "content":news_item.content,
        #        "url":"newsurl"}
        #    news_simple += [news_item_simple]
        def is_published(news_item):
            if (not news_item.pub_date) or (news_item.pub_date>=datetime.now()):
                return False
            if news_item.unpub_date and news_item.unpub_date<=datetime.now():
                return False
            return news_item.is_published
        news_record = lambda news_item: {
            "pub_date":None if news_item.pub_date is None else news_item.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "unpub_date":None if news_item.unpub_date is None else news_item.unpub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "is_published":is_published(news_item),
            "title":news_item.title,
            "excerpt":news_item.excerpt,
            "content":news_item.content,
            "tags":[tag.name for tag in news_item.tags.all()],
            "url":news_item.get_absolute_url()}
        news = [news_record(news_item) for news_item in news_found]
        #news = []
        #for news_item in news_found:
        #    news_item.url = "news_url"
        #    news += [news_item]
        #news_json = simplejson.dumps(news_simple)
        #news_serialized = serializers.serialize("json", news)
        serializers._load_serializers()
        news_serialized = serializers.json.simplejson.dumps(news)
        response.write(news_serialized)
    else:
        raise Exception("No records found for tags specified")
    
    return response
