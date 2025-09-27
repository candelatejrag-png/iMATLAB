import re

pattern = re.compile(r"([a-zA-Z_]+)+\((.*?)\)")

c1 = "euler(3)"
c2 = "mcd(2,4)"
c3 = "pow(-3,4,5)"
dic_comandos = {'primo': 'es_primo','primos': 'lista_primos', 'factorizar': 'factorizar', 'mcd': 'mcd', 'coprimos': 'coprimos', 'pow': 'potencia_mod_p', 'inv': 'inversa_mod_p', 'euler': 'euler', 'legendre': 'legendre', 'resolversistema': 'resolver_sistema_congruencias'}

comando_limpio = {}
for c in [c1,c2,c3]: 
    match = re.search(pattern, c)
    comando_limpio[dic_comandos[match.group(1)]] = re.findall(r"-?\d+", match.group(2))

print(comando_limpio)
    