from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

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