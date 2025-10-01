import asyncio
import json
import types

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

# from rest_framework.permissions import IsAuthenticated

from bot.bot import TelegramBot
from tasktracker.models import Task, Category
from tasktracker.serializers import TaskSerializer, CategorySerializer
from users.models import User
from users.permissions import IsSuperUser, IsOwner


bot = TelegramBot()


@csrf_exempt
@require_POST
def webhook(request):
    """Обработчик вебхуков от Telegram"""
    try:
        update = json.loads(request.body)

        asyncio.run(bot.dp.feed_update(bot.bot, types.Update(**update)))
        return HttpResponse("OK")

    except json.JSONDecodeError as e:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        telegram_id = self.request.GET.get("telegram_id")
        if telegram_id:
            user = User.objects.get(telegram_id=telegram_id)
        else:
            user = self.request.user
        serializer.save(owner=user)


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        telegram_id = self.request.GET.get("telegram_id")
        if telegram_id:
            user = User.objects.get(telegram_id=telegram_id)
            return Task.objects.filter(owner=user)
        else:
            if self.request.user.is_superuser:
                return Task.objects.all()
            queryset = Task.objects.filter(owner=self.request.user)
            return queryset


class TaskDetailAPIView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny, IsOwner)

    def get_object(self):
        task = Task.objects.get(pk=self.kwargs['pk'])
        return task


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)


class TaskDeleteAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)


class CategoryAPIViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)