from django.urls import path, re_path, include
from Book import views as book_view
from django.conf import settings
from django.conf.urls.static import static
from .views import PostDetailView
from django.views.static import serve

urlpatterns = [
    path('', book_view.home, name='book-home'),
    # path('webhook/stripe/', book_view.stripe_webhook, name='stripe-webhook'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='book-detail'),
    path('upvotes/', book_view.upvote.as_view(), name='upvote'),
    path('downloads/', book_view.downloads.as_view(), name='downloads'),
    path('reads/', book_view.reads.as_view(), name='reads'),
    path('fav/', book_view.fav.as_view(), name='fav'),
    path('search', book_view.search, name='search'),
    path('report', book_view.report, name='report'),
    path('genre/<str:pk>', book_view.gen, name='gen'),
    path('webhook/stripe/', book_view.webhook, name='webhook'),
    path('go/<int:id>/<int:type>/create-checkout-session/',
         book_view.create_payment, name='create_checkout'),
    path('go/<int:id>/<int:type>/', book_view.go, name='go'),
    path('success/<str:id>/<str:type>', book_view.success, name="success"),
    path('download/<str:path>', serve,
         {'document_root': settings.MEDIA_ROOT}, name='download'),

    # re_path(r'^download/(?P<path>.*)$', serve,
    #         {'document_root': settings.MEDIA_ROOT}, name='download'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
