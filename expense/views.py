from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import PostForm,CreateCategory,StoreForm,CreateIncome
from django.contrib.auth.models import User,auth
from .models import Category,Sub_Category,Customer,Income,Data,Year,Month
from django.db.models import Q
import itertools
import datetime
from django.utils import timezone
from datetime import date,timedelta
from django.urls import reverse
from calendar import monthrange
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        amount = instance.spent
        print(amount)
        m = instance.timestamp.strftime("%B")
        y = instance.timestamp.strftime("%Y")

        month_instance ,created = Month.objects.get_or_create(name= m) 
        print(created)
        year_instance ,created = Year.objects.get_or_create(name =y) 
        print(created)
        instance.month_link = month_instance
        instance.save()
        month_instance.year_link = year_instance
        month_instance.save()

        print("exp")
        messages.success(request,"Successfully Created")
        return redirect("expense:timeline")
    context = {
        "form" : form,
        "action":"create",
    }
    return render(request, "post_form.html", context)

def post_detail(request,id):
    instance = get_object_or_404(Data, id=id)
    context = {
        "title": instance.sub_category, 
        "instance" : instance,
    }
    return render(request, "post_detail.html", context)

def timeline(request):
    queryset_list = Data.objects.filter(user=request.user)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(spent__icontains=query)|
            Q(pay_type__icontains=query)|            
            Q(sub_category__name__icontains=query)|
            Q(sub_category__category__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5) 
    page_request_var ="page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        "object_list" : queryset,
        "title": "Expenditures",
        "page_request_var": page_request_var, 
    }
    return render(request, "timeline.html", context)    

