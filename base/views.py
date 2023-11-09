from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from .models import Item

# Create your views here.


class ItemList(ListView):
  model = Item
  template_name='item.html'
  context_object_name = 'itemList'
  paginate_by = 5
  queryset = Item.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ItemList, self).get_context_data(**kwargs)
    item_id = self.request.session['user']
    context['loginuser'] = item_id
    return context