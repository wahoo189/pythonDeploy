# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

def index(request):
    if 'total_price' not in request.session:
        request.session['total_price'] = 0.0
        request.session['total_items'] = 0

    items = [
        {'name': 'Dojo T-Shirt', 'price': 10.0},
        {'name': 'Dojo Hoodie', 'price': 20.0},
        {'name': 'Dojo Cup', 'price': 30.0},
        {'name': 'Algorithm Book', 'price': 40.0},
    ]

    quantity = range(1, 10)

    context = {
        'items': items,
        'quantity_range': quantity
    }
    return render(request, 'amadon/index.html', context)

def buy_item(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        price = float(request.POST['price'])
        request.session['total_charge'] = quantity * price
        request.session['total_price'] += quantity * price
        request.session['total_items'] += quantity
        # request.session.modified = True
        return redirect('/amadon/checkout')

    return redirect('/amadon')

def checkout(request):
    return render(request, 'amadon/checkout.html')