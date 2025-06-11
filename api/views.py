from django.shortcuts import render
from rest_framework import viewsets
from .models import Blog
from .serializers import Blog_positionSerializer
# Create your views here.
# class blog(viewsets.ModelViewSet):
#     queryset = Blog.objects.all().order_by('-created_at')
#     serializer_class = Blog_positionSerializer


# def create_article(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         content = request.POST['content']
#         image = request.FILES.get('image')

#         Article.objects.create(title=title, content=content, image=image)
 
    
#     return render(request, 'dashboard/add_blog.html')

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all().order_by('-created_at')
#     serializer_class = ArticleSerializer



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class BlogCreateAPIView(APIView):
    def get(self, request):
        pblog = Blog.objects.all()
        serializer = BlogSerializer(pblog, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"ok":True,"matn":"ezafe shod"})
        
        return JsonResponse({"ok":False,"matn":serializer.errors})
@method_decorator(csrf_exempt, name='dispatch')
class BlogDetailAPIView(APIView):
    def patch(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"ok":True,"matn":"ezafe shod"})
        return JsonResponse({"ok":False,"matn":serializer.errors})
    
    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse({"ok":False,"matn":serializer.errors})

    def delete(self, request, slug):
        product = get_object_or_404(Blog, slug=slug)
        product.delete()
        return JsonResponse({"ok":True,"matn":"hazf shod"})
