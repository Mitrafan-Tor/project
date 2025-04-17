from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache # импортируем наш кэш
from .models import Product

class ProductDetailView(DetailView):
   template_name = 'sample_app/product_detail.html'
   queryset = Product.objects.all()

   def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно

      obj = cache.get(f'product-{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

      #если объекта нет в кэше, то получаем его и записываем в кэш

      if not obj:
         obj = super().get_object(queryset=self.queryset)
         cache.set(f'product-{self.kwargs["pk"]}', obj)

      return obj

from .filters import ProductFilter
from .forms import ProductForm
from .models import Product



class ProductsList(PermissionRequiredMixin, ListView):
    model = Product
    ordering = 'name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 10
    permission_required = ('simpleapp.view_product',)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ProductDetail(PermissionRequiredMixin, DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    permission_required = ('simpleapp.view_product',)


class ProductCreate(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
    permission_required = ('simpleapp.add_product',)


class ProductUpdate(PermissionRequiredMixin,LoginRequiredMixin,  UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
    permission_required = ('simpleapp.change_product',)

# Представление удаляющее товар.
class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = ('simpleapp.delete_product', )

class AddProduct(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product', )
    model = Product  # Указываем модель
    fields = ['name', 'description', 'quantity', 'price']  # Указываем поля для формы
    template_name = 'shop/add_product.html'  # Указываем шаблон
    success_url = reverse_lazy('products')  # Перенаправление после успешного создания