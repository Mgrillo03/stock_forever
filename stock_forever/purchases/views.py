from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Purchase
from stock.models import Product
from supplier.models import Supplier



def index(request):
    purchases_list = Purchase.objects.all()
    
    #purchase = Purchase.objects.first()
    
    return render(request, "purchases/index.html",{
        'purchases_list' : purchases_list
    })

def new_1(request, error_message = ''):
    suppliers_list = Supplier.objects.all()
     
    return render(request, "purchases/new.html",{
        'suppliers_list' : suppliers_list,
        'error_message': error_message,
        'cond' : True
    })

def new_2(request):
    suppliers_list = Supplier.objects.all()
    products_list = Product.objects.all()
    product_quantity = request.POST["quantity"]
    supplier_name = request.POST["supplier"]
    quantity_list = range(int(product_quantity))

    try:
        supplier = Supplier.objects.get(name=supplier_name)
    except (KeyError, supplier.DoesNotExist):
                error_message = 'El proveedor ingresano no existe en la base de datos'
                return new_1(request,error_message=error_message)
    else:

        return render(request, "purchases/new.html",{        
            'supplier_name' : supplier_name,
            'products_list' : products_list,
            'quantity_list' : quantity_list,
            'product_quantity' : product_quantity,
            'cond' : False        
        })

def add(request): 
    supplier_name = request.POST["supplier"]
    supplier = Supplier.objects.get(name=supplier_name)
    purchase = Purchase.objects.create(supplier=supplier)
    purchase.save()
    product_quantity = request.POST["product_quantity"]
    suma=0
    for i in range(int(product_quantity)):
        var = "product_"+str(i+1)   
        name = request.POST[var]
        product = Product.objects.get(name=name)
        
        var = "quantity_"+str(i+1)
        quantity = request.POST[var]
        product.stock += int(quantity)
        

        var = "price_"+str(i+1)
        price = request.POST[var]
        total = float(quantity) * float(price)
        suma+=total
        
        product.price = price 
        product.save()        

        purchase.product.add(product, through_defaults={'price':price,'quantity':quantity, 'total':total})

    purchase.total = suma
    purchase.save()
    products_list = purchase.purchase_product_set.all()

    payed = request.POST["payed"]
    substraction = suma - float(payed)
    supplier.debt -= substraction
    supplier.save()

    return render(request, "purchases/add.html",{
        'purchase':purchase,
        'products_list': products_list
    })
    
def detail_update_delete(request):    
    purchases_list = Purchase.objects.all()
   
    try:
        purchase = get_object_or_404(Purchase, pk=request.POST["choice"])
    except (KeyError, Purchase.DoesNotExist):
        return render(request, "purchases/index.html", {
            'purchases_list':purchases_list,
            "error_message": "No elegiste una compra"
        })
    else:

        if request.POST["action"] == "Editar":
            products_list = Product.objects.all()
            suppliers_list = Supplier.objects.all()
            purchase_product_set = purchase.purchase_product_set.all()

            return render(request, "purchases/update.html",{
                'purchase' : purchase,
                'products_list' : products_list,
                'suppliers_list' : suppliers_list,
                'purchase_product_set' : purchase_product_set

            })
        elif request.POST["action"] == "Eliminar":
            return render(request, "purchases/delete.html",{
                'purchase' : purchase
            })
        elif request.POST["action"] == "Detalle":
            
            purchase_product_set = purchase.purchase_product_set.all()
            return render(request, "purchases/detail.html",{
                'purchase': purchase,
                'purchase_product_set': purchase_product_set
            })

def detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    purchase_product_set = purchase.purchase_product_set.all()
    return render(request, "purchases/detail.html",{
        'purchase': purchase,
        'purchase_product_set': purchase_product_set
    })

def update_add(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    products_list = Product.objects.all()
    purchase_products = purchase.product.all()
    for i in products_list:
        if i not in purchase_products:
            purchase.product.add(i)
            break    
    purchase.save()
    suppliers_list = Supplier.objects.all()
    purchase_product_set = purchase.purchase_product_set.all()

    return render(request, "purchases/update.html",{
        'purchase' : purchase,
        'products_list' : products_list,
        'suppliers_list' : suppliers_list,
        'purchase_product_set' : purchase_product_set

    })

def update_del(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    suppliers_list = Supplier.objects.all()
    products_list = Product.objects.all()
    last_product = purchase.product.last()   
    purchase.product.remove(last_product)
    purchase.save()    
    purchase_product_set = purchase.purchase_product_set.all()

    return render(request, "purchases/update.html",{
        'purchase' : purchase,
        'products_list' : products_list,
        'suppliers_list' : suppliers_list,
        'purchase_product_set' : purchase_product_set

    })

def save_update(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    supplier_name = request.POST["supplier"]
    supplier = get_object_or_404(Supplier, name= supplier_name)
    purchase.supplier = supplier
    purchase.save()

    set_product = purchase.purchase_product_set.all()

    products_totals = purchase.product.count()
    products_list = []
    
    for i in range(products_totals):
        product_old = get_object_or_404(Product, pk = set_product[i].product.pk)
        product_old.stock -= set_product[i].quantity
        product_old.save()

        var = 'product_'+str(i+1)
        name = request.POST[var]
        product = get_object_or_404(Product, name = name)
        products_list.append(product)

        

    purchase.product.set(products_list)
    suma = 0

    for i in range(products_totals):
        var = 'product_'+str(i+1)
        name = request.POST[var]
        product = get_object_or_404(Product, name = name)
        purchase_detail = purchase.purchase_product_set.get(product=product)
        var = 'quantity_'+str(i+1)
        quantity = request.POST[var]
        purchase_detail.quantity = int(quantity)
        product.stock += int(quantity)
        product.save()

        var = 'price_'+str(i+1)
        price = request.POST[var]
        purchase_detail.price = float(price)
    
        total = float(price) * float(quantity)
        purchase_detail.total = total
        purchase_detail.save()

        suma += total   
    
    purchase.total = suma
    
    purchase.save()    
        
    return render(request, "purchases/update_saved.html",{
        'purchase' : purchase
    })

def confirm_detele(request, purchase_id):
    if request.POST["action"] == "Eliminar":
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        set_product = purchase.purchase_product_set.all()

        products_totals = purchase.product.count()
        
        for i in range(products_totals):
            product_old = get_object_or_404(Product, pk = set_product[i].product.pk)
            product_old.stock -= set_product[i].quantity
            product_old.save() 

        supplier = get_object_or_404(Supplier, pk=purchase.supplier.pk)
        supplier.debt += purchase.total
        supplier.save()

        purchase.delete()
        return render(request, "purchases/purchase_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("purchases:index"))
