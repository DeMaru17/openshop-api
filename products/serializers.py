from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request:
            # Mengambil URL utama yang sedang diakses
            base_url = request.build_absolute_uri('/products').rstrip('/')
            
            # Memasukkan array _links sesuai kriteria HATEOAS
            representation['_links'] = [
                {
                    "rel": "self",
                    "href": f"{base_url}",
                    "action": "POST",
                    "types": ["application/json"]
                },
                {
                    "rel": "self",
                    "href": f"{base_url}/{instance.id}/",
                    "action": "GET",
                    "types": ["application/json"]
                },
                {
                    "rel": "self",
                    "href": f"{base_url}/{instance.id}/",
                    "action": "PUT",
                    "types": ["application/json"]
                },
                {
                    "rel": "self",
                    "href": f"{base_url}/{instance.id}/",
                    "action": "DELETE",
                    "types": ["application/json"]
                }
            ]
        return representation