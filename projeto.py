###############
### Gerador ###
###############

from re import S
from tkinter.messagebox import RETRY
from typing import Type


def cria_gerador(b, s):
    """
    Recebe um inteiro (b) correspondente ao número de bits e um inteiro
    correspondente à seed. Devolve o gerador correspondente.
                                                                        #
    b (int) -- Bits
    s (int) -- Seed
    """
    if not isinstance(b, int) or not isinstance(s, int) or b not in [32,64]:
        raise ValueError('cria_gerador: argumentos invalidos')
    return [b, s]

def cria_copia_gerador(g):
    """Devolve uma cópia de um gerador"""
    return g.copy() ### WHAT ###

def obtem_estado(g):
    return g[1]

def define_estado(g, s):
    """ Defone o novo valor do estado do gerador (g) como o inteiro (s) """
    g[1] == s 
    return s

def atualiza_estado(g):
    if not eh_gerador(g): raise TypeError ### IS IT?? ###
    if g[0] == 32:
        g[1] ^= (g[1] << 13) & 0xFFFFFFFF
        g[1] ^= (g[1] >> 17) & 0xFFFFFFFF
        g[1] ^= (g[1] << 5) & 0xFFFFFFFF
    elif g[0] == 64: 
        g[1] ^= (g[1] << 13) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] >> 7) & 0xFFFFFFFFFFFFFFFF
        g[1] ^= (g[1] << 17) & 0xFFFFFFFFFFFFFFFF
    return obtem_estado(g)

def eh_gerador(g):
    if g[0] == 32 or g[0] == 64 and isinstance(g[1], int): return True
    return False

def gerador_para_str(g): return 'xorshift'+str(g[0])+'(s='+str(g[1])+')'

def gera_numero_aleatorio(g, n):
    """
    Aceita um gerador (g) e atualiza o seu estado, devolvendo um número
    aleatório no intervalo [1, n] obtido a partir do estado atualizado
    de g por (1 + mod(s, n)), sendo mod() a operação de divisão inteira
                                                                        #
    g -- Gerador
    n (int) -- Limite superior do intervalo
    """
    g[1] = atualiza_estado(g)
    return 1 + g[1]//n


g1 = cria_gerador(32, 1)
for n in range(3): atualiza_estado(g1)
print(gera_numero_aleatorio(g1, 25))