
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login as dj_login, logout
import logging
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Book
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    if request.session.has_key('is_logged'):
     # return redirect('/index')
        books = Book.objects.all()
        return HttpResponse("you are logged in")
    
    #return render(request, '404.html')
    return render(request, 'index.html')



def handleSignupStep1(request):
    # Retrieve data from the session, if available, to prepopulate the form
    uname = request.session.get('uname', '')
    pass1 = request.session.get('pass1', '')

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home or login on cancel

        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        errors = []

        if User.objects.filter(username=uname).exists():
            errors.append("Username already taken, try something else.")
        if len(uname) > 15:
            errors.append("Username must be max 15 characters.")
        if pass1 != pass2:
            errors.append("Passwords do not match.")
        if len(pass1) < 8:
            errors.append("Password should be at least 8 characters long.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register_step1.html', {'uname': uname, 'pass1': pass1})

        # Store data in session
        request.session['uname'] = uname
        request.session['pass1'] = pass1
        return redirect('register_step2')

    return render(request, 'register_step1.html', {'uname': uname, 'pass1': pass1})
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home or login on cancel

        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        errors = []

        if User.objects.filter(username=uname).exists():
            errors.append("Username already taken, try something else.")
        if len(uname) > 15:
            errors.append("Username must be max 15 characters.")
        if pass1 != pass2:
            errors.append("Passwords do not match.")
        if len(pass1) < 8:
            errors.append("Password should be at least 8 characters long.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register_step1')

        request.session['uname'] = uname
        request.session['pass1'] = pass1
        return redirect('register_step2')

    return render(request, 'register_step1.html')

def handleSignupStep2(request):
    # Retrieve data from the session, if available, to prepopulate the form
    fname = request.session.get('fname', '')
    lname = request.session.get('lname', '')
    email = request.session.get('email', '')

    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step1')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']

        # Store data in session
        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['email'] = email
        return redirect('register_step3')

    return render(request, 'register_step2.html', {'fname': fname, 'lname': lname, 'email': email})
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step1')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']

        request.session['fname'] = fname
        request.session['lname'] = lname
        request.session['email'] = email
        return redirect('register_step3')

    return render(request, 'register_step2.html')

