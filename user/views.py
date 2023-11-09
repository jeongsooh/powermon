from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from user.models import User
from .forms import RegisterForm, LoginForm

# Create your views here.

def index(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      request.session['user'] = form.data.get('userid')
      return redirect('/energyinfo/dashboard')
  else:
    form = LoginForm()
  return render(request, 'index.html', {'form': form})

# def dashboard(request):
#   username  = request.session.get('user')

#   return render(request, 'dashboard.html', {'loginuser': username})

# class RegisterView(FormView):
#   template_name = 'register.html'
#   form_class = RegisterForm
#   success_url = '/'
#   def form_valid(self, form):
#     user = User(
#       userid=form.data.get('userid'),
#       password=make_password(form.data.get('password')),
#       level='user'
#     )
#     user.save()

#     return super().form_valid(form)

class UserCreateView(CreateView):
  model = User
  template_name = 'user_register.html'
  fields = ['userid', 'password']
  success_url = '/user/list'

  # def get_context_data(self, **kwargs):
  #   if 'user' in self.request.session:
  #     return redirect('/user/list')
  #   return redirect('/')

class UserDeleteView(DeleteView):
  model = User
  template_name='user_confirm_delete.html'
  success_url = '/user/list'

class UserUpdateView(UpdateView):
  model = User
  template_name='user_update.html'
  fields = [ 'userid', 'name', 'phone']
  success_url = '/user/list'

class UserList(ListView):
  model = User
  template_name='user.html'
  context_object_name = 'userList'
  paginate_by = 2
  queryset = User.objects.all()

  def get_context_data(self, **kwargs):
    context = super(UserList, self).get_context_data(**kwargs)
    user_id = self.request.session['user']
    query = self.request.GET.get("q", None)
    page = self.request.GET.get('page')
    category = self.request.GET.get('category')
    context['loginuser'] = user_id
    context['q'] = query
    context['category'] = category
    context['page']=page
    return context

  def get_queryset(self) :
    queryset = User.objects.all()
    query = self.request.GET.get("q", None)
    category = self.request.GET.get('category')
    if query:
      if category=='all':
        queryset = queryset.filter(
          Q(userid__icontains=query) |
          Q(name__icontains=query) |
          Q(phone__icontains=query)
        )
      elif category=='userid':
        queryset = queryset.filter(           
          Q(userid__icontains=query))
      elif category=='name':
        queryset = queryset.filter(           
          Q(name__icontains=query))
      elif category=='phone':
        queryset = queryset.filter(           
          Q(phone__icontains=query))
    return queryset

class UserDetail(DetailView):
  template_name='user_detail.html'
  queryset = User.objects.all()
  context_object_name = 'user'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.request.session['user']
    context['loginuser'] = user_id
    
    return context

class LoginView(FormView):
  template_name = 'login.html'
  form_class = LoginForm
  success_url = '/user/list'

  def form_valid(self, form):
    self.request.session['user'] = form.user_id

    return super().form_valid(form)


def logout(request):
  if 'user' in request.session:
    del(request.session['user'])

  return redirect('/')

def search(request):
  country = request.GET.get("country")
  if country:
      form = forms.SearchForm(request.GET)
      if form.is_valid():
          print(form.cleaned_data)
  else:
      form = forms.SearchForm()
  context = {"form": form}
  return render(request, "rooms/search.html", context)
