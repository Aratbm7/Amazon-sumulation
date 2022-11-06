from xml import dom
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from decimal import Decimal
from accounts.models import Merchant
from .models import Category, ProductImage, SubCategory, MobileProduction


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')


class MerchantSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'store_name']


class MobileProductSerilizers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    images = ImageSerializers(many=True, read_only=True)
    merchant = MerchantSerilizer(read_only=True)
    subcategory = serializers.SerializerMethodField(
        method_name='get_subcategory_hyperlink')

    def get_subcategory_hyperlink(self, obj):
        scheme = self.context['scheme']
        domain = self.context['domain']
        url = (
            f'{scheme}://{domain}/categories/{obj.subcategory.category_id}/subcategories/{obj.subcategory_id}')
        return url

    class Meta:
        model = MobileProduction
        fields = ('id', 'title', 'slug', 'unit_price',
                  'inventory', 'brand', 'memory',
                  'ram', 'colors',  'discount', 'price_with_tax',
                  'tax_price', 'price_with_discount',
                  'merchant', 'subcategory', 'images')

    price_with_tax = serializers.SerializerMethodField(
        method_name='price_plus_tax')
    tax_price = serializers.SerializerMethodField(
        method_name='calculate_tax')
    price_with_discount = serializers.SerializerMethodField(
        method_name='discounted_price')

    def price_plus_tax(self, mobileproduction: MobileProduction):
        price_with_tax = mobileproduction.unit_price * Decimal(1.1)
        return Decimal('{:.2f}'.format(price_with_tax))

    def calculate_tax(self, mobileproduction: MobileProduction):
        price = mobileproduction.unit_price * Decimal(1.1)
        tax_price = price - mobileproduction.unit_price
        return Decimal('{:.2f}'.format(tax_price))

    def discounted_price(self, mobileproduction: MobileProduction):
        discounted_price = \
            self.price_plus_tax(mobileproduction) * \
            Decimal(mobileproduction.discount)
        return Decimal('{:.2f}'.format(discounted_price))

    def create(self, validated_data):
        count = MobileProduction.objects.all().count() + 1
        return MobileProduction.objects.create(id=count, **validated_data)


class SubcategorySerializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    # products = MobileProductSerilizers(many=True, read_only=True)
    products = serializers.SerializerMethodField('get_products')

    def get_products(self, obj):
        scheme = self.context['scheme']
        domain = self.context['domain']
        return (f'{scheme}://{domain}/products/?subcategory__id={int(obj.id)}')

    class Meta:
        model = SubCategory
        fields = ('id', 'title', 'slug', 'description', 'products')

    def create(self, validated_data):
        category_id = self.context['category_id']
        id = SubCategory.objects.all().count() + 1
        print(validated_data)
        return SubCategory.objects.create(id=id, category_id=category_id, **validated_data)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    subcategories = serializers.SerializerMethodField('get_subcategories')

    def get_subcategories(self, category):
        print(self.context['domain'])
        print(self.context['scheme'])
        scheme = self.context['scheme']
        domain = self.context['domain']
        return (f'{scheme}://{domain}/categories/{category.id}/subcategories')

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'description',
                  'created_at', 'is_active', 'subcategories')

    def create(self, validated_data):
        id = Category.objects.all().count() + 1
        return Category.objects.create(**validated_data, id=id)
