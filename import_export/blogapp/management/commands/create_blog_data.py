import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from blogapp.models import Author, Category, Tag, Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo blog')

        categories = []
        for i in range(5):
            cat, _ = Category.objects.get_or_create(name=f'Category {i+1}')
            categories.append(cat)

        tags = []
        for i in range(9):
            tag, _ = Tag.objects.get_or_create(name=f'Tag_{i+1}')
            tags.append(tag)

        authors = []
        for i in range(3):
            author, _ = Author.objects.get_or_create(
                name=f'Author {i+1}',
                bio=f'Author #{i+1} bio.'
            )
            authors.append(author)

        fake_words = ['Django', 'Python', 'Web', 'Code', 'Fast', 'Logic', 'Dev', 'Backend', 'Frontend', 'Base']
        for i in range(7):
            content = " ".join(random.choices(fake_words, k=10))
            article = Article.objects.create(
                title=f"Article #{i+1} Title",
                content=content,
                pub_date=now(),
                author=random.choice(authors),
                category=random.choice(categories),
            )
            selected_tags = random.sample(tags, k=random.randint(1, 3))
            article.tags.set(selected_tags)

        self.stdout.write('End demo')
