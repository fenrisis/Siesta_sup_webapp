from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import SUPBoard, RentalSlot, Order
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from datetime import time


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

def logout_view(request):
    logout(request)
    return redirect('sup:home')

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
        rental_date = request.POST.get('date')

        # Create a new RentalSlot object based on user selection
        sup_board = SUPBoard.objects.get(id=sup_board_id)

        # Set default start_time and end_time (you can modify this based on your requirements)
        start_time = time(9, 0)  # Default start time is 9:00 AM
        end_time = time(10, 0)   # Default end time is 10:00 AM

        rental_slot = RentalSlot.objects.create(
            sup_board=sup_board,
            date=rental_date,
            start_time=start_time,
            end_time=end_time
        )

        rental_slot.save()

        # Store the created rental slot ID in the session so we can access it later
        request.session['rental_slot_id'] = rental_slot.id

        return redirect('sup:select_seats')  # Redirect to the next step of the rental process

    # Fetch all available SUP boards from the database
    sup_boards = SUPBoard.objects.all()

    return render(request, 'sup/rent.html', {'sup_boards': sup_boards}) 

@login_required
def select_seats(request):
    if request.method == 'POST':
        # Get the selected seats from the submitted form data
        selected_seats = int(request.POST.get('selected_seats'))
        rental_slot_id = request.session.get('rental_slot_id')

        # Update the RentalSlot object with the selected seats
        rental_slot = RentalSlot.objects.get(id=rental_slot_id)
        rental_slot.selected_seats = selected_seats
        rental_slot.save()

        # Clear the stored rental_slot_id from the session
        del request.session['rental_slot_id']

        # Calculate the total amount for the order
        total_amount = selected_seats * rental_slot.sup_board.price_per_seat

        # Create a new Order object
        user = request.user
        order = Order.objects.create(
            rental_slot=rental_slot,
            user=user,
            total_amount=total_amount
        )

        return redirect('sup:order_detail', id=order.id)  # Redirect to the order detail page

    return render(request, 'sup/select_seats.html')

@login_required
def order_detail(request, id=None):
    order = get_object_or_404(Order, id=id)
    context = {
        'order': order,
    }
    return render(request, 'sup/order_detail.html', context)