def handleSignupStep3(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step2')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        profession = request.POST['profession']
        savings = request.POST['savings']
        income = request.POST['income']

        # Save the data in the session
        request.session['profession'] = profession
        request.session['savings'] = savings
        request.session['income'] = income

        # Retrieve other necessary session data
        uname = request.session['uname']
        pass1 = request.session['pass1']
        fname = request.session['fname']
        lname = request.session['lname']
        email = request.session['email']

        # Create the User and UserProfile object
        user = User.objects.create_user(username=uname, password=pass1, email=email, first_name=fname, last_name=lname)
        profile = UserProfile(user=user, profession=profession, Savings=savings, income=income)
        profile.save()

        # Log in the user
        dj_login(request, user)
        request.session['is_logged'] = True
        return redirect('register_step4')

    # Pass profession choices to the template
    profession_choices = UserProfile._meta.get_field('profession').choices
    return render(request, 'register_step3.html', {'profession_choices': profession_choices})

    # Retrieve data from the session, if available, to prepopulate the form
    profession = request.session.get('profession', '')
    savings = request.session.get('savings', '')
    income = request.session.get('income', '')

    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step2')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        profession = request.POST['profession']
        savings = request.POST['savings']
        income = request.POST['income']

        # Retrieve session data for user creation
        uname = request.session['uname']
        pass1 = request.session['pass1']
        fname = request.session['fname']
        lname = request.session['lname']
        email = request.session['email']

        # Store profession-related data in session
        request.session['profession'] = profession
        request.session['savings'] = savings
        request.session['income'] = income

        # Create User and UserProfile
        user = User.objects.create_user(username=uname, password=pass1, email=email, first_name=fname, last_name=lname)
        profile = UserProfile(user=user, profession=profession, Savings=savings, income=income)
        profile.save()

        dj_login(request, user)
        request.session['is_logged'] = True
        return redirect('register_step4')

    return render(request, 'register_step3.html', {'profession': profession, 'savings': savings, 'income': income})

    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step2')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel
        
        profession = request.POST['profession']
        savings = request.POST['Savings']
        income = request.POST['income']

        uname = request.session['uname']
        pass1 = request.session['pass1']
        fname = request.session['fname']
        lname = request.session['lname']
        email = request.session['email']

        user = User.objects.create_user(username=uname, password=pass1, email=email, first_name=fname, last_name=lname)
        profile = UserProfile(user=user, profession=profession, Savings=savings, income=income)
        profile.save()

        dj_login(request, user)
        request.session['is_logged'] = True
        return redirect('register_step4')

    return render(request, 'register_step3.html')

def register_success(request):
    # Retrieve the first name from the session
    fname = request.session.get('fname', '')

    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step3')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        # Final submission logic here
        messages.success(request, "Registration complete!")
        return redirect('home')  # Redirect to home or another page after success

    return render(request, 'register_step4.html', {'fname': fname})
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('register_step3')
        if 'cancel' in request.POST:
            return redirect('home')  # Redirect to home on cancel

        # Final submission logic here
        messages.success(request, "Registration complete!")
        return redirect('home')  # Redirect to home or another page after success

    return render(request, 'register_step4.html')

def handlelogin(request):
    messages.error(request, '')
    if request.method == 'POST':
        loginuname = request.POST.get("loginuname")
        loginpassword1 = request.POST.get("loginpassword1")
        
        user = authenticate(username=loginuname, password=loginpassword1)
        
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            request.session["user_id"] = user.id
            
            messages.success(request, "Successfully logged in")
            template = loader.get_template('index.html')
            return HttpResponse(template.render())
        
        else:
            messages.error(request, "Username or password maybe invalid, Please try again")
            return render(request, 'login.html')
    return render(request, 'login.html', {'messages': messages.get_messages(request)})

# Step 1: Enter username
def reset_password_step1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            # If valid, proceed to step 2
            return redirect('reset_password_step2')
        except User.DoesNotExist:
            # If username is invalid, show an error
            messages.error(request, 'Username does not exist. Please try again.')
    return render(request, 'reset_password_step1.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_username'] = username
            return redirect('reset_password_step2')
        except User.DoesNotExist:
            messages.error(request, 'Username not found.')
    
    return render(request, 'reset_password_step1.html')

# views.py
# Step 2: Enter email and create a new password
def reset_password_step2(request):
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = User.objects.filter(email=email).first()
        
        # Check if email exists and belongs to the user
        if user is None:
            messages.error(request, 'Email does not match any account.')
            return redirect('reset_password_step2')
        
        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('reset_password_step2')

        # If everything is valid, save the new password
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password reset successfully.')
        return redirect('reset_password_step3')
        
    return render(request, 'reset_password_step2.html')

# views.py
def reset_password_step3(request):
    return render(request, 'reset_password_step3.html')


logger = logging.getLogger(__name__)


def book_list(request):
    sort_by = request.GET.get('sort_by', 'title')
    search_query = request.GET.get('search', '')

    # Start by querying all books
    books = Book.objects.all()

    # Apply search filter if search_query is provided
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(subtitle__icontains=search_query) | 
            Q(authors__icontains=search_query)
        )
    
    # Sort the filtered books
    books = books.order_by(sort_by)

    # Limit the result to only the first 50 books
    books = books[:50]

    # Get unique categories
    unique_categories = Book.objects.exclude(category__isnull=True).exclude(category='nan').values_list('category', flat=True).distinct()

    return render(request, 'books.html', {'books': books, 'unique_categories': unique_categories})


def edit_book(request, book_id):
    # Retrieve the specific book by its ID
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Bind the submitted data to the form
        form = BookForm(request.POST, instance=book)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the changes to the book
            form.save()
            
            # Redirect or return success response after saving
            return redirect('book_list')  # Redirect to the book list view or a success page
        else:
            return HttpResponse("Invalid form data", status=400)
    else:
        # If not POST, display the form with the existing book data
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    if request.method == 'DELETE':
        book = Book.objects.get(pk=book_id)
        book.delete()
        return JsonResponse({'success': True})
    
def user_profile(request):
    return render(request, 'profile.html')
@csrf_exempt  # 
def add_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Create a new book instance
        book = Book(
            isbn=data['isbn'],
            title=data['title'],
            subtitle=data['subtitle'],
            authors=data['authors'],
            publisher=data['publisher'],
            publish_date=data['publish_date'],
            category=data['category'],
            distribution_expense=data['distribution_expense'],
        )
        # Save the book to the database
        book.save()
        return JsonResponse({'success': True, 'message': 'Book added successfully!'})
    #return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    return render(request, 'addbook.html')



























