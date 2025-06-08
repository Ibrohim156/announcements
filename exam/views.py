from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Property,UserProfile,Request,LeaveRequest
from .forms import PropertyForm,PropertyFilterForm,RequestForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required,user_passes_test


def home(request):
    form = PropertyFilterForm(request.GET)
    properties = Property.objects.all().order_by('-created_at')

    if form.is_valid():
        deal_type = form.cleaned_data.get('deal_type')
        rooms = form.cleaned_data.get('rooms')

        if deal_type:
            properties = properties.filter(deal_type=deal_type)
        if rooms:
            properties = properties.filter(rooms=rooms)

    return render(request, 'main.html', {'properties': properties, 'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, role=role)
            login(request, user)  
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'sign/reg.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Неверное имя пользователя или пароль"
            return render(request, 'sign/login.html', {'error': error_message})
    return render(request, 'sign/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')




def is_seller(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'seller'

@login_required
@user_passes_test(is_seller)
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'property/add_property.html', {'form': form})



@login_required
@user_passes_test(is_seller)
def my_properties(request):
    properties = Property.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'property/my_properties.html', {'properties': properties})

@login_required
@user_passes_test(is_seller)
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    property.delete()
    return redirect('my_properties')





@login_required
def leave_request(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        return render(request, 'property/request_sent.html', {'property': property})
    return render(request, 'property/leave_request.html', {'property': property})




@login_required
def leave_request(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.property = property_obj
            req.buyer = request.user
            req.save()
            return redirect('home')
    else:
        form = RequestForm()
    return render(request, 'property/leave_request.html', {'form': form, 'property': property_obj})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'property/property_detail.html', {'property': property})



@login_required
def my_requests(request):
    requests = LeaveRequest.objects.filter(buyer=request.user)
    return render(request, 'my_requests.html', {'requests': requests})
