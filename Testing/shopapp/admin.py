from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
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
        ('Extra options', {
            'fields': (
                'archived',
                'created_by',
            ),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete'
        }),
    )
    

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInLine(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine,
    ]
    list_display = 'pk', 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    
    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

