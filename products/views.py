from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(APIView):
    def get(self, request):
        # Menyaring data yang belum terhapus (is_delete=False)
        products = Product.objects.filter(is_delete=False)

        # Menangkap parameter pencarian
        name_query = request.query_params.get('name', None)
        location_query = request.query_params.get('location', None)

        if name_query:
            products = products.filter(name__icontains=name_query)
        if location_query:
            products = products.filter(location__icontains=location_query)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        # Mengembalikan format JSON dengan root "products"
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Mengubah status is_delete menjadi True alih-alih menghapus data permanen
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)