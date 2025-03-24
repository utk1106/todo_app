from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        print("Form valid, user:", form.cleaned_data['username'])
        response = super().form_valid(form)  # Handles authentication and login
        if 'json' in self.request.headers.get('Accept', '').lower():
            return JsonResponse({
                "status": "success",
                "message": "Login worked",
                "redirect_to": self.get_success_url()
            })
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"status": "error", "message": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            # token.blacklist()
            # Manually blacklist the token
            outstanding_token, _ = OutstandingToken.objects.get_or_create(
                jti=token["jti"],
                defaults={
                    "token": str(token),
                    "user_id": token["user_id"],
                    "exp": token["exp"],
                }
            )
            BlacklistedToken.objects.get_or_create(token=outstanding_token)
            
            return Response(
                {"status": "success", "message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
# @method_decorator(csrf_exempt, name='dispatch')
# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     # fields = '__all__'
#     redirect_authenticated_user = True

    # def form_valid(self, form):
    #     # response = super().form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     print("POST data:", request.POST)
    #     return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     print("Form valid, user:", form.cleaned_data['username'])
    #     # Manually authenticate and log in
    #     user = authenticate(
    #         request=self.request,
    #         username=form.cleaned_data['username'],
    #         password=form.cleaned_data['password']
    #     )
    #     if user is not None:
    #         login(self.request, user)
    #         print("User logged in:", user)
    #     else:
    #         print("Authentication failed")
    #     # Force JSON to test
    #     return JsonResponse({
    #         "status": "success",
    #         "message": "Login worked - manual",
    #         "redirect_to": self.get_success_url()
    #     })

    # def form_valid(self, form):
    #     print("Form valid, user:", form.cleaned_data['username'])
    #     # Manually authenticate and log in
    #     user = authenticate(
    #         request=self.request,
    #         username=form.cleaned_data['username'],
    #         password=form.cleaned_data['password']
    #     )
    #     if user is not None:
    #         login(self.request, user)
    #     # Return response based on Accept header
    #     if 'json' in self.request.headers.get('Accept', '').lower():
    #         return JsonResponse({
    #             "status": "success",
    #             "message": "Login worked",
    #             "redirect_to": self.get_success_url()
    #         })
    #     response = super().form_valid(form)
    #     if 'json' in self.request.headers.get('Accept', '').lower():
    #             return JsonResponse({
    #             "status": "success",
    #             "message": "Login worked",
    #             "redirect_to": self.get_success_url()
    #             # "accept_header": self.request.headers.get('Accept', 'Not sent')
    #         })
    #     return HttpResponseRedirect(self.get_success_url())
    
    # def get_success_url(self):
    #     return reverse_lazy('tasks') #print username
        
        # if self.request.headers.get('Accept') == 'application/json':
        #     # Postman or API client: return JSON
        #     return JsonResponse({
        #         "status": "success",
        #         "message": "login worked",
        #         # "redirect_to": self.get_success_url()
        #     })
        # # Browser: redirect as usual
        # return HttpResponseRedirect(self.get_success_url())  # Should redirect
        # return JsonResponse({
        #     "status":"success",
        #     "message":"login worked",
        #     # "redirect_to":self.get_success_url
        # })

    

#class CustomLoginView(LoginView):
    # template_name = 'base/login.html'
    # fields = '__all__'
    # redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy('tasks') #print username

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        user = form.save()
        # if user is not None:
        login(self.request, user)
        # 
        response = super().form_valid(form)  # Prepares the success response
        if 'json' in self.request.headers.get('Accept', '').lower():
            return JsonResponse({
                "status": "success",
                "message": "Registration and login worked",
                "redirect_to": self.success_url
            })
        return HttpResponseRedirect(self.success_url)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# class TaskList(LoginRequiredMixin,ListView):
#     model = Task
#     context_object_name = 'tasks'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = context['tasks'].filter(user=self.request.user)
#         context['count'] = context['tasks'].filter(complete=False).count()
#         context['now'] = timezone.now() #add current time for due soon highlighting
#         return context
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['now'] = timezone.now()
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'json' in self.request.headers.get('Accept', '').lower():
            tasks = list(context['tasks'].values('id', 'title', 'description', 'complete', 'due_date'))
            return JsonResponse({
                "status": "success",
                "tasks": tasks,
                "count": context['count'],
                "now": context['now'].isoformat()
            })
        return super().render_to_response(context, **response_kwargs)   

# class TaskDetail(LoginRequiredMixin,DetailView):
#     model = Task
#     context_object_name = 'task'
#     template_name = 'base/task.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context 
#     #to show more task details
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'json' in self.request.headers.get('Accept', '').lower():
            task = context['task']
            return JsonResponse({
                "status": "success",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "complete": task.complete,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                },
                "now": context['now'].isoformat()
            })
        return super().render_to_response(context, **response_kwargs)

# class TaskCreate(LoginRequiredMixin,CreateView):
#     model = Task
#     fields = ['title', 'description', 'complete', 'due_date'] #added due_date for cron job
#     success_url = reverse_lazy('tasks')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(TaskCreate, self).form_valid(form)
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due_date']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if 'json' in self.request.headers.get('Accept', '').lower():
            return JsonResponse({
                "status": "success",
                "message": "Task created",
                "task_id": self.object.id,
                "redirect_to": self.success_url
            })
        return HttpResponseRedirect(self.success_url)

# class TaskUpdate(LoginRequiredMixin,UpdateView):
#     model = Task
#     fields = ['title', 'description', 'complete', 'due_date'] #added due_date for cron job
#     success_url = reverse_lazy('tasks')
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due_date']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'json' in self.request.headers.get('Accept', '').lower():
            return JsonResponse({
                "status": "success",
                "message": "Task updated",
                "task_id": self.object.id,
                "redirect_to": self.success_url
            })
        return HttpResponseRedirect(self.success_url)

#reminded isn’t included in fields because it’s managed by the cron job, not the user

# class DeleteView(LoginRequiredMixin,DeleteView):
#     model = Task
#     context_object_name = 'task'
#     success_url = reverse_lazy('tasks')
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'json' in self.request.headers.get('Accept', '').lower():
            return JsonResponse({
                "status": "success",
                "message": "Task deleted",
                "redirect_to": self.success_url
            })
        return HttpResponseRedirect(self.success_url)


    #how to do it in falsk ---this part
# New API views using JWT
class TaskListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        count = tasks.filter(complete=False).count()
        tasks_data = list(tasks.values('id', 'title', 'description', 'complete', 'due_date'))
        return Response({
            "status": "success",
            "tasks": tasks_data,
            "count": count,
            "now": timezone.now().isoformat()
        })

class TaskDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
            return Response({
                "status": "success",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "complete": task.complete,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                },
                "now": timezone.now().isoformat()
            })
        except Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

class TaskCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = Task.objects.create(
            user=request.user,
            title=request.data.get('title'),
            description=request.data.get('description'),
            complete=request.data.get('complete', False),
            due_date=request.data.get('due_date')
        )
        return Response({
            "status": "success",
            "message": "Task created",
            "task_id": task.id
        }, status=status.HTTP_201_CREATED)

class TaskUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
            task.title = request.data.get('title', task.title)
            task.description = request.data.get('description', task.description)
            task.complete = request.data.get('complete', task.complete)
            task.due_date = request.data.get('due_date', task.due_date)
            task.save()
            return Response({
                "status": "success",
                "message": "Task updated",
                "task_id": task.id
            })
        except Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

class TaskDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
            task.delete()
            return Response({
                "status": "success",
                "message": "Task deleted"
            })
        except Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)