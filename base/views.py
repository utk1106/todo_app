from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    # fields = '__all__'
    redirect_authenticated_user = True

    # def form_valid(self, form):
    #     # response = super().form_valid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'json' in self.request.headers.get('Accept', '').lower():
                return JsonResponse({
                "status": "success",
                "message": "Login worked",
                "redirect_to": self.get_success_url()
                # "accept_header": self.request.headers.get('Accept', 'Not sent')
            })
        return HttpResponseRedirect(self.get_success_url())
        
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

    def get_success_url(self):
        return reverse_lazy('tasks') #print username

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
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['now'] = timezone.now() #add current time for due soon highlighting
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context 
    #to show more task details

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due_date'] #added due_date for cron job
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due_date'] #added due_date for cron job
    success_url = reverse_lazy('tasks')

#reminded isn’t included in fields because it’s managed by the cron job, not the user

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


    #how to do it in falsk ---this part