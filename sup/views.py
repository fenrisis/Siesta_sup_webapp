from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import SUPBoard, RentalSlot
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'sup/home.html')

def login_view(request):
    if request.method == 'POST':
        # Process login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('sup:home')
    return render(request, 'sup/login.html')

def register_view(request):
    if request.method == 'POST':
        # Process registration form submission
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sup:home')
    else:
        form = CreateUserForm()
    return render(request, 'sup/register.html', {'form': form})

@login_required
def rent_sups(request):
    if request.method == 'POST':
        # Handle SUP rental form submission
        sup_board_id = request.POST.get('sup_board')
        rental_date = request.POST.get('rental_date')

        # Create a new RentalSlot object based on user selection
        sup_board = SUPBoard.objects.get(id=sup_board_id)
        rental_slot = RentalSlot.objects.create(user=request.user, sup_board=sup_board, rental_date=rental_date)
        rental_slot.save()

        return redirect('select_seats')  # Redirect to the next step of the rental process

    # Fetch all available SUP boards from the database
    sup_boards = SUPBoard.objects.all()

    return render(request, 'sup/rent.html', {'sup_boards': sup_boards})
