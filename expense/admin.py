from django.contrib import admin
from .models import Customer
from .models import Category
from .models import Sub_Category
from .models import Income
from .models import Data,Month,Year
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Income)
admin.site.register(Data)
admin.site.register(Month)
admin.site.register(Year)