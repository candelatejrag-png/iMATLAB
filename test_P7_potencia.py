import pytest
import modular
from test_imatlab import try_command

@pytest.mark.parametrize("base,exp,p,salida_esperada",[
    (2,3,7,1),    
    (-8,-9,7,6),
    (186,152,15,6),
    (112,23,9,7),
    (16,-5,7,2)    
])
def test_potencia_mod_p_basico(base: int, exp:int, p:int, salida_esperada: int) -> None:
    assert(modular.potencia_mod_p(base,exp,p)==salida_esperada)


def test_potencia_mod_p_cero():
    """ Este test comprueba que, en los casos esperados,
    realmente se lanza la excepción esperada"""
    with pytest.raises(ZeroDivisionError):
        modular.potencia_mod_p(2,3,0)
    with pytest.raises(ZeroDivisionError):
        modular.potencia_mod_p(0,0,7)

@pytest.mark.parametrize("base,exp,p,salida_esperada",[    
    (2,3,7,"1"),
    (0,0,0,"NE"),
    (0,0,9,'NE'),
    (-8,-9,7,'6'),
    (8,6,4,'0'),
    (112,23,9,'7') 
])
def test_potencia_imatlab(base: int, exp:int, p:int, salida_esperada: str) -> None:
    try_command(f"pow({base},{exp},{p})",salida_esperada)