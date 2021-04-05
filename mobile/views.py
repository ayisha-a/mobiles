from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def registration(request):
    context = {}
    form = UserCreationForm()
    context["form"] = form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    return render(request, "registration.html", context)

def signin(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pwd = request.POST.get("password")
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"message": "invalid password"})
    return render(request, "login.html")

def signout(request):
    logout(request)
    return redirect("signin")

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # all_products = Product.objects.all().order_by("-id")
        # paginator = Paginator(all_products, 8)
        # page_number = self.request.GET.get('page')
        # print(page_number)
        # product_list = paginator.get_page(page_number)
        context['product_list'] = Product.objects.all()
        return context



class MobileView(TemplateView):

    template_name = "view.html"
    context={}
    def get(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        mobile=Product.objects.get(id=id)
        self.context["mobile"]=mobile
        return render(request, self.template_name, self.context)



class Addtocart (TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        mobile_id = self.kwargs['pk']
        # get product
        mobile = Product.objects.get(id=mobile_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=mobile)
            #
            # # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += mobile.price
                cartproduct.save()
                cart_obj.total += mobile.price
                cart_obj.save()
             # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=mobile, rate=mobile.price, quantity=1, subtotal=mobile.price)
                cart_obj.total += mobile.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=mobile, rate=mobile.price, quantity=1, subtotal=mobile.price)
            cart_obj.total += mobile.price
            cart_obj.save()

        return context

class CartView(TemplateView):
    template_name = "cartview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCart(TemplateView):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("viewcart")



class EmptyCart(TemplateView):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("viewcart")

class PlaceOrderView(CreateView):
    template_name = 'placeorder.html'
    form_class=CheckOutForm
    success_url = reverse_lazy("home")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            order = form.save()

        else:
            return redirect("home")
        return super().form_valid(form)

