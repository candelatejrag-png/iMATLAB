import modular as m
import time
i = time.time()
print(m.factorizar_cripto(1008999991*1008069017))
f = time.time()
t1 = f-i
i = time.time()
print(m.factorizar_cripto_2(1008999991*1008069017))
f = time.time()
t2 = f-i
print(t1, t2)