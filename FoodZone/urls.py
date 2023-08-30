from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index,name='index'),
    path('contact/', views.contact_us, name='contact'),
    path('about/', views.About, name='about'),
    path('register/', views.Register, name='register'),
    path('login/',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('dish/<int:id>/', views.single_dish, name='dish'),
    path('team/',views.team_members,name="team"),
    path('dishes/',views.all_dishes,name="all_dishes"),
    path('booking', views.Booking, name='booking'),
    path('items/<int:id>',views.Items,name='items'),
    path('item_details/<int:id>',views.Item_Details,name='item_details'),

    #payment
    path('paypal/',include('paypal.standard.ipn.urls')),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
