from PIL import Image, ImageDraw
from collections import deque
from Graph import *
import networkx as nx
import matplotlib.pyplot as plt

equipamento_vermelho = None
area_manutencao_verde = None

def criar_grafo_a_partir_de_imagem():
    global equipamento_vermelho, area_manutencao_verde  
    # Solicita o caminho da imagem ao usuário
    bitmap_path = input("Informe o caminho para o arquivo bitmap: ")

    # Abre a imagem
    imagem = Image.open(bitmap_path)
    largura, altura = imagem.size
    grafo = Graph()
    
    # Percorre os pixels da imagem e adiciona nós ao grafo
    for x in range(largura):
        for y in range(altura):
            # Adiciona nó para o pixel atual
            grafo.add_node((x, y))

            # Adiciona arestas com base na cor do pixel
            pixel_color = imagem.getpixel((x, y))

            # Se o pixel é vermelho, é o nó de equipamento
            if pixel_color == (255, 0, 0):
                equipamento_vermelho = (x, y)

            # Se o pixel é verde, é um nó de manutenção
            elif pixel_color == (0, 255, 0):
                area_manutencao_verde = (x, y)

            # Se o pixel não for preto (considerando RGB), conecta aos vizinhos
            if pixel_color != (0, 0, 0):
                # Adiciona aresta para o pixel acima
                if y > 0:
                    grafo.add_undirected_edge((x, y), (x, y - 1), 1)

                # Adiciona aresta para o pixel abaixo
                if y < altura - 1:
                    grafo.add_undirected_edge((x, y), (x, y + 1), 1)

                # Adiciona aresta para o pixel à esquerda
                if x > 0:
                    grafo.add_undirected_edge((x, y), (x - 1, y), 1)

                # Adiciona aresta para o pixel à direita
                if x < largura - 1:
                    grafo.add_undirected_edge((x, y), (x + 1, y), 1)

    return grafo

def buscar_caminho_bfs(grafo, equipamento_vermelho, area_manutencao_verde):
    # Executa o BFS e obtém a lista de nós visitados e o dicionário de predecessores
    _, predecessores = grafo.bfs(equipamento_vermelho)

    # Verifica se a área de manutenção verde é alcançável a partir do equipamento vermelho
    if area_manutencao_verde not in predecessores:
        print("Não foi possível encontrar um caminho válido.")
        return None

    # Reconstruir o caminho de volta a partir da área de manutenção verde
    caminho = []
    no_atual = area_manutencao_verde
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = predecessores[no_atual]

    # Inverter o caminho para começar do equipamento vermelho
    caminho.reverse()
    return caminho

def exibir_caminho_com_setas(caminho):
    if caminho is None:
        print("Não há caminho disponível.")
        return

    for i in range(len(caminho) - 1):
        atual = caminho[i]
        proximo = caminho[i + 1]

        # Determina a direção entre os nós
        if proximo[0] > atual[0]:
            direcao = '→'
        elif proximo[0] < atual[0]:
            direcao = '←'
        elif proximo[1] > atual[1]:
            direcao = '↓'
        elif proximo[1] < atual[1]:
            direcao = '↑'
        else:
            direcao = ' '

        print(direcao, end=' ')

    print()

# Recebendo o grafo criado
grafo_resultante = criar_grafo_a_partir_de_imagem()
print(grafo_resultante)

# Busca um caminho usando BFS
caminho = buscar_caminho_bfs(grafo_resultante, equipamento_vermelho, area_manutencao_verde)

# Exibe o caminho encontrado ou informa que não é possível deslocar o equipamento
if caminho:
    print("Caminho encontrado:")
    for passo, coordenadas in enumerate(caminho):
        print(f"Passo {passo + 1}: Mover para {coordenadas}")
else:
    print("Não é possível deslocar o equipamento até a área de manutenção.")

# Exibe os passos de deslocamento
exibir_caminho_com_setas(caminho)