"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Addmoney_info, UserProfile
import datetime


def register(request):
    # Your registration logic here
    return render(request, 'home/register.html')

def charts(request):
    # Your logic for the charts view here
    return render(request, 'home/charts.html')

def tables(request):
    # Your logic for the tables view here
    return render(request, 'home/tables.html')


def search(request):
    # Your logic for the search view here
    return render(request, 'home/search.html')


 # ABOVE ARE TROUBLESHOOTING CODES 


 
def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request, 'login.html')
    # return HttpResponse('This is home')




def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            # 'add_info': addmoney_info,
            'page_obj': page_obj
        }
        # if request.session.has_key('is_logged'):
        return render(request, 'home/index.html', context)
    return redirect('home')

def addmoney(request):
    return render(request, 'home/addmoney.html')

def profile(request):
    if request.session.has_key('is_logged'):
        return render(request, 'home/profile.html')
    return redirect('/home')

def profile_edit(request, id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        return render(request, 'home/profile_edit.html', {'add': add})
    return redirect("/home")

def profile_update(request, id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            user.userprofile.profession = request.POST["profession"]
            user.userprofile.save()
            user.save()
            return redirect("/profile")
    
    return redirect("/home")

def handleSignup(request):
    if request.method =='POST':
        # get the post parameters
        uname = request.POST["uname"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        profession = request.POST['profession']
        Savings = request.POST['Savings']
        income = request.POST['income']
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        profile = UserProfile(Savings=Savings, profession=profession, income=income)

        # check for errors in input
        if request.method == 'POST':
            try:
                user_exists = User.objects.get(username=request.POST['uname'])
                messages.error(request, "Username already taken, Try something else!!!")
                return redirect("/register")
            except User.DoesNotExist:
                if len(uname) > 15:
                    messages.error(request, "Username must be max 15 characters, Please try again")
                    return redirect("/register")
                if not uname.isalnum():
                    messages.error(request, "Username should only contain letters and numbers, Please try again")
                    return redirect("/register")
                if pass1 != pass2:
                    messages.error(request, "Password do not match, Please try again")
                    return redirect("/register")
                
                # create the user
                user = User.objects.create_user(uname, email, pass1)
                user.first_name = fname
                user.last_name = lname
                user.email = email

                # profile = UserProfile.objects.all()
                user.save()
                # p1=profile.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Your account has been successfully created")
                return redirect("/")
        else:
            return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def handlelogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginuname = request.POST.get("loginuname")
        loginpassword1 = request.POST.get("loginpassword1")
        
        # Authenticate the user
        user = authenticate(username=loginuname, password=loginpassword1)
        
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            request.session["user_id"] = user.id
            
            messages.success(request, "Successfully logged in")
            return redirect('/index')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect("/")
    
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    if 'is_logged' in request.session:
        del request.session['is_logged']
        del request.session["user_id"]
        
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('home')
    
    return HttpResponse('404 - Not Found')

def addmoney_submission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            addmoney_info1 = Addmoney_info.objects.filter(user=user1).order_by('-Date')
            
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            Category = request.POST["Category"]
            
            add = Addmoney_info(
                user=user1,
                add_money=add_money,
                quantity=quantity,
                Date=Date,
                Category=Category
            )
            add.save()
            
            paginator = Paginator(addmoney_info1, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'page_obj': page_obj
            }
            
            return render(request, 'home/index.html', context)
    
    return redirect('/index')

def addmoney_update(request, id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add = Addmoney_info.objects.get(id=id)
            add.add_money = request.POST["add_money"]
            add.quantity = request.POST["quantity"]
            add.Date = request.POST["Date"]
            add.Category = request.POST["Category"]
            add.save()
            return redirect("/index")
    
    return redirect("/home")

def expense_edit(request, id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        return render(request, 'home/expense_edit.html', {'addmoney_info': addmoney_info})
    
    return redirect("/home")

def expense_delete(request, id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    
    return redirect("/home")

def expense_month(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date - datetime.timedelta(days=30)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    
    addmoney = Addmoney_info.objects.filter(
        user=user1,
        Date__gte=one_month_ago,
        Date__lte=todays_date
    )
    
    finalrep = {}

    def get_Category(addmoney_info):
        # if addmoney_info.add_money == "Expense":
        return addmoney_info.Category
    
    Category_list = list(set(map(get_Category, addmoney)))
    
    def get_expense_category_amount(Category, add_money):
        quantity = 0
        filtered_by_category = addmoney.filter(
            Category=Category,
            add_money="Expense"
        )
        for item in filtered_by_category:
            quantity += item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stats(request):
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_month_ago = todays_date - datetime.timedelta(days=30)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        
        addmoney_info = Addmoney_info.objects.filter(
            user=user1,
            Date__gte=one_month_ago,
            Date__lte=todays_date
        )
        
        sum_expenses = 0
        for i in addmoney_info:
            if i.add_money == 'Expense':
                sum_expenses += i.quantity
        addmoney_info.sum = sum_expenses
        
        sum_income = 0
        for i in addmoney_info:
            if i.add_money == 'Income':
                sum_income += i.quantity
        addmoney_info.sum1 = sum_income
        
        x = user1.userprofile.Savings + addmoney_info.sum1 - addmoney_info.sum
        y = user1.userprofile.Savings + addmoney_info.sum1 - addmoney_info.sum
        
        if x < 0:
            messages.warning(request, 'Your expenses exceeded your savings')
            x = 0
        if x > 0:
            y = 0
        
        addmoney_info.x = abs(x)
        addmoney_info.y = abs(y)
        
        return render(request, 'home/stats.html', {'addmoney': addmoney_info})

def expense_week(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date - datetime.timedelta(days=7)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    
    addmoney = Addmoney_info.objects.filter(
        user=user1,
        Date__gte=one_week_ago,
        Date__lte=todays_date
    )
    
    finalrep = {}
    
    def get_Category(addmoney_info):
        return addmoney_info.Category
    
    Category_list = list(set(map(get_Category, addmoney)))
    
    def get_expense_category_amount(Category, add_money):
        quantity = 0
        filtered_by_category = addmoney.filter(
            Category=Category,
            add_money="Expense"
        )
        for item in filtered_by_category:
            quantity += item.quantity
        return quantity
    
    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y, "Expense")
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def weekly(request):
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_week_ago = todays_date - datetime.timedelta(days=7)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        
        addmoney_info = Addmoney_info.objects.filter(
            user=user1,
            Date__gte=one_week_ago,
            Date__lte=todays_date
        )
        
        sum = 0
        for i in addmoney_info:
            if i.add_money == 'Expense':
                sum = sum + i.quantity
        addmoney_info.sum = sum
        
        sum1 = 0
        for i in addmoney_info:
            if i.add_money == 'Income':
                sum1 = sum1 + i.quantity
        addmoney_info.sum1 = sum1
        
        x = user1.userprofile.Savings + addmoney_info.sum1 - addmoney_info.sum
        y = user1.userprofile.Savings + addmoney_info.sum1 - addmoney_info.sum
        
        if x < 0:
            messages.warning(request, 'Your expenses exceeded your savings')
            x = 0
        
        if x > 0:
            y = 0
        
        addmoney_info.x = abs(x)
        addmoney_info.y = abs(y)
        
        return render(request, 'home/weekly.html', {'addmoney_info': addmoney_info})

def check(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_exists = User.objects.filter(email=email).exists()
        
        if not user_exists:
            messages.error(request, "Email not registered, TRY AGAIN!!!")
            return redirect("/reset_password")
    
    return redirect('/home')

def info_year(request):
    todays_date = datetime.date.today()
    one_year_ago = todays_date - datetime.timedelta(days=365)
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)
    
    addmoney = Addmoney_info.objects.filter(
        user=user,
        Date__gte=one_year_ago,
        Date__lte=todays_date
    )
    
    finalrep = {}
    
    def get_category(addmoney_info):
        return addmoney_info.Category
    
    Category_list = list(set(map(get_category, addmoney)))
    
    def get_expense_category_amount(Category, add_money):
        quantity = 0
        filtered_by_category = addmoney.filter(
            Category=Category,
            add_money="Expense"
        )
        for item in filtered_by_category:
            quantity += item.quantity
        return quantity
    
    for category in Category_list:
        finalrep[category] = get_expense_category_amount(category, "Expense")
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info(request):
    return render(request, 'home/info.html')



"""