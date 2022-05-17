from sympy import *

init_printing(pretty_print=True)
valor_metro_quadrado = 4.000
x = Symbol('x')
f_x = (4*x)
print(type(f_x))
g_x = (x**2)
f_x = Mul(input('Digite a função f(x): '))
total = Eq(f_x, g_x)
total = solve(total)
print(f"a: {total[0]}")
print(f"b: {total[1]}")

integral_final = Integral((f_x) - g_x, (x,total[0],total[1])).doit().evalf()

resultado = Integral((f_x) - g_x, (x,total[0],total[1])).doit().evalf(4) if integral_final > 9.9 else Integral((f_x) - g_x, (x,total[0],total[1])).doit().evalf(2)
print(f'{resultado} m²')
resultado = float(resultado)
valor = (valor_metro_quadrado * resultado)

print(f'R$ {round(valor,2)}')