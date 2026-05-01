from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse

from .models import Article


class ArticleListView(ListView):
    queryset = (
        Article.objects
            .filter(pub_date__isnull=False)
            .order_by('-pub_date')
    )
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    # template_name = ".html"


class LatestArticlesFeed(Feed):
    title = 'Latest articles'
    description = 'Latest hot new free updates'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return (
            Article.objects
                .filter(pub_date__isnull=False)
                .order_by('-pub_date')[:5]
        )
    
    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:20] + '...'
