from django.urls import path
from .views import newsListView, news_detail, SearchResultsList
from .views import ContactPageView, HomePageView, \
    LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, \
    NewsCreateView, admin_page_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', newsListView, name='all_news_list'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(),  name='news_delete'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:news>/', news_detail,  name='single_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_pages'),
    path('local-news/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign-news/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('technology-news/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport-news/', SportNewsView.as_view(), name='sport_news_page'),
    path('admin-page/', admin_page_view, name='admin_page'),
    path('search-results/', SearchResultsList.as_view(), name='search_results'),
]
