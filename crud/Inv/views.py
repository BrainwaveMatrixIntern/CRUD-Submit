from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from Inv.forms import RegForm, ItemAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Inv.models import Item, Category
from crud.settings import LOW_ITEM_QUANTITY
from django.contrib import messages


# Create your views here.
class Home(TemplateView):
    template_name = "Inv/home.html"

class RegView(View):

    def get(self, request):
        form = RegForm()
        return render(request, "Inv/signup.html", {"form" : form})

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password= form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("home")
        return render(request, "Inv/signup.html", {"form" : form})

class DashBoard(LoginRequiredMixin, View):
    def get(self, request):
        items = Item.objects.filter(user=self.request.user.id).order_by("-id")
        lowQuantity = Item.objects.filter(
            user = self.request.user.id, 
            quantity__lte = LOW_ITEM_QUANTITY
        )
        if lowQuantity.count() > 0:
            if lowQuantity.count() <= 10:
                messages.error(request, f"{lowQuantity.count()} item is low in quantity!")
            else:
                messages.error(request, f"{lowQuantity.count()} item is low in quantity!")
        lowQuantityIds = Item.objects.filter(
            user = self.request.user.id,
            quantity__lte = LOW_ITEM_QUANTITY
        ).values_list("id", flat=True)
        return render(request, "Inv/dashboard.html", {"items" : items, "lowQuantityId" : lowQuantityIds})

class ItemAdd(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemAddForm
    template_name = "Inv/addItem.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ItemEdit(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemAddForm
    template_name = "Inv/addItem.html"
    success_url = reverse_lazy("dashboard")

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "Inv/itemDelete.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "item"