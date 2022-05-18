
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from sympy import Integral, Symbol,Eq, solve, expand,init_printing ,integrate
from integrais.models import Integral
from integrais.api.serializers import IntegralSerializer
from django.db import connections


class Pagination(PageNumberPagination):
    page_size = 50
    
class IntegralViewSet(ModelViewSet):
    queryset = Integral.objects.all()
    serializer_class = IntegralSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter)
    filter_fields = ('id','f_x', 'g_x','a','b', 'area', 'valor')
    
    @action(detail=False, methods=['POST'], url_path='calcula')
    def insere(self, request):
        
        x = Symbol('x')
        f_x = request.data['f_x']
        g_x = request.data['g_x']
        
        init_printing(pretty_print=True)
        valor_metro_quadrado = 4.000
        
        try:
            f_x = expand(f_x)
            g_x = expand(g_x)
            
            total = Eq(f_x, g_x)
            total = solve(total)
            print(f"a: {total[0]}")
            print(f"b: {total[1]}")

            integral_final = integrate((f_x) - g_x, (x,total[0],total[1])).doit().evalf()
            resultado = integrate((f_x) - g_x, (x,total[0],total[1])).doit().evalf(4) if integral_final > 9.9 else integrate((f_x) - g_x, (x,total[0],total[1])).doit().evalf(2)
            print(f'{resultado} m²')
            resultado = float(resultado)
            valor = (valor_metro_quadrado * resultado)

            print(f'R$ {round(valor,3)}')
            
            sql = f"""INSERT INTO integral(f_x, g_x, a, b, area, valor) VALUES ('{f_x}', '{g_x}','{total[0]}', '{total[1]}' ,{resultado}, 3.0/{valor});"""
                        
            with connections['default'].cursor() as cursor:
                cursor.execute(sql)            
            cursor.close()    
            connections['default'].close()
            
            
            return Response(valor)
        except Exception as e:
            print(e)
            return Response(print("A conta não pode ser realizada"))
        