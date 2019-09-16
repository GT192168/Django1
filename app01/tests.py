from django.test import TestCase

# Create your tests here.

import random


random_num=random.randint(0,9)
random_lowalf=chr(random.randint(97,122))
random_upperalf=chr(random.randint(65,90))


from django.db.models import Q


from app01.models import Customer


Q().children.append(())

Customer.objects.filter(name__contains="赵")