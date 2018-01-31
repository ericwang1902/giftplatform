from  rest_framework import generics,mixins

from .serializers import privateareaSerialzer

from users.models import privatearea

class privateareaList(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

class privateareaDetail(generics.GenericAPIView,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset = privatearea.objects.all()
    serializer_class = privateareaSerialzer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def  delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)