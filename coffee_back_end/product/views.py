from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Product, Recipe, RecipeItem, PromotionalPrice, TimeSlotPrice
from .serializers import (
    CategorySerializer, ProductSerializer, RecipeSerializer, 
    RecipeItemSerializer, PromotionalPriceSerializer, TimeSlotPriceSerializer
)

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(product_code__icontains=search) |
                Q(description__icontains=search)
            )
        
        # 按分类筛选
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        
        # 按产品类型筛选
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        
        # 按状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def recipe(self, request, pk=None):
        """获取产品的配方"""
        product = self.get_object()
        try:
            recipe = Recipe.objects.get(product=product)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response({"detail": "配方不存在"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def promotional_prices(self, request, pk=None):
        """获取产品的促销价格"""
        product = self.get_object()
        prices = PromotionalPrice.objects.filter(product=product)
        serializer = PromotionalPriceSerializer(prices, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def time_slot_prices(self, request, pk=None):
        """获取产品的时段价格"""
        product = self.get_object()
        prices = TimeSlotPrice.objects.filter(product=product)
        serializer = TimeSlotPriceSerializer(prices, many=True)
        return Response(serializer.data)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        recipe_items = request.data.pop('recipe_items', [])
        serializer = self.get_serializer(data=request.data, context={'recipe_items': recipe_items})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        recipe_items = request.data.pop('recipe_items', [])
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # 更新配方项
        if recipe_items:
            # 先删除现有项
            RecipeItem.objects.filter(recipe=instance).delete()
            # 添加新项
            for item in recipe_items:
                RecipeItem.objects.create(recipe=instance, **item)
        
        return Response(serializer.data)

class RecipeItemViewSet(viewsets.ModelViewSet):
    queryset = RecipeItem.objects.all()
    serializer_class = RecipeItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class PromotionalPriceViewSet(viewsets.ModelViewSet):
    queryset = PromotionalPrice.objects.all()
    serializer_class = PromotionalPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        queryset = PromotionalPrice.objects.all()
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按激活状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

class TimeSlotPriceViewSet(viewsets.ModelViewSet):
    queryset = TimeSlotPrice.objects.all()
    serializer_class = TimeSlotPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        queryset = TimeSlotPrice.objects.all()
        
        # 按产品筛选
        product = self.request.query_params.get('product', None)
        if product:
            queryset = queryset.filter(product__id=product)
        
        # 按激活状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset
