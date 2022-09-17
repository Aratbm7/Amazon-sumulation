
from rest_framework import serializers
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from drf_writable_nested.mixins import NestedUpdateMixin
# from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Customer, Address, Merchant


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'code']

    # def create(self, validated_data):
    #     customer_id = models.Customer.objects.get(
    #         id=validated_data['customer_id']).id
    #     return Address.objects.create(**validated_data, customer_id=customer_id)

    # def update(self, instance, validated_data):
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.street = validated_data.get('street', instance.street)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.save()
    #     return instance

    # def save(self, **kwargs):
    #     city = self.validated_data['city']
    #     street = self.validated_data['street']
    #     code = self.validated_data['code']
    #     return super().save(**kwargs)


class CustomerSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    address = AddressSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'image', 'birth_day', 'phone', 'is_merchant_user',
                  'membership', 'user_id', 'address']
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='IR'),

        }

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
        address.city = address_data.get('city', address.city)
        address.street = address_data.get('street', address.street)
        address.code = address_data.get('code', address.code)
        address.save()
        return super().update(instance, validated_data)


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'store_name', 'cart_id',
                  'card_image_front', 'card_image_back', ]
