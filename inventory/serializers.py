from rest_framework import serializers
from .models import Category, Product, Sale


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'barcode_code', 'category', 'category_id',
            'price', 'quantity',
        ]


class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_barcode = serializers.CharField(source='product.barcode_code', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'product', 'product_name', 'product_barcode',
            'quantity', 'unit_price', 'total_price', 'sold_at', 'note',
        ]
        read_only_fields = ['unit_price', 'total_price', 'sold_at']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        if quantity > product.quantity:
            raise serializers.ValidationError(
                f"Not enough stock. Available: {product.quantity}"
            )
        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        validated_data['unit_price'] = product.price
        validated_data['total_price'] = product.price * quantity
        product.quantity -= quantity
        product.save()
        return super().create(validated_data)
