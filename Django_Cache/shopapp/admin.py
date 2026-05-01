from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.shortcuts import render, redirect

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm
from .utils import save_csv_products, save_csv_orders


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                  queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest,
                    queryset: QuerySet):
    queryset.update(archived=False)


class OrderInLine(admin.TabularInline):
    model = Product.orders.through


class ProductInLine(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'

    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
        ProductInLine,
    ]
    list_display = ('pk', 'name', 'description_short',
                    'price', 'discount', 'archived')
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description', 'discount'
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description'
            ),
        }),
        ('Price options', {
            'fields': (
                'price',
                'discount'
            ),
            # 'classes': ('collapse',),
        }),
        ('Images', {
            'fields': (
                'preview',
            ),
            'classes': ('collapse',),
        }),
        ('Extra options', {
            'fields': (
                'archived',
            ),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete'
        }),
    )

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        save_csv_products(form.files['csv_file'].file, request.encoding)
        self.message_user(request, 'Data from CSV has been imported')
        return redirect('..')
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv'
            ),
        ]
        return new_urls + urls

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInLine(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/orders_changelist.html'

    inlines = [
        ProductInLine,
    ]
    list_display = 'pk', 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    
    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        save_csv_orders(form.files['csv_file'].file, request.encoding)
        self.message_user(request, 'Data from CSV has been imported')
        return redirect('..')
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-csv/',
                self.import_csv,
                name='import_orders_csv'
            ),
        ]
        return new_urls + urls
