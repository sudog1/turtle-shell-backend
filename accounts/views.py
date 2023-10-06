from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class AccountView(APIView):
    def get(self,request):
        pass
    def put(self,requeest):
        pass


class AccountProfileView(APIView):
    pass

class AccountFollowView(APIView):
    pass

