from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from .forms import MedicineForm, EquipmentForm
from .models import Medicine, Equipment


# Create your views here.


def login_register(request):
    if request.method == "POST":
        if 'login' in request.POST:  # Обробляємо авторизацію
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправляємо після входу
            else:
                messages.error(request, "Invalid username or password")
        elif 'register' in request.POST:  # Обробляємо реєстрацію
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    login(request, user)
                    return redirect('home')  # Перенаправляємо після реєстрації
            else:
                messages.error(request, "Passwords do not match")
    return render(request, 'inventory/login_register.html')


@login_required(login_url='login_register')
def profile(request):
    return render(request, 'inventory/profile.html')


def home_view(request):
    medicines = Medicine.objects.filter(user=request.user)
    # latest_changes = [

    # {'name': 'Анальгін', 'category': 'Препарат', 'updated_at': '2024-11-20', 'action': 'Додано'},
    # {'name': 'Парацетамол', 'category': 'Препарат', 'updated_at': '2024-11-22', 'action': 'Оновлено'},
    # {'name': 'Стерилізатор', 'category': 'Обладнання', 'updated_at': '2024-11-24', 'action': 'Оновлено'},
    # ]
    return render(request, 'inventory/home.html', {'medicines': medicines})


def pharmacy_info(request):
    return render(request, 'inventory/pharmacy_info.html', {})


def admin_or_pharmacy_employee(view_func):
    """Кастомний декоратор для перевірки доступу."""

    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or hasattr(request.user, 'pharmacy'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied")

    return wrapper


@login_required(login_url='login_register')
# @admin_or_pharmacy_employee
def manage_medicines(request):
    medicines = Medicine.objects.filter(user=request.user)
    return render(request, 'inventory/manage_medicines.html', {'medicines': medicines, 'action': manage_medicines})


# @admin_or_pharmacy_employee
# @login_required(login_url='login_register')
# def add_medicine(request):
#     if request.method == 'POST':
#         form = MedicineForm(request.POST)
#         if form.is_valid():
#             medicine = form.save(commit=False)
#             if request.user.pharmacy:
#                 medicine.pharmacy = request.user.pharmacy
#             else:
#                 return HttpResponseForbidden("You do not belong to any pharmacy.")
#             medicine.save()
#             return redirect('manage_medicines')
#     else:
#         form = MedicineForm()
#     return render(request, 'inventory/manage_medicines.html', {'form': form, 'action': 'add'})


@login_required(login_url='login_register')
# @admin_or_pharmacy_employee
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    medicine.delete()
    return redirect('manage_medicines')


@login_required(login_url='login_register')
# @admin_or_pharmacy_employee
def manage_equipment(request):
    equipment = Equipment.objects.filter(user=request.user)
    return render(request, 'inventory/manage_equipment.html', {'equipments': equipment})


# @login_required(login_url='login_register')
# # @admin_or_pharmacy_employee
# def edit_medicine(request, pk):
#     medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
#     if request.method == 'POST':
#         form = MedicineForm(request.POST, instance=medicine)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_medicines')
#     else:
#         form = MedicineForm(instance=medicine)
#     return render(request, 'inventory/manage_medicines.html', {'form': form, 'action': 'edit', 'medicine': medicine})


# @login_required(login_url='login_register')
# # @admin_or_pharmacy_employee
# def add_equipment(request):
#     if request.method == 'POST':
#         form = EquipmentForm(request.POST)
#         if form.is_valid():
#             equipment = form.save(commit=False)
#             equipment.pharmacy = request.user
#             equipment.save()
#             return redirect('manage_equipment')
#     else:
#         form = EquipmentForm()
#     return render(request, 'inventory/manage_equipment.html', {'form': form})


# @login_required(login_url='login_register')
# # @admin_or_pharmacy_employee
# def edit_equipment(request, pk):
#     equipment = get_object_or_404(Equipment, pk=pk, pharmacy=request.user)
#     if request.method == 'POST':
#         form = EquipmentForm(request.POST, instance=equipment)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_equipment')
#     else:
#         form = EquipmentForm(instance=equipment)
#     return render(request, 'inventory/manage_equipment.html', {'form': form})


@login_required(login_url='login_register')
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, user=request.user)
    equipment.delete()
    messages.success(request, "Обладнання успішно видалено.")
    return redirect('manage_equipment')


# def index(request):
#   return HttpResponse("Hello, world. You're at the polls index.")
