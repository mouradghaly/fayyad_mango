from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django import forms 
from django.db import models 
import random

# Create your views here
class model(models.Model):
    name = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    phonenumber = models.CharField(max_length=11)
    address = models.CharField()
    order_description = models.CharField(max_length=50)
    total = models.CharField(max_length=10)
    id = models.IntegerField(primary_key=True)
    order_status =  models.CharField(default="Created", max_length=30)

class products(models.Model):
    name = models.CharField(max_length=10)
    price = models.CharField(max_length=10)



@csrf_exempt
def order(request):
    if request.method == "POST":
        my_model = model.objects.all()
        name =request.POST.get('name')
        lastname = request.POST.get('lastname')
        phonenumber = request.POST.get('number')
        address = request.POST.get("address")
        order_description = request.POST.get("order_description")
        total = request.POST.get("total")
        id = random.randint(1, 2000)
        ##########################################ANTI JAVASCRIPT ABUSE############################################################
        ###########################################################################################################################
        order = model(name = name, lastname = lastname, phonenumber = phonenumber, address = address, order_description=order_description, total=total, id= id)
        order.save()
        return JsonResponse({"Status": "Order Created", "Id": id })
    else :
        return render(request, "fayyad_mango.html")


'''def authn(request):
    form = log_in_form(request.POST)
    if request.method == "POST":
        if form.is_valid():
            usr  = form.cleaned_data['usr']
            password = form.cleaned_data['password']
            request.session['usr'] = usr
            request.session['password'] = password
            if usr == "Mourad":
                return HttpResponseRedirect("https://127.0.0.1:8000/bruxies/admin/")
            else :
                return HttpResponseForbidden("We Know what you're trying to do ;)")
    else :
        return render(request, "authn.html", {"form": form} )'''
    

def admin(request):
    my_model = model.objects.all()
    return render(request, "admin.html")
    
@csrf_exempt
def track_order(request):
    if request.method == "POST":
        order = json.loads(request.body)
        order_id = order["order"]
        x = model.objects.get(id= order_id)
        print(x.order_status)
        return JsonResponse({"Status": x.order_status })
    
    else : 
        return render(request, "tracker.html")

def dashboard(request):
    if request.method == "GET":
        mymodel = model.objects.all()
        orders = []
        unfulfilled_orders = []
        for order in mymodel:
            if order.order_status != "Delivered":
                orders.append({"id": order.id, "name": order.name, "lastname": order.lastname, "phonenumber": order.phonenumber, "description": order.order_description, "status": order.order_status, "address": order.address, "total": order.total})
        return JsonResponse(orders, safe=False)
    
def dashboard_complete(request):
    if request.method == "GET":
        orders = []
        mymodel = model.objects.filter(order_status = "Delivered")
        for order in mymodel:
            orders.append({"id": order.id, "name": order.name, "lastname": order.lastname, "description": order.order_description,  "phonenumber": order.phonenumber, "address": order.address})

        return JsonResponse(orders, safe=False)

@csrf_exempt
def update_status(request):
    if request.method == "POST":
        message = json.loads(request.body)
        if message["order"][0] == "p":
            message["order"] = message["order"].replace("p", "")
            message = int(message["order"])
            print(message)
            order = model.objects.get(id=message)
            order.order_status = "Prepared"
            order.save()
            return JsonResponse({"Response": f' Order {message} Prepared'})
        
        if message["order"][0] == "d":
            message["order"] = message["order"].replace("d", "")
            message["order"] = int(message["order"])
            print(message)
            message = int(message["order"])
            order = model.objects.get(id=message)
            order.order_status = "Out for Delivery"
            order.save()
            return JsonResponse({"Response": "Out for Delivery"})
        
        if message["order"][0] == "a":
            message["order"] = message["order"].replace("a", "")
            message = int(message["order"])
            order = model.objects.get(id=message)
            order.order_status = "Delivered"
            order.save()
        return HttpResponse(message)
    
@csrf_exempt
def price(request):
    if request.method == "GET":
        model  = products.objects.all()
        prices = []
        for product in model:
            prices.append({"name": f'{product.name}', "price": f'{product.price}'})
        return JsonResponse(prices, safe=False)
    
    if request.method == "POST":
        print("Working")
        new_ewes_price =  request.POST.get("new_ewes_price")
        new_taymour_price = request.POST.get("new_taymour_price")
        new_fass_price = request.POST.get("new_fass_price")
        print(new_ewes_price, new_taymour_price, new_fass_price)
        updates = []
        if new_ewes_price != "":
            ewes  = products.objects.get(name="Ewes")
            ewes.price = new_ewes_price
            ewes.save()
            updates.append(f'Ewes price updated to {new_ewes_price}')
            return HttpResponse("OK")

        if new_taymour_price != "":
            taymour = products.objects.get(name="Taymour")
            taymour.price = new_taymour_price
            taymour.save()
            updates.append(f'Taymour price updated to {new_taymour_price}')

        if new_fass_price != "":
            fass = products.objects.get(name= "Fass")
            fass.price = new_fass_price
            fass.save()
            updates.append(f'Fass price updated to {new_fass_price}')
        
        return JsonResponse(updates, safe=False)
        
