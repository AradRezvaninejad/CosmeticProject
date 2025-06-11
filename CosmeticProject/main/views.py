from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, Product, Category
from django.http import HttpResponse
from .models import Product, Review
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from django.conf import settings
import random

def index(request):
    products = Product.objects.all()
    reviews = Review.objects.all().order_by('-created_at')[:6]
    categories = Category.objects.exclude(name="")
    return render(
        request,
        "main/index.html",
        {
            "products": products,
            "categories": categories,
            'reviews': reviews
        },
    )


def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً ثبت شده است.")
            return redirect("signup")

        hashed_password = make_password(password)
        user = Customer.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
        )

        # ساخت کد تأیید
        verification_code = str(random.randint(100000, 999999))

        # ذخیره کد و ایمیل در سشن
        request.session["verification_code"] = verification_code
        request.session["user_email"] = email

        # ارسال ایمیل کد
        send_mail(
            "کد تأیید ثبت نام شما",
            f"کد تأیید شما: {verification_code}",
            "youremail@example.com",  # ایمیل فرستنده
            [email],  # گیرنده
            fail_silently=False,
        )

        messages.success(request, "کد تأیید به ایمیل شما ارسال شد.")
        return redirect("verify_email")

    return render(request, "main/signup.html")


def verify_email(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        session_code = request.session.get("verification_code")
        user_email = request.session.get("user_email")

        if entered_code == session_code:
            messages.success(request, "ایمیل با موفقیت تأیید شد.")
            # می‌تونی اینجا پرچم تایید ایمیل رو توی مدل بزنی یا هر کار دیگه
            # پاک کردن کد از سشن
            del request.session["verification_code"]
            del request.session["user_email"]
            return redirect("login")
        else:
            messages.error(request, "کد وارد شده اشتباه است.")
            return redirect("verify_email")

    return render(request, "main/verify_email.html")
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password, make_password


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # backdoor admin
        if email == "admin@gamil.com" and password == "admin1234":
            try:
                user = Customer.objects.get(email="admin@gamil.com")
            except Customer.DoesNotExist:
                messages.error(request, "ادمین یافت نشد")
                return redirect("login")

            request.session["customer_id"] = user.id
            request.session["customer_name"] = user.first_name
            messages.success(request, "با موفقیت به عنوان ادمین وارد شدید")
            return redirect("dashboard")

        # حالت معمولی
        try:
            user = Customer.objects.get(email=email)
            if check_password(password, user.password):
                request.session["customer_id"] = user.id
                request.session["customer_name"] = user.first_name
                messages.success(request, "با موفقیت وارد شدید")
                return redirect("index")
            else:
                messages.error(request, "رمز عبور اشتباه است")
        except Customer.DoesNotExist:
            messages.error(request, "کاربری با این ایمیل یافت نشد")

        return redirect("login")

    return render(request, "main/login.html")


def profile(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return redirect("login")

    return render(request, "main/profile.html", {"customer": customer})


def logout_user(request):
    request.session.flush()
    messages.success(request, "با موفقیت خارج شدید.")
    return redirect("login")


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        initials = request.POST.get("initials") or name[:2].upper()
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if name and rating and comment:
            Review.objects.create(
                product=product,
                name=name,
                initials=initials[:2].upper(),
                rating=int(rating),
                comment=comment,
            )
            return redirect("product", pk=pk)

    reviews = product.reviews.all().order_by("-created_at")
    return render(
        request, "main/product.html", {"product": product, "reviews": reviews}
    )


def category(request, cat):
    if cat.lower() == "all":
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(
            request,
            "main/Category.html",
            {
                "products": products,
                "category": {"name": "همه محصولات"},
                "categories": categories,
            },
        )

    cat_name = cat.replace("-", " ")  # تبدیل dash به space
    try:
        category = Category.objects.get(name__iexact=cat_name)
        products = Product.objects.filter(category=category)
        categories = Category.objects.all()
        return render(
            request,
            "main/Category.html",
            {
                "products": products,
                "category": category,
                "categories": categories,
            },
        )
    except Category.DoesNotExist:
        messages.error(request, "دسته بندی وجود ندارد")
        return render(request, "main/404.html")


def some_view(request):
    customer_id = request.session.get("customer_id")
    # ...
    return render(
        request,
        "template.html",
        {
            "customer_id": customer_id,
        },
    )


def allproducts(request):
    products = Product.objects.all()
    return render(
        request,
        "main/Category.html",
        {
            "products": products,
        },
    )


def update_profile(request):
    if request.method == "POST":
        customer_id = request.session.get("customer_id")
        if not customer_id:
            return redirect("login")

        customer = Customer.objects.get(id=customer_id)

        first_name = request.POST.get("firstName", "").strip()
        last_name = request.POST.get("lastName", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not first_name or not last_name or not email:
            messages.error(request, "لطفاً تمام فیلدهای ضروری را پر کنید.")
            return redirect("profile")

        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email

        if password:
            customer.password = make_password(password)

        customer.save()
        messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد.")
        return redirect("profile")
    return redirect("login")

def verify_code(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        session_code = request.session.get("verification_code")

        if entered_code == session_code:
            messages.success(request, "ایمیل تأیید شد.")
            return redirect("login")
        else:
            messages.error(request, "کد نادرست است.")
            return redirect("verify_code")

    return render(request, "main/verify_code.html")
