from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
import random

from django.http import JsonResponse

from django.contrib import auth
from django import forms

from django.core.exceptions import ValidationError
import re
from app01.models import UserInfo,Customer,ConsultRecord
from app01.form import UserForm
from django.urls import reverse
from django.db.models import Q
from app01.utils.page import Pagination

def login(request):
    '''
    基于ajax和用户认证组件实现的登录功能
    :param request:
    :return:
    '''
    # if request.method=="POST":
    if request.is_ajax():
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        validcode=request.POST.get("validcode")

        #Ajax请求返回一个字典
        response={"user":None,"err_msg":""}
        if validcode.upper() == request.session.get("keep_str").upper():
            user_obj=auth.authenticate(username=user,password=pwd)
            if user_obj:
                auth.login(request,user_obj) # request.session["user_id"]=user_obj.pk
                response["user"]=user
            else:
                response['err_msg']="用户名或者密码错误！"
        else:
            response["err_msg"]="验证码错误！"

        return JsonResponse(response)
    else:
        return render(request, "login.html")

def get_valid_img(request):
    '''
    基于PIL模块获取动态验证码
    :param request:
    :return:
    '''

    #  方式1：读取指定图片
    # with open("static/img/valid.jpg","rb") as f:
    #     data=f.read()


    # 方式2：基于PIL模块创建验证码图片
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO


    def get_random_color():
        import random
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=open("valid.png","wb")
    # img.save(f,"png")
    # with open("valid.png","rb") as f:
    #     data=f.read()

    # 方式3：
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # # 方式4:完善文本
    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # draw=ImageDraw.Draw(img)
    # font=ImageFont.truetype("static/font/kumo.ttf",32)
    # draw.text((0,0),"python!",get_random_color(),font=font)
    #
    # # 写与读
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # 方式5:

    img = Image.new("RGB", (350, 38), get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/kumo.ttf", 32)

    keep_str=""
    for i in range(6):
        random_num = str(random.randint(0, 9))
        random_lowalf = chr(random.randint(97, 122))
        random_upperalf = chr(random.randint(65, 90))
        random_char=random.choice([random_num,random_lowalf,random_upperalf])
        draw.text((i*30+50,0),random_char, get_random_color(), font=font)
        keep_str+=random_char


    # width=350
    # height=38
    # for i in range(100):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(500):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 写与读
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    print('keep_str',keep_str)

    # 将验证码存在各自的session中

    request.session['keep_str']=keep_str

    return HttpResponse(data)

def reg(request):
    '''
    基于ajax和forms实现的注册功能
    :param request:
    :return:
    '''
    if request.method=="POST":
        print(request.POST)
        form=UserForm(request.POST)
        res={"user":None,"err_msg":""}
        if form.is_valid():
            res["user"]=form.cleaned_data.get("user")
            print("cleaned_data",form.cleaned_data)
            user=form.cleaned_data.get("user")
            pwd=form.cleaned_data.get("pwd")
            email=form.cleaned_data.get("email")

            user=UserInfo.objects.create_user(username=user,password=pwd,email=email)


        else:
            print(form.errors)
            print(form.cleaned_data)
            res["err_msg"] =form.errors

        return JsonResponse(res)


    else:
        form=UserForm()
        return  render(request,"reg.html",locals())

def logout(request):
    auth.logout(request)
    return redirect("/login/")


#############################################


# 登录装饰器


# def login_required(func):
#    def inner(request):
#        if not request.user.id:
#            return redirect("/login/")
#        else:
#            ret=func(request)
#            return ret
#    return inner

from django.contrib.auth.decorators import login_required
from django.views import View
from django import forms
from app01.form import CustomerModelForm

@login_required
def index(request):

    return render(request,"index.html")

# 客户展示类视图
class CustomerView(View):
    def get(self,request):
        if reverse("customers_list") == request.path:
            label="公户列表"
            customer_list = Customer.objects.filter(consultant__isnull=True)
        else:
            label = "我的客户"
            customer_list = Customer.objects.filter(consultant=request.user)

            # search过滤
        val = request.GET.get("q")
        field = request.GET.get("field")
        if val:
            q = Q()
            q.children.append((field + "__contains", val))
            customer_list = customer_list.filter(q)

            # customer_list=customer_list.filter(Q(name__contains=val)|Q(qq__contains=val))

        # 分页
        current_page_num = request.GET.get("page")
        pagination = Pagination(current_page_num, customer_list.count(), request)

        customer_list = customer_list[pagination.start:pagination.end]

        #
        path=request.path
        next="?next=%s"%path

        return render(request, "customer_list.html", {"next":next,"label":label,"customer_list": customer_list, "pagination": pagination})

    def post(self,request):

        # action的批量处理
        print(request.POST)
        func_str=request.POST.get("action")
        data=request.POST.getlist("selected_pk_list")
        if not hasattr(self,func_str):
            return HttpResponse("非法输入！")
        else:
            func=getattr(self,func_str)
            queryset=Customer.objects.filter(pk__in=data)
            ret=func(request,queryset)
            if ret:
                return ret
            # ret=self.get(request)
            # return ret
            return redirect(request.path)

    def patch_delete(self,request,queryset):
        queryset.delete()

    def patch_reverse_gs(self,request,queryset):
        '''
        公户转私户
        :param data:
        :return:
        '''
        ret=queryset.filter(consultant__isnull=True)
        if ret:
            ret.update(consultant=request.user)
        else:
            return HttpResponse("手速太慢！")

    def patch_reverse_sg(self,request,queryset):
        '''
        公户转私户
        :param data:
        :return:
        '''
        queryset.update(consultant=None)







# class AddCustomerView(View):
#
#     def get(self,request):
#         form=CustomerModelForm()
#         return render(request,"add_customer.html",{"form":form})
#
#     def post(self,request):
#         form=CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("customers_list"))
#         else:
#             return render(request, "add_customer.html", {"form": form})
#
#
# class EditCustomerView(View):
#     def get(self,request,id):
#         edit_obj=Customer.objects.get(pk=id)
#         form=CustomerModelForm(instance=edit_obj)
#         return render(request,"edit_customer.html",{"form":form})
#
#     def post(self,request,id):
#         edit_obj = Customer.objects.get(pk=id)
#         form=CustomerModelForm(request.POST,instance=edit_obj)
#         if form.is_valid():
#             form.save()
#             return redirect(request.GET.get("next"))
#         else:
#             return render(request, "edit_customer.html", {"form": form})


class AddEditCustomerView(View):
    def get(self,request,edit_id=None):
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form = CustomerModelForm(instance=edit_obj)
        return render(request, "add_edit_customer.html", {"form": form,"edit_obj":edit_obj})

    def post(self,request,edit_id=None):
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form=CustomerModelForm(request.POST,instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(request, "add_edit_customer.html", {"form": form,"edit_obj":edit_obj})



class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model=ConsultRecord
        # fields="__all__"
        exclude=["delete_status"]



class AddEditConsultRecordView(View):
    def get(self,request,edit_id=None):
        edit_obj = ConsultRecord.objects.filter(pk=edit_id).first()
        form = ConsultRecordModelForm(instance=edit_obj)
        return render(request, "add_edit_consultrecord.html", {"form": form,"edit_obj":edit_obj})

    def post(self,request,edit_id=None):
        edit_obj = ConsultRecord.objects.filter(pk=edit_id).first()
        form=ConsultRecordModelForm(request.POST,instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse("consult_records"))
        else:
            return render(request, "add_edit_consultrecord.html", {"form": form,"edit_obj":edit_obj})









class ConsultRecordView(View):
        def get(self,request):

            consult_record_list=ConsultRecord.objects.filter(consultant=request.user)
            customer_id=request.GET.get("customer_id")
            if customer_id:
                consult_record_list=consult_record_list.filter(customer_id=customer_id)

            return render(request,"consultrecord.html",{"consult_record_list":consult_record_list})