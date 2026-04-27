from django.views.generic import ListView
from .models import Article

class ArticleListView(ListView):
    queryset = (
        Article.objects
        .select_related("author", "category")
        .prefetch_related("tags")
        .all()
    )
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"
