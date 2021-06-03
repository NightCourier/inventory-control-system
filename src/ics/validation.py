def get_booked_amount(request, product):
    return int(request.POST["amount_booked"]) if product.amount_booked != int(
        request.POST["amount_booked"]) else 0
