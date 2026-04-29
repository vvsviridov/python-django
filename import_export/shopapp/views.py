import logging

from csv import DictWriter

from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.syndication.views import Feed

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

from shopapp.models import Product, Order, ProductImage

from .forms import ProductForm, OrderForm
from .serializers import ProductSerializer, OrderSerializer
from .utils import save_csv_products, save_csv_orders


log = logging.getLogger(__name__)


@extend_schema(description='extend_schema description')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений (ViewSet) для управления товарами.

    Обеспечивает стандартные действия CRUD: список, создание, просмотр, 
    обновление и удаление товаров.
    
    Поддерживает:
    - Поиск по полям: название и описание.
    - Сортировку по: названию, цене и скидке.
    - Фильтрацию по: названию, описанию, цене, скидке и статусу архивации.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'discount']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieve **products**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    
    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = ('attachment; '
                                           f'filename={filename}')
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        csv_writer = DictWriter(response, fieldnames=fields)
        csv_writer.writeheader()
        for obj in queryset:
            csv_writer.writerow({
                field: getattr(obj, field)
                for field in fields
            })
        return response
    
    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class LatestProductsFeed(Feed):
    title = 'Latest prdoucts'
    description = 'Latest hot new free prdoucts'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects
                .filter(created_at__isnull=False)
                .order_by('-created_at')[:5]
        )
    
    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:20] + '...'


class OrderViewSet(ModelViewSet):
    """
    Набор представлений (ViewSet) для управления заказами.

    Позволяет просматривать список заказов, создавать новые, а также 
    редактировать или удалять существующие заказы.

    Поддерживает:
    - Поиск по полям: пользователь, адрес доставки, состав продуктов и промокод.
    - Сортировку по: пользователю, дате создания и адресу доставки.
    - Фильтрацию по: пользователю, адресу доставки и промокоду.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['user', 'delivery_address', 'products', 'promocode']
    ordering_fields = ['user', 'created_at', 'delivery_address']
    filterset_fields = [
        'user',
        'delivery_address',
        'promocode',
    ]

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'orders-export.csv'
        response['Content-Disposition'] = ('attachment; '
                                           f'filename={filename}')
        queryset = self.filter_queryset(self.get_queryset())
        fields = ['user', 'delivery_address', 'products', 'promocode']
        queryset = queryset.select_related('user').prefetch_related('products')
        csv_writer = DictWriter(response, fieldnames=fields)
        csv_writer.writeheader()
        for obj in queryset:
            data = self.get_serializer(obj).data
            csv_writer.writerow({
                field: data.get(field) for field in fields
            })
        return response
    
    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        orders = save_csv_orders(
            request.FILES['file'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'data': [
                {
                    "userId": 1,
                    "id": 1,
                    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
                },
                {
                    "userId": 1,
                    "id": 2,
                    "title": "qui est esse",
                    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
                },
                {
                    "userId": 1,
                    "id": 3,
                    "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",
                    "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"
                },
                {
                    "userId": 1,
                    "id": 4,
                    "title": "eum et est occaecati",
                    "body": "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"
                },
                {
                    "userId": 1,
                    "id": 5,
                    "title": "nesciunt quas odio",
                    "body": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"
                },
                {
                    "userId": 1,
                    "id": 6,
                    "title": "dolorem eum magni eos aperiam quia",
                    "body": "ut aspernatur corporis harum nihil quis provident sequi\nmollitia nobis aliquid molestiae\nperspiciatis et ea nemo ab reprehenderit accusantium quas\nvoluptate dolores velit et doloremque molestiae"
                },
            ],
            'items': 1,
        }
        log.debug('Products for shop index: %s', context['data'])
        log.info('Rendering shop index')
        return render(request, 'shopapp/shop_index.html', context=context)


class ProductsView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductsDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'discount', 'preview']
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    # fields = ['name', 'price', 'description', 'discount', 'preview']
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        for img in self.request.FILES.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=img,
            )
        return response


    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersView(ListView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderDetailsView(DetailView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderCreateView(CreateView):
    model = Order
    fields = ['delivery_address', 'promocode', 'user', 'products']
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['delivery_address', 'promocode', 'user', 'products']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': p.pk,
                'name': p.name,
                'price': str(p.price),
                'archived': p.archived,
                'created_by': request.user.pk,
            }
            for p in products
        ]
        elem = products_data[0]
        name = elem['name']
        print('name:', name)
        return JsonResponse({'products': products_data})
