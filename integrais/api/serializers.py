from rest_framework.serializers import ModelSerializer
from integrais.models import Integral

class IntegralSerializer(ModelSerializer):
    class Meta:
        model = Integral
        fields = ['id','f_x', 'g_x','a','b', 'area', 'valor']