from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, ScheduleViewSet, BlogPostViewSet, CheckInViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'blogposts', BlogPostViewSet)
router.register(r'checkins', CheckInViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
