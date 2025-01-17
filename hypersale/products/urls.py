from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, DiscountViewSet, ProductViewSet, OrderViewSet, ReviewViewset, WishlistViewset, APIRootView
from rest_framework.authtoken.views import obtain_auth_token 

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'wishlist', WishlistViewset)
router.register(r'reviews', ReviewViewset)
router.register(r'discounts', DiscountViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', APIRootView.as_view(), name='api-root'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
