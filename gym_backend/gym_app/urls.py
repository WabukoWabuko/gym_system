from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'members', views.MemberViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'blogposts', views.BlogPostViewSet)
router.register(r'checkins', views.CheckInViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
