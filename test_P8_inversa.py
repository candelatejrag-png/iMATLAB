import pytest
import modular
from test_imatlab import try_command

@pytest.mark.parametrize("n,p,salida_esperada",[
    (2,7,4),
    (111,250,241),
    (2154,2423,1216)
])
def test_inversa_mod_p_basico(n: int, p:int, salida_esperada: int) -> None:
    assert(modular.inversa_mod_p(n,p)==salida_esperada)


def test_potencia_mod_p_cero():
    """ Este test comprueba que, en los casos esperados,
    realmente se lanza la excepción esperada"""
    with pytest.raises(ZeroDivisionError):
        modular.inversa_mod_p(2,0)
    with pytest.raises(ValueError):
        modular.inversa_mod_p(24,6)

@pytest.mark.parametrize("n,p,salida_esperada",[    
    (2,7,"4"),
    (2,0,"NE"),
    (111,250,'241'),
    (2154,2423,'1216')
])
def test_inversa_imatlab(n: int, p:int, salida_esperada: str) -> None:
    try_command(f"inv({n},{p})",salida_esperada)