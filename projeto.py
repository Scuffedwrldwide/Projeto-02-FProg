###############
### Gerador ###
###############

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
    """ Define o novo valor do estado do gerador (g) como o inteiro (s) """
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

def gerador_para_str(g): 
    if eh_gerador(g): return 'xorshift'+str(g[0])+'(s='+str(g[1])+')'

def gera_numero_aleatorio(g, n):
    """
    Aceita um gerador (g) e atualiza o seu estado, devolvendo um número
    aleatório no intervalo [1, n] obtido a partir do estado atualizado
    de g por (1 + mod(s, n)), sendo mod() a operação de divisão inteira
                                                                        #
    g (TAD)      -- Gerador
    n (int)      -- Limite superior do intervalo
    return (int) -- Número aleatório
    """
    if not eh_gerador(g) or not isinstance(n, int) or n < 1: raise ValueError ### HUH?? ###
    g[1] = atualiza_estado(g)
    return 1 + g[1]%n

def gera_carater_aleatorio(g, c):
    """
    Aceita um gerador (g) e atualiza o seu estado, devolvendo um número
    aleatório no intervalo [1, n] obtido a partir do estado atualizado
    de g por (1 + mod(s, n)), sendo mod() a operação de divisão inteira
                                                                        #
    g (TAD)      -- Gerador
    c (int)      -- Carater 'máximo' 
    return (str) -- Carater aleatório
    """
    if ord(c) < ord('A')  or  ord(c) > ord('Z'): raise ValueError
    return chr(gera_numero_aleatorio(g, ord(c)-64)+64) # Gera um número em [65, ord(c)] sendo 65 o codigo ASCII de 'A'

##################
### Coordenada ###
##################

def cria_coordenada(col,lin): 
    """
    Recebe uma string correspondente à coluna e um inteiro de 0 a 99
    e devolve a correspondente coordenada, um tipo imutável

    col    (str) -- Carater da coluna
    lin    (int) -- Inteiro da linha
    return (TAD) -- Coordenadas  
    """
    if  not isinstance(col, str) or ord(col) < ord('A') or ord(col) > ord('Z')\
        or not isinstance(lin, int) or lin < 1 or lin > 99\
        or not eh_coordenada((col,lin)):
            raise ValueError('cria_coordenada: argumentos invalidos')
    return (col,lin)

def obtem_coluna(c): return c[0]
def obtem_linha(c): return c[1]

def eh_coordenada(arg):
    """ Verifica se um argumento é uma coordenada. """
    if  isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], int)\
        and ord(arg[0]) >= ord('A') and ord(arg[0]) <= ord('Z') and 1 <= arg[1] and arg[1] <= 99:
            return True
    return False

def coordenadas_iguais(c1, c2):
    """ Compara duas coordenadas e verifica se são iguais """
    if  eh_coordenada(c1) and eh_coordenada(c2) and obtem_coluna(c1) == obtem_coluna(c2)\
        and obtem_linha(c1) ==  obtem_linha(c2):
            return True
    return False

def coordenada_para_str(c):
    """Devolve uma string que representa a coordenada dada como argumento"""
    if not eh_coordenada: raise TypeError ### DO I? ###
    num = lambda x: '0'+str(x) if x < 10 else str(x)
    return c[0] + num(c[1])

def str_para_coordenada(s):
    """Devolve uma coordenada definida pela string dada como argumento"""
    if len() == 3: return cria_coordenada(s[0],eval(s[1:]))

def obtem_coordenadas_vizinhas(c):
                                                                        #
    """Dada uma coordenada, devolve as coordenadas vizinhas, começando 
    pela superior esquerda na ordem dos ponteiros do relógio."""
    if not eh_coordenada(c): raise TypeError
    viz = []
    char = lambda offset: chr(ord(c[0])+offset)
    line = obtem_linha(c)
    for i in [
        (char(-1), line-1), (char(0), line-1), (char(1), line-1),   # Acima da coordenada
        (char(1), line),                                            # Direita da coordenada
        (char(1), line+1), (char(0), line+1), (char(-1), line+1),   # Abaixo da coordenada
        (char(-1), line),                                           # Esquerda da coordenada
    ]:
        if eh_coordenada(i): viz.append(i)
    return tuple(viz)

def obtem_coordenada_aleatoria(c, g):
                                                                        #
    """ Utilizando o TAD Gerador, devolve uma coordenada alearória.
    O argumento C define a maior linha e coluna possíveis. Pode ser
    entendido geométricamente como o 'canto inferior direito' da àrea
    na qual se procura gerar uma coord. aleatória 
    
    c (TAD) -- Maior linha e coluna possíveis
    g (TAD) -- Gerador
    """
    col, line = obtem_coluna(c), obtem_linha(c)
    return cria_coordenada(
        gera_carater_aleatorio(g,col),
        gera_numero_aleatorio(g,line)
    )

###############
### Parcela ###
###############

# Estados:
#   Limpa Destapada  -- ( ? ) 
#   Marcada Tapada   -- ( @ )
#   Tapada           -- ( # )
#   Minada Destapada -- ( X )

def cria_parcela(): return {'state': '#', 'mine': 0} 

def cria_copia_parcela(p): 
    if eh_parcela(p): return p.copy()

def limpa_parcela(p):
    """ Atualiza o estado da parcela para 'limpa' ('?') """
    if eh_parcela(p): 
        p.update({'state': '?'})
        return p
    raise ValueError ### WHICH?? ###

