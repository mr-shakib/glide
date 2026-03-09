# from django.urls import path
# from .views import project_list, project_detail

# urlpatterns = [
#     path("projects", project_list),
#     path("projects/<int:project_id>/", project_detail)
# ]

from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()

router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = router.urls