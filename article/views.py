import random
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.


def article_list(request):
    query = request.GET.get('q')
    articles = Article.objects.search(query=query)
    paginator = Paginator(articles, 3)
    page_number = request.GET.get("page")
    page_qs = paginator.get_page(page_number)
    context = {
        'object_list': page_qs
    }
    return render(request, 'article/index.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        'object': article
    }
    return render(request, 'article/detail.html', context)


def article_create(request):
    context = {
        "created": False
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        obj = Article.objects.create(title=title, content=content,)
        context['created'] = True
        context['object'] = obj
        messages.success(request, 'Article success fully created')
    return render(request, 'article/create.html', context)


def article_creat_form(request):
    form = ArticleForm(None or request.POST, files=request.FILES)
    if form.is_valid():
        obj = form.save()
        reverse_url = reverse('article:detail', args=[obj.slug])
        messages.success(request, 'Article success fully created form')
        return redirect(reverse_url)
    context = {
        'form': form
    }
    return render(request, 'article/create_form.html', context)


def article_change(request, slug):
    obj = Article.objects.get(slug=slug)
    form = ArticleForm(instance=obj)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=obj, files=request.FILES)
        if form.is_valid():
            form.save()
            reverse_url = reverse('article:change-form', kwargs={'slug': obj.slug})
            messages.success(request, 'Article success fully change')
            return redirect(reverse_url)
    context = {
        'form': form,
        'object': obj,
    }
    return render(request, 'article/edit.html', context)


@login_required(login_url='auth:login')
@permission_required(perm='request.user.is_admin', login_url='/',  raise_exception='You have no enough prermission to delete')
def article_delete(request, slug):
    obj = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        obj.delete()
        messages.error(request, 'Article success fully delete')
        return redirect('article:list')
    context = {
        'object': obj
    }
    return render(request, 'article/delete.html', context)