def marca_parcela(p):
    """ Atualiza o estado da parcela para 'marcada' ('@') """
    if eh_parcela(p): 
        p.update({'state': '@'})
        return p
    raise ValueError ### WHICH?? ###

def desmarca_parcela(p):
    """ Atualiza o estado da parcela para 'tapada' ('#') """
    if eh_parcela(p): 
        p.update({'state': '#'})
        return p
    raise ValueError ### WHICH?? ###

def esconde_mina(p):
    """ Atualiza o estado da parcela para 'minada' ('X') """
    if eh_parcela(p): 
        p.update({'mine': 1})
        return p
    raise ValueError ### WHICH?? ###

def eh_parcela(arg):
    if isinstance(arg, dict) and list(arg.keys()) == ['state', 'mine']\
        and arg['state'] in ['?', '@', '#', 'X'] and arg['mine'] in [0,1]:
            return True
    return False

def eh_parcela_limpa(p): 
    if not eh_parcela(p): raise ValueError ### WHICH?? ###
    return p['state'] == '?'
def eh_parcela_marcada(p): 
    if not eh_parcela(p): raise ValueError ### WHICH?? ###
    return p['state'] == '@'
def eh_parcela_tapada(p):
    if not eh_parcela(p): raise ValueError ### WHICH?? ###
    return p['state'] == '#'    
def eh_parcela_minada(p): 
    if not eh_parcela(p): raise ValueError ### WHICH?? ###
    return p['mine'] == 1

def parcelas_iguais(p1,p2):
    if not eh_parcela(p1) or not eh_parcela(p2): return False
    if p1 == p2: return True
    return False

def parcela_para_str(p):
    if eh_parcela(p): return p['state']
    raise TypeError ### WHICH? ###

def alterna_bandeira(p):
    if eh_parcela_marcada(p): 
        p = desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p): 
        p = marca_parcela(p)
        return True
    return False

#############
### Campo ###
#############

def cria_campo(c, l):
    """
                                                                        #
    Cria um campo de minas de acordo com a cadeia de caracteres 'c' e o 
    número de linhas 'l', correspondentes à coordenada do canto inferior
    direito do campo. O campo toma a forma de um dicionário de listas. 
    Cada lista corresponde a uma coluna, e cada Parcela (TAD) numa 
    dada lista corresponde à interceção de uma coluna com uma linha.

    c (str) -- Colunas pretendidas
    l (int) -- Linhas pretendidas
    """
    minefield = dict()
    if eh_coordenada(cria_coordenada(c, l)):
        for col in range(65, ord(c)+1):
            minefield.update({chr(col): [cria_parcela() for i in range(l)]})
    return minefield

def cria_copia_campo(m):
    """ Retorna uma copia profunda do minefield (m)"""
    copy = dict()
    if eh_campo(m):
        for col in range(65, ord(obtem_ultima_coluna(m))): copy.update({chr(col): m[chr(col)]})
        return copy
    
def obtem_ultima_coluna(m): return list(m.keys())[-1]

def obtem_ultima_linha(m): return len(m['A'])

def obtem_parcela(m, c):
    """ Devolve a parcela localizada na coordenada 'c'
    
    m (TAD) -- Campo de Minas
    c (TAD) -- Coordenadas
    """
    return (m[obtem_coluna(c)])[obtem_linha(c)-1]

def obtem_coordenadas(m, s):
                                                                        #
    """ 
    Devolve um tuplo contendo todas as parcelas correspondentes ao 
    estado 's', ordenadas da esquerda para a direita e de cima a baixo
    segundo a sua posição no campo 'm'
    
    m (TAD) -- Campo de Minas
    s (str) -- Estado selecionado
    """

    coords = list()
    for c in list(m.keys()):
        for p in m[c]:
            if s == parcela_para_str(p): coords.append(p)
    return tuple(coords)

def obtem_numero_minas_vizinhas(m, c):
    """
    Devolve o número de parcelas vizinhas à coordenada que escondem se
    verificam minadas
    
    """
    if not eh_coordenada_campo(m, c): raise TypeError ### idk man ###
    count = 0
    for coord in obtem_coordenadas_vizinhas(c):
        if eh_parcela_minada(obtem_parcela(m, coord)): count += 1
    return count

def eh_campo(arg):
    def keys(arg):
        for k in arg.keys():
            if not isinstance(k, str) or ord('A') > ord(k) or ord('Z') < ord(k): return False
        return True
    def values(arg):
        for k in arg.keys():
            for p in k:
                if not eh_parcela(p): return False
        return True
    return isinstance(arg, dict) and  0 < len(arg) <= 27 and keys(arg) and values(arg)

def eh_coordenada_campo(m, c):
    return eh_campo and eh_coordenada(c)\
        and ord(obtem_coluna(c)) <= ord(obtem_ultima_coluna(m))\
        and obtem_linha(c) <= obtem_ultima_coluna(m)

def campos_iguais(m1, m2): return eh_campo(m1) and eh_campo(m2) and m1 == m2

def campo_para_str(m):
    def line_str(m):
        num = lambda x: '0'+str(x) if x < 10 else str(x)
        linestr = ''
        for line in range(1, obtem_ultima_linha(m)+1):
            p = ''
            for col in list(m.keys()):
                p += parcela_para_str(obtem_parcela(m,cria_coordenada(col, line)))
            linestr += num(line)+'|'+p+'|\n'
        return linestr

    def header(m):
        cols = '   '
        for i in list(m.keys()): cols += i
        return cols

    separator = '  +' + '-'*(ord(obtem_ultima_coluna(m))-64) + '+'
    return header(m) + '\n' + separator + '\n' + line_str(m) + separator
