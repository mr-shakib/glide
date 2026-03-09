# from django.http import JsonResponse
# from .models import Project
# from django.shortcuts import get_object_or_404

# def project_list(request):
#     projects = Project.objects.all()

#     data = [
#         {
#             "id": p.id,
#             "name": p.name,
#             "description": p.description,
#             "owner": p.owner.username,
#         }
#         for p in projects
#     ]

#     return JsonResponse(data, safe=False)

# def project_detail(request, project_id):
#     project = get_object_or_404(Project, id=project_id)

#     data = {
#         "id": project.id,
#         "name": project.name,
#         "description": project.description,
#         "owner": project.owner.username,
#     }

#     return JsonResponse(data)

from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
