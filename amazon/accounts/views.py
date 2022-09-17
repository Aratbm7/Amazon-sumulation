
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CustomerSerializer, MerchantSerializer
from .models import Customer, Merchant
from rest_framework import status


class CustomerViewset(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'option', 'header']
    queryset = Customer.objects.select_related('address').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            print(request.data)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(request.data)

            return Response(serializer.data)

    # @action(detail=False, permission_classes=[IsAuthenticated], methods=['GET', 'PUT'], serializer_class=AddressSerializer)
    # def address(self, request):
    #     customer = Customer.objects.only('id').get(user_id=request.user.id)
    #     if request.method == 'GET':
    #         address = Address.objects.get(
    #             customer_id=customer.id)
    #         serializer = AddressSerializer(address)
    #         return Response(serializer.data)

    #     elif request.method == 'PUT':
    #         address = Address.objects.get(
    #             customer_id=customer.id)
    #         serializer = AddressSerializer(
    #             address, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.data)


class MerchantViewset(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        merchent = Merchant.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = MerchantSerializer(merchent)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = MerchantSerializer(
                merchent, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        # elif request.method == 'DELETE':
        #     Merchant.objects.get(user_id=request.user.id).delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
