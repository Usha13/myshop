from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderTrack
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum

MERCHANT_KEY = 'OOWK%G2!iGU6%Imq'


# Create your views here.
def index(request):
    catprod = Product.objects.values('pcategory', 'id')
    cats = {item['pcategory'] for item in catprod}
    allprod = []
    for ct in cats:
        prod = Product.objects.filter(pcategory=ct)
        n = len(prod)
        nslide = n // 4 + ceil((n / 4) - (n // 4))
        allprod.append([prod, range(1, nslide), nslide])
        param = {'allprod': allprod}
    return render(request, "shop/index.html", param)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        cnt = Contact(name=name, phone=phone, email=email, desc=desc)
        cnt.save()
        submit = True
        return render(request, "shop/contact.html", {'submit': submit})
    return render(request, "shop/contact.html")


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        email = request.POST.get('email')

        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = OrderTrack.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.prod_desc, 'time': item.timestamp})
                    response = json.dumps({'status': 'Success', 'updates': updates, 'itemjson': order[0].item_json},
                                          default=str)
                return HttpResponse(response)
            else:
                resp = json.dumps({'status': 'No item'})
                return HttpResponse(resp)

        except Exception as e:
            resp = json.dumps({'status': 'No item'})
            return HttpResponse(resp)

    return render(request, "shop/tracker.html")


def product(request, myid):
    product = Product.objects.filter(id=myid)
    param = {'product': product[0]}
    print(product)
    return render(request, "shop/product.html", param)


def checkout(request):
    if request.method == "POST":
        itemjson = request.POST.get('itemjson')
        tprice = request.POST.get('tprice')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address1') + " " + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        order = Order(item_json=itemjson, tprice=tprice, name=name, phone=phone, email=email, address=address,
                      city=city, state=state,
                      zip=zip_code)
        order.save()
        prodtrack = OrderTrack(order_id=order.order_id, prod_desc="The order has been Placed")
        prodtrack.save()
        thank = True
        id = order.order_id
        # param = {'thank': thank, 'id': id}
        # return render(request, "shop/checkout.html", param)
        data_dict = {
            'MID': 'vFAPHA73733710090009',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(tprice),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlepayment/',
        }
        data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request, "shop/paytm.html", {'param_dict': data_dict})

    return render(request, "shop/checkout.html")


def checkout2(request, myid):
    if request.method == "POST":
        itemjson = request.POST.get('itemjson')
        tprice = request.POST.get('tprice')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address1') + " " + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        order = Order(item_json=itemjson, tprice=tprice, name=name, phone=phone, email=email, address=address,
                      city=city, state=state,
                      zip=zip_code)
        order.save()
        prodtrack = OrderTrack(order_id=order.order_id, prod_desc="The order has been Placed")
        prodtrack.save()
        thank = True
        id = order.order_id
        # param = {'thank': thank, 'id': id}
        # return render(request, "shop/checkout2.html", param)
        data_dict = {
            'MID': 'vFAPHA73733710090009',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(tprice),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlepayment2/',
        }
        data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request, "shop/paytm.html", {'param_dict': data_dict})
    else:
        prod = Product.objects.filter(id=myid)
        param = {'prod': prod[0]}
        print(prod)
        return render(request, "shop/checkout2.html", param)


def cart(request):
    return HttpResponse("Shop cart")


def payment(request):
    return HttpResponse("Shop cart")


@csrf_exempt
def handlepayment(request):
    form = request.POST
    respons_dict = {}
    for i in form.keys():
        respons_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(respons_dict, MERCHANT_KEY, checksum)

    if verify:
        if respons_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order unsuccessful because" + respons_dict['RESPMSG'])
    else:
        print("order unsuccessful because" + respons_dict['RESPMSG'])

    return render(request, 'shop/paymentstatus.html', {'response': respons_dict})


@csrf_exempt
def handlepayment2(request):
    form = request.POST
    respons_dict = {}
    for i in form.keys():
        respons_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(respons_dict, MERCHANT_KEY, checksum)

    if verify:
        if respons_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order unsuccessful because" + respons_dict['RESPMSG'])
    else:
        print("order unsuccessful because" + respons_dict['RESPMSG'])

    return render(request, 'shop/paymentstatus2.html', {'response': respons_dict})


def searchMatch(query, item):
    if query in item.pdesc.lower() or query in item.pname.lower() or query in item.pcategory.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    catprod = Product.objects.values('pcategory', 'id')
    cats = {item['pcategory'] for item in catprod}
    allprod = []
    for ct in cats:
        prodtemp = Product.objects.filter(pcategory=ct)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslide = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprod.append([prod, range(1, nslide), nslide])
    param = {'allprod': allprod, 'msg': ""}
    if len(allprod) == 0:
        param = {'msg': "Please make sure to enter relevant search query"}
    return render(request, "shop/search.html", param)
