from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from small_web.serializers import SignUpSerializer

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(template_name="index.html")


class SignUpAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signup.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = SignUpSerializer()
        return Response({"serializer": serializer, "style": self.style})

    def post(self, request):
        user_data = request.POST
        serializer = SignUpSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response({"serializer": serializer, "style": self.style})
        return Response(template_name="index.html")

