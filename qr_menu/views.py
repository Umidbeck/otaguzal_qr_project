from django.utils.translation import activate, get_language
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Product, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        current_lang = get_language()
        lang = request.GET.get('lang')

        if lang and lang in dict(settings.LANGUAGES) and lang != current_lang:
            # Tilni darhol faollashtiramiz
            activate(lang)
            # Cookie ni yangilaymiz va redirect qilamiz
            response = HttpResponseRedirect(f'/{lang}/' if lang != 'en' else '/')
            response.set_cookie('django_language', lang, max_age=3600 * 24 * 365)
            return response

        self.extra_context = {
            'categories': Category.objects.all(),
        }
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.all()


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name_en = request.POST['name_en']
        product.name_uz = request.POST['name_uz']
        product.name_ru = request.POST['name_ru']
        product.description_en = request.POST['description_en']
        product.description_uz = request.POST['description_uz']
        product.description_ru = request.POST['description_ru']
        product.price = request.POST['price']
        product.category_id = request.POST['category']
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "Mahsulot muvaffaqiyatli tahrirlandi!")
        return redirect('home')
    return render(request, 'admin/edit_product.html', {'product': product, 'categories': Category.objects.all()})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Mahsulot muvaffaqiyatli o'chirildi!")
        return redirect('home')
    return render(request, 'admin/delete_product.html', {'product': product})


@login_required
def add_product(request):
    if request.method == 'POST':
        name_en = request.POST['name_en']
        name_uz = request.POST['name_uz']
        name_ru = request.POST['name_ru']
        description_en = request.POST['description_en']
        description_uz = request.POST['description_uz']
        description_ru = request.POST['description_ru']
        price = request.POST['price']
        category_id = request.POST['category']
        image = request.FILES.get('image')
        Product.objects.create(
            name_en=name_en, name_uz=name_uz, name_ru=name_ru,
            description_en=description_en, description_uz=description_uz, description_ru=description_ru,
            price=price, category_id=category_id, image=image
        )
        messages.success(request, "Yangi mahsulot muvaffaqiyatli qo'shildi!")
        return redirect('home')
    return render(request, 'admin/add_product.html', {'categories': Category.objects.all()})
