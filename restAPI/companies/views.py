from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import  status
from .models import Stock
from django.http import  Http404
from .serializers import StockSerializer
from rest_framework.response import Response


# class LoginRequiredMixin(object):
#     """
#     View mixin which verifies that the user has authenticated.
#
#     NOTE:
#         This should be the left-most mixin of a view.
#     """
#     @classmethod
#     def as_view(cls):
#         return login_required(super(LoginRequiredMixin, cls).as_view())
#     # @method_decorator(login_required)
#     # def dispatch(self, *args, **kwargs):
#     #     return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

# list all stocks or create a new one
# stocks/FB/
class StockList(APIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        # print "this is StockList"
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StockDetail(APIView):
    def get_queryset(self):

        return Stock.objects.filter(owner=self.request.user)

    def get_object(self, pk, *args, **kwargs):
        try:
            return Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # print "this is StockDetail"
        stock = self.get_object(pk)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        stock = self.get_object(pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        stock = self.get_object(pk)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
