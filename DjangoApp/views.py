from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product
from decimal import Decimal

@csrf_exempt
def hello_world(request):
    return HttpResponse("Hello, World!")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        if not request.body:
            return HttpResponseBadRequest("Request body is empty.")

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")

        required_fields = ['name', 'price', 'available']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return HttpResponseBadRequest(f"Missing required fields: {', '.join(missing_fields)}")

        name = data.get('name')
        price = data.get('price')
        available = data.get('available')

        try:
            if price is not None:
                price = Decimal(str(price))
                if price <= 0:
                    return HttpResponseBadRequest("Price must be a positive number.")
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid value for price.")

        if not isinstance(available, bool):
            return HttpResponseBadRequest("Available field must be a boolean.")

        if Product.objects.filter(name=name).exists():
            return HttpResponseBadRequest("Product with this name already exists.")

        try:
            product = Product(name=name, price=price, available=available)
            product.full_clean()
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation error: {e}")

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201)

    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found.")

    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })

    return HttpResponseNotAllowed(['GET'])

