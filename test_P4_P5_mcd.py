from typing import List
import pytest
import modular
from test_imatlab import try_command

@pytest.mark.parametrize("a,b,salida_esperada",[
    (10,15,5),
    (2,17,1),
    (68,276,4),
    (0,0,0),
    (-22,-33,11)   
])
def test_mcd_basico(a: int, b:int, salida_esperada: int) -> None:
    assert(modular.mcd(a,b)==salida_esperada)


@pytest.mark.parametrize("a,b,mcd_esperado",[
    (6,10,2),
    (2,17,1),
    (68,276,4),
    (0,0,0),
    (-22,-33,11)     
])
def test_bezout_basico(a: int, b:int, mcd_esperado: int) -> None:
    (d,x,y)=modular.bezout(a,b)
    assert(d==mcd_esperado)
    assert(a*x+b*y==d)

@pytest.mark.parametrize("nlist,salida_esperada",[
    ([4,10,14],2),
    ([22,34,67],1),
    ([0,0,0,0],0),
    ([-90,-878,36],2)
])
def test_mcd_n_basico(nlist: List[int], salida_esperada: int) -> None:
    assert(modular.mcd_n(nlist)==salida_esperada)


@pytest.mark.parametrize("nlist,mcd_esperado",[
    ([4,10,14],2),
    ([22,34,67],1),
    ([0,0,0,0],0),
    ([-90,-878,36],2)   
])
def test_bezout_n_basico(nlist: List[int], mcd_esperado: int) -> None:
    (d,X)=modular.bezout_n(nlist)
    assert(d==mcd_esperado)
    assert(len(X)==len(nlist))
    suma=0
    for i in range(len(X)):
        suma+=X[i]*nlist[i]
    assert(suma==d)

@pytest.mark.parametrize("comando,salida_esperada",[
    ("mcd(10,15)","5"),
    ("mcd(4)","4"),
    ("mcd(4,10,14)","2"),
    ('mcd(-90,-878,36)','2'),
    ('mcd(0,0,0,0)','0'),
    ('mcd(88,99,77)','11')
])
def test_mcd_n_imatlab(comando:str, salida_esperada: str) -> None:
    try_command(comando,salida_esperada)