def post_update(request,id=None):
    instance = get_object_or_404(Data, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("expense:timeline")    
    context = {
        "title": instance.sub_category, 
        "instance" : instance,
        "action":"update",
        "form" : form,
    }
    return render(request, "post_form.html", context)

def post_delete(request,id=None):
    instance = get_object_or_404(Data, id=id)
    instance.delete()
    messages.success(request,"Successfully Deleted")
    return redirect("expense:timeline")

def budget(request):
    categories = Category.objects.filter(user=request.user)
    
    form1 = CreateCategory(request.POST or None, request.FILES or None)
    if form1.is_valid():
        instance = form1.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Category Successfully Created")
        return redirect("expense:budget")

    form2 = StoreForm(request.POST or None, request.FILES or None, user=request.user)
    if form2.is_valid():
        f_data = form2.cleaned_data
        instance = Sub_Category(category=f_data['category'], amt=f_data['amt'], name=f_data['name'])
        instance.save()
        data = Data(user=request.user, sub_category=instance, spent=instance.amt, recursive=f_data['recursive'], pay_type=f_data['pay_type'])
        data.save()
        messages.success(request,"Sub-Category Successfully Created")
        return redirect("expense:timeline")
    
    form3 = CreateIncome(request.POST or None, request.FILES or None)
    if form3.is_valid():
        instance = form3.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Income Successfully Created")
        return redirect("expense:budget")


    context = {
        'categories' : categories,
        "cat_form" : form1,        
        "subcat_form" : form2,  
        "income_form" :form3,      
        "action" : "create",
    }
    return render(request,'budget.html',context)

def analytics(request, *args, **kwargs):
    dataset = Data.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    months = Month.objects.filter(year_link__user=request.user)
    years = Year.objects.filter(user=request.user)
    rec_amt=0
    year_expenditure=0
    year_income=0
    labels2 = []
    chart_data = []
    labels1 = []
    chart_data1 = []

    for year in years:
        year.annual_expenditure = 0
        for month in months:
            month.monthly_expenditure = 0
            month.monthly_expenditure += rec_amt
            month.save()
            for data in dataset:    
                m = data.timestamp.strftime("%B")
                y = data.timestamp.strftime("%Y")
                if(data.recursive == True):
                    rec_amt += data.spent
                if(str(year.name) == y):
                    if(str(month.name) == m):
                        month.monthly_expenditure += data.spent
                        month.save()
#            print(month.monthly_expenditure)
            year.annual_expenditure += month.monthly_expenditure
            year.save()
        labels1.append("Expenditure")
        chart_data1.append(year.annual_expenditure)
        year_expenditure=year.annual_expenditure
        print(year.annual_expenditure)

    for year in years:
        year.annual_income = 0
        for month in months:
            month.monthly_income = 0
            for income in incomes:
                m = income.timestamp.strftime("%B")
                y = income.timestamp.strftime("%Y")
                if(str(year.name) == y):
                    if(month.name == m):
                        month.monthly_income +=income.amt
                        month.save()
                        print(month.monthly_income)
            year.annual_income += month.monthly_income
            year.save()
        year_income=year.annual_income
        print(year.annual_income)

    labels1.append("Balance")
    chart_data1.append(year_income-year_expenditure)

    expenditure_total=0
    for category in categories:
        category.amt=0 
        for subcategory in category.sub_category.all():
            subcategory.amt=0
            for data in dataset:
                if data.sub_category == subcategory:
                    subcategory.amt += data.spent
                    subcategory.save()
            category.amt += subcategory.amt
            category.save()
        labels2.append(category.name)
        chart_data.append(category.amt)
        expenditure_total += category.amt
    
        context = {
        'object_list' : dataset,
        'categories' : categories,
        'incomes' : incomes,
        'expenditure_total' : expenditure_total,
        'months' : months,
        'years' : years,
        'labels2': labels2,
        'data2': chart_data,
        'labels1': labels1,
        'data1': chart_data1,
    }
    return render(request, 'analytics.html', context) 

def calendarToday(request):
    if request.user.is_authenticated:
        today = timezone.now()
        print(today)
        d1 = today.strftime("%d")
        d2 = today.strftime("%m")
        d3 = today.strftime("%Y")
        return HttpResponseRedirect(reverse('expense:calendar',kwargs={'date':int(d1),'month':int(d2),'year':(d3)}))
    else:
        return HttpResponseRedirect(reverse('first:login'))
 
def calendar(request,date,month,year):
    day_string = date+"-"+month+"-"+year
    start_date = datetime.datetime.strptime(day_string,"%d-%m-%Y")
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method=="POST":
        print("po")
        if 'pre' in request.POST:
            print("pre")
            if int(month) > 1:
                return redirect('expense:calendar', date='1', month=str(int(month)-1), year=year)
            else:
                return redirect('expense:calendar', date='1', month='12', year=str(int(year)-1))

        if 'next' in request.POST:
            if int(month) < 12:
                return redirect('expense:calendar', date='1', month=str(int(month)+1), year=year)
            else:
                return redirect('expense:calendar', date='1', month='1', year=str(int(year)+1))


        if 'addexpense' in request.POST:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                day = request.POST['req_date']
                print("!!!!!!",day)
                print("!!!!!!",type(day)) 
                day = datetime.datetime.strptime(day, "%Y-%m-%d")
                print("!!!!!!",day) 
                instance.timestamp = day
                instance.save()
                print(instance.timestamp)
                amount = instance.spent
                print(amount)
                m = instance.timestamp.strftime("%B")
                y = instance.timestamp.strftime("%Y")

                month_instance ,created = Month.objects.get_or_create(name= m) 
                print(created)
                year_instance ,created = Year.objects.get_or_create(name =y) 
                print(created)
                instance.month_link = month_instance
                instance.save()
                month_instance.year_link = year_instance
                month_instance.save()


                messages.success(request,"Successfully Created")
                return redirect("expense:timeline")

        else:
            return redirect("expense:calendarToday")

            
    else:

        user = request.user
        day_string = date+"-"+month+"-"+year
    #    day_date = datetime.datetime.strptime(day_string,"%d-%m-%Y")
        d = datetime.date(int(year),int(month),int(date)).strftime("%d")
        m = datetime.date(int(year),int(month),int(date)).strftime("%m")
        y = datetime.date(int(year),int(month),int(date)).strftime("%Y")
        today = timezone.now()
        weekday_start = monthrange(int(year),int(month))[0]
        no_of_days = monthrange(int(year),int(month))[1]
        gaps = list(range(0,weekday_start))
        dates = list(range(1,no_of_days+1))
        monthName = datetime.date(int(year),int(month),int(date)).strftime("%B")

        start_date = datetime.datetime.strptime(day_string,"%d-%m-%Y")
        end_date = start_date +timedelta( days=1 )
        day_dataset = Data.objects.filter(timestamp__range=(start_date, end_date),user=request.user)
        for day_data in day_dataset:
            print(day_data.spent)
            print(day_data.timestamp)

        myrange = list(range(0,7))
        day_no = start_date.weekday()
        context = {
            "form" : form,
            "action":"create",
            'user':request.user,
            'date':int(date),
            'month':int(month),
            'year':int(year),
            'start_date':start_date,
            'gaps':gaps,
            'dates':dates,
            'today_day':today.day,
            'today_month':today.month,
            'today_year':today.year,
            'month_name':monthName,
            'd':d,
            'm':m,
            'y':y,
            'range':myrange,
            'day_no':day_no,
            'username': request.user.get_username,
            'day_dataset':day_dataset
        }
        return render(request,"calendar.html",context)
