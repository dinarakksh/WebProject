from rest_framework import serializers

from core import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('id', 'src',)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = models.Category()
        category.name = validated_data.get('name')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductCreateOrUpdateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    in_stock = serializers.BooleanField(required=False)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        product = models.Product()
        product.name = validated_data.get('name')
        product.price = validated_data.get('price')
        product.category_id = validated_data.get('category_id')
        product.in_stock = validated_data.get('in_stock')
        product.description = validated_data.get('description')
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.price = validated_data.get('price')
        instance.category_id = validated_data.get('category_id')
        instance.in_stock = validated_data.get('in_stock')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class CartItemCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ('product', 'quantity')


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer()

    class Meta:
        model = models.CartItem
        fields = ('id', 'product', 'quantity', 'total_price')


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = models.UserPersonalCart
        fields = ('items', 'total_price')