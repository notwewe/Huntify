from django.shortcuts import render


# Create your views here.
def property_management(request):
    return render(request, 'boarding_house/dashboard/property-management.html')


def booking_management(request):
    return render(request, 'boarding_house/dashboard/booking-management.html')


def rent_a_room(request):
    return render(request, 'boarding_house/rent-a-room.html')


def boarding_house_detail(request):
    return render(request, 'boarding_house/boarding-house-detail.html')


def boarding_room_detail(request):
    return render(request, 'boarding_house/boarding-room-detail.html')


def get_property_table(request, property_type):
    if request.method == 'GET':
        if property_type == 'boarding_house':
            return render(request, 'boarding_house/dashboard/boarding-house-table.html')
        elif property_type == 'boarding_room':
            return render(request, 'boarding_house/dashboard/boarding-room-table.html')
