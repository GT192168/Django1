


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
class LoginMiddleWare(MiddlewareMixin):

    def process_request(self,request):

        if request.path in ["/login/","/reg/","/get_valid_img/"]:
            return None

        if not request.user.id:
            return redirect("/login/")

