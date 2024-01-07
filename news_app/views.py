from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from config.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category
from .forms import ContactForm, CommentForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.db.models import Q, Count


def newsListView(request):
    news_list = News.objects.filter(status=News.Status.Published)
    contex = {
        "news_list": news_list
    }

    return render(request, 'news/home.html', contex)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'news/single_page.html', context)


# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:5]
#     uzbek_news_one = News.published.filter(category__name="O'zbekiston").order_by('-publish_time')[:1]
#     uzbek_news = News.published.all().filter(category__name="O'zbekiston")[1:6]
#
#     contex = {
#         'news_list': news_list,
#         'categories': categories,
#         'uzbek_news': uzbek_news,
#         'uzbek_news_one': uzbek_news_one,
#     }
#
#     return render(request, 'news/home.html', contex)


# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
#     contex = {
#     'form': form
#     }
#
#     return render(request, 'news/contact.html', contex)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        contex = {
            'form': form
        }
        return render(request, 'news/contact.html', contex)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
        contex = {
            'form': form
        }
        return render(request, 'news/contact.html', contex)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:20]
        context['mahalliy_xabarlar'] = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlari'] = News.published.filter(category__name="Xorij").order_by('-publish_time')[:5]
        context['texnologiya_xabarlari'] = News.published.filter(category__name="Texnologiya").order_by('-publish_time')[:5]
        context['sport_xabarlari'] = News.published.filter(category__name="Sport").order_by('-publish_time')[:5]

        return context


class LocalNewsView(ListView):
    model = News
    template_name = "news/mahalliy.html"
    context_object_name = "mahalliy_yangiliklar"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = "news/xorij.html"
    context_object_name = "xorij_yangiliklari"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Xorij")
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = "news/texnologiya.html"
    context_object_name = "texnologiya_yangiliklari"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Texnologiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = "sport_yangiliklari"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Sport")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'cud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'cud/news_delete.html'
    success_url = reverse_lazy("home_page")


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'cud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru', 'body', 'body_uz', 'body_en', 'body_ru', 'image', 'category', 'status')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )