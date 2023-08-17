from django.shortcuts import render,redirect
from .models import Task
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import login
# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model=Task 
    context_object_name="tasks"

    def get_context_data(self,**kwargs): 
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()

        search_res=self.request.GET.get('search-area')
        if search_res: 
            context['tasks']=context['tasks'].filter(title__startswith=search_res)
        context['search_res']=search_res
        return context
   

class TaskDetail(LoginRequiredMixin,DetailView): 
    model=Task 
    context_object_name="tasks"

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task 
    fields=['title','desc','complete']
    success_url=reverse_lazy('task')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView): 
    model=Task 
    fields=['title','desc','complete']
    success_url=reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView): 
    model=Task 
    success_url=reverse_lazy('task')

class CustomLogin(LoginView): 
    fields='__all__'
    template_name='to_do/login.html'
    #redirect_authenticated_user=True

    def get_success_url(self):
     return reverse_lazy('task')

class RegisterPage(FormView): 
    template_name="to_do/register.html"
    form_class=UserCreationForm 
    redirect_authenticated_user=True 
    success_url=reverse_lazy('task')

    def form_valid(self,form): 
        user=form.save()
        if user is not None: 
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self,*args,**kwargs): 
        user=self.request.user 
        if user.is_authenticated: 
            return redirect('task')
        return super(RegisterPage,self).get(*args,**kwargs)

