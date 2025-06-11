from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import uuid
from django.core.files.base import ContentFile
import base64
from datetime import datetime
import json
from api import models
from rest_framework import viewsets
import requests
import jdatetime
from django.core.files.base import ContentFile


def dashboard_index(request):
    return render(request, "dashboard_admin/dashboard.html")


def order_detail(request, id):
    return render(request, "dashboard_admin/order-detail.html")


def transactions(request):
    return render(request, "dashboard_admin/transactions-1.html")


def order_list(request):
    return render(request, "dashboard_admin/order-list.html")


def product_list(request):
    return render(request, "dashboard_admin/product-list.html")


def blog_list(request):
    headers = {"Content-Type": "application/json", "Vary": "Accept"}
    response = requests.get("http://localhost:8000/api/Blog", headers=headers).json()
    print(response)
    for i in range(len(response)):
        print(i)
        response[i]["created"] = miladi_to_shamsi_matn(response[i]["created"])

    return render(request, "dashboard_admin/blog_list.html", {"blogz": response})


def miladi_to_shamsi_matn(miladi_date):
    year, month, day = map(int, miladi_date.split("-"))
    shamsi_date = jdatetime.date.fromgregorian(year=year, month=month, day=day)

    months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]

    result = f"{shamsi_date.year}/{shamsi_date.month}/{shamsi_date.day}"
    print(result)
    return result


def add_blog(request):
    print("jerivneo")
    return render(request, "dashboard_admin/add_blog.html")

    # if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
    #     try:
    #         data = json.loads(request.body)
    #     except:
    #         return JsonResponse({"ok":False,"matn": "invalid data"})

    #     if data["work"]=="add_blog":
    #         print(data)
    #         return JsonResponse({"ok":True,"matn":"sajiodhvoisdhfowihvow"})
    # else:
    #     return render(request,'dashboard/add_blog.html')


def sub_categories(request):
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"ok": False, "matn": "invalid data"})

        if data["work"] == "add_cat":
            print("salam")
            categoriz = models.Sub_category.objects.all()
            new = True
            for i in categoriz:
                if data["name"] == i.name:
                    new = False
            if not new:
                return JsonResponse(
                    {"ok": False, "matn": "کتگوری با این اسم از قبل وجود دارد"}
                )

            models.Sub_category(
                name=data["name"], description=data["description"], slug=data["slug"]
            ).save()
            return JsonResponse(
                {"ok": True, "matn": "کتگوری مورد نظر با موفقیت اضافه شد"}
            )

    else:
        return render(request, "dashboard_admin/sub_category.html")


def categories(request):
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"ok": False, "matn": "invalid data"})

        if data["work"] == "add_cat":
            print("salam")
            categoriz = models.Category.objects.all()
            new = True
            for i in categoriz:
                if data["name"] == i.name:
                    new = False
            if not new:
                return JsonResponse(
                    {"ok": False, "matn": "کتگوری با این اسم از قبل وجود دارد"}
                )

            models.Category(
                name=data["name"], description=data["description"], slug=data["slug"]
            ).save()
            return JsonResponse(
                {"ok": True, "matn": "کتگوری مورد نظر با موفقیت اضافه شد"}
            )

    else:
        return render(request, "dashboard_admin/product-categories.html")


def add_products(request):
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"ok": False, "matn": "invalid data"})

        if data["work"] == "add_product":
            categoriz = models.Product.objects.all()
            new = True
            for i in categoriz:
                if data["name"] == i.name:
                    new = False
            if not new:
                return JsonResponse(
                    {"ok": False, "matn": "کالایی با این نام وجود دارد"}
                )
            try:
                category = models.Category.objects.get(name=data["category"])
                sub_category = models.Sub_category.objects.get(
                    name=data["sub_category"]
                )
            except:
                return JsonResponse(
                    {
                        "ok": False,
                        "matn": "قبل از اضافه کردن کالا باید نوع و کتگوری اضافه کنید",
                    }
                )
            print(category.name)
            is_sale = True
            if data["is_sale"] == "normal_price":
                is_sale = False
            format, imgstr = data["picture"].split(";base64,")  # جدا کردن فرمت و داده
            ext = format.split("/")[-1]  # مثل png یا jpg
            image_file = ContentFile(
                base64.b64decode(imgstr), name=f'{data["name"]}.{ext}'
            )
            models.Product(
                name=data["name"],
                description=data["description"],
                price=data["normal_price"],
                is_sale=is_sale,
                sale_price=data["sale_price"],
                picture=image_file,
                quantity=data["quantity"],
                category=category,
                sub_category=sub_category,
            ).save()
            return JsonResponse(
                {"ok": True, "matn": "کالای مورد نظر با موفقیت اضافه شد"}
            )
        elif data["work"] == "get_categoriz":
            category = models.Category.objects.all()
            sub_category = models.Sub_category.objects.all()
            return JsonResponse(
                {
                    "ok": True,
                    "category": bool(len(category)),
                    "sub_category": bool(len(sub_category)),
                }
            )

    else:
        category = models.Category.objects.all()
        sub_category = models.Sub_category.objects.all()
        return render(
            request,
            "dashboard_admin/add-product-1.html",
            {"category": category, "sub_category": sub_category},
        )


def banners(request):
    return render(request, "dashboard_admin/banners.html")


def add_banner(request):
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):

        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"ok": False, "matn": "invalid data"})

        if data["work"] == "get_brands&categoris&products":
            products = bool(len(models.Product.objects.all()))
            categoriz = bool(len(models.Category.objects.all()))
            brands = bool(len(models.Sub_category.objects.all()))
            return JsonResponse(
                {"products": products, "categoriz": categoriz, "brands": brands}
            )

        elif data["work"] == "add_banner":
            bannerz = models.banners.objects.all()
            is_new = True
            for i in bannerz:
                if data["banner_title"] == i.title:
                    is_new = False
            if not is_new:
                return JsonResponse({"ok": False, "matn": "بنری با این نام وجود دارد"})

            models.banners(
                title=data["banner_title"],
                big_content=data["big_content"],
                small_content=data["small_content"],
                button_text=data["button_text"],
                related_value=data["related_value"],
                related=data["related"],
                picture=data["picture"],
            ).save()
            return JsonResponse({"ok": True, "matn": "banner ezafe shod"})

    else:
        products = models.Product.objects.all()
        categoriz = models.Category.objects.all()
        brands = models.Sub_category.objects.all()
        return render(
            request,
            "dashboard_admin/add_banner.html",
            {"products": products, "categoriz": categoriz, "brands": brands},
        )


def profile(request):
    return render(request, "dashboard_admin/profile-settings.html")


def user_list(request):
    return render(request, "dashboard_admin/sellers-list.html")


def user_info(request, username):
    return render(request, "dashboard_admin/sellers-profile.html")


def logout(request):
    pass
