from django.shortcuts import render, redirect, get_object_or_404,reverse
from . models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
# Create your views here.



def Index(request):
    category = Category.objects.all()
    profile = Profile.objects.all()
    dishes = Dish.objects.all()
    members = Team.objects.all().order_by('name')
    context = {
        'team_members': members,
        'profile':profile,
        'dishes': dishes,
        'category': category,
    }
    return render(request, 'index.html',context)


def contact_us(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        data.save()
        context['message']=f"Dear { name }, Thanks for Contact Us"
    return render(request, 'contact.html',context)


def About(request):
    return render(request, 'about.html')


def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            user = User.objects.filter(username=username)
            if user.exists():
                messages.info(request,"User name is Already Exists")
                return redirect('register')

            if password1 != password2:
                messages.info(request, "Confirm password doesn't match")
            else:
                my_user = User.objects.create_user(email,email,password1)
                my_user.first_name = username
                my_user.set_password(password1)
                my_user.save()
                profile = Profile(user=my_user,contact_number=contact)
                profile.save()
                messages.success(request, "Account created")
                return redirect('login')
        except:
            messages.error(request, "User Already Exist")
    return render(request,'register.html')


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email, password=passw)
        if check_user:
            login(request, check_user)
            if check_user.is_superuser or check_user.is_staff:
                return HttpResponseRedirect('/admin/')
            return HttpResponseRedirect('/dashboard')
        else:
            messages.error(request, "Email or password is Invalid")

    return render(request,'login.html')


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def Dashboard(request):
    login_user = get_object_or_404(User, id=request.user.id)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    if "update_profile" in request.POST:
        name = request.POST.get('name')

        contact = request.POST.get('contact_number')
        address = request.POST.get('address')
        profile.user.first_name = name
        profile.user.save()
        profile.contact_number = contact
        profile.address = address
        profile.save()

        if "profile_pic" in request.FILES:
            profile_pic = request.FILES['profile_pic']
            profile.profile_pic = profile_pic
            profile.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('dashboard')

    # Change password
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check:
            login_user.set_password(n_password)
            login_user.save()
            login(request,login_user)
            messages.success(request, "Password Updated Successfully")
        else:
            messages.error(request, "Current Password Incorrect")
    #myorders
    orders = Order.objects.filter(customer__user__id=request.user.id).order_by('-id')
    context = {
        'profile': profile,
        'orders': orders,
    }
    return render(request,'dashboard.html',context)


def team_members(request):
    members = Team.objects.all().order_by('name').order_by('-id')
    print(members)
    context = {
        'team_members': members,
    }
    return render(request,'team.html', context)


def all_dishes(request):
    context = {}
    dishes = Dish.objects.all()
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name

    context['dishes'] = dishes
    return render(request, 'all_dishes.html', context)


def single_dish(request, id):
    context ={}
    dish = get_object_or_404(Dish, id=id)
    if request.user.is_authenticated:
        cust = get_object_or_404(Profile, user__id=request.user.id)
        order = Order(customer=cust, item=dish)
        order.save()
        inv = f'INV0000-{order.id}'

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': dish.discounted_price,
            'item_name': dish.name,
            'user_id': request.user.id,
            'invoice': inv,
            'notify_url': 'http://{}{}'.format(settings.HOST, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(settings.HOST, reverse('payment_done')),
            'cancel_url': 'http://{}{}'.format(settings.HOST, reverse('payment_cancel')),
        }

        order.invoice_id = inv
        order.save()
        request.session['order_id'] = order.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({'dish': dish, 'form': form})
    return render(request,'dish.html',context)


def Booking(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guest = request.POST.get('guest')

        data = Booking_table(
            name=name,
            email=email,
            contact=contact,
            date=date,
            time=time,
            guests=guest,
        )
        data.save()
        messages.success(request, "Your Booking Has been Done")
    return render(request,'booking_table.html')


def payment_done(request):
    pid = request.GET.get('PayerID')
    order_id = request.session.get('order_id')
    order_obj = Order.objects.get(id=order_id)
    order_obj.status=True
    order_obj.payer_id = pid
    order_obj.save()
    return render(request,'payment_successful.html')


def payment_cancel(request):
    # remove comment to delete order
    # order_id = request.session.get('order_id')
    # Order.objects.get(id=order_id).delete()
    return render(request, 'payment_failed.html')


def Items(request,id):
    category = Category.objects.filter(id=id)
    category1 = get_object_or_404(Category, id=id)
    subcategories = Sub_category.objects.filter(category=category1)

    print(category)
    print(category1)
    print(subcategories)
    context = {
        'category': category,
        'category1': category1,
        'subcategories': subcategories,
    }
    return render(request,'items.html',context)


def Item_Details(request,id):
    sub_category = Sub_category.objects.filter(id=id)
    sub_category1 = get_object_or_404(Sub_category, id=id)
    dishes = Dish.objects.filter(Sub_category=sub_category1)


    context = {
        'sub_category': sub_category,
        'dishes': dishes,
        'sub_category1': sub_category1
    }
    return render(request,'item_detail.html',context)
