from PIL import Image, ImageDraw
from collections import deque
from Graph import *
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

equipamento_vermelho = None
area_manutencao_verde = None
bitmap_path = None

def criar_grafo_a_partir_de_imagem():
    global equipamento_vermelho, area_manutencao_verde, bitmap_path  
    # Solicita o caminho da imagem ao usuário
    bitmap_path = obter_caminho_imagem()

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
                # Adiciona aresta para o pixel acima (se não for preto)
                if y > 0 and imagem.getpixel((x, y - 1)) != (0, 0, 0):
                    grafo.add_undirected_edge((x, y), (x, y - 1), 1)

                # Adiciona aresta para o pixel abaixo (se não for preto)
                if y < altura - 1 and imagem.getpixel((x, y + 1)) != (0, 0, 0):
                    grafo.add_undirected_edge((x, y), (x, y + 1), 1)

                # Adiciona aresta para o pixel à esquerda (se não for preto)
                if x > 0 and imagem.getpixel((x - 1, y)) != (0, 0, 0):
                    grafo.add_undirected_edge((x, y), (x - 1, y), 1)

                # Adiciona aresta para o pixel à direita (se não for preto)
                if x < largura - 1 and imagem.getpixel((x + 1, y)) != (0, 0, 0):
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
            direcao = '↑'
        elif proximo[1] < atual[1]:
            direcao = '↓'
        else:
            direcao = ' '

        print(f"Mover {direcao} para {proximo}")

    print()

def obter_caminho_imagem():
    # Cria uma janela Tkinter invisível para a seleção de arquivo
    root = Tk()
    root.withdraw()

    # Abre a caixa de diálogo para a seleção do arquivo
    file_path = filedialog.askopenfilename(title="Selecione o arquivo bitmap", filetypes=[("Todos os arquivos", "*.*")])
    return file_path

def visualizar_grafo_customizado(grafo, caminho=None, imagem=None):
    # Obtém os nós e arestas do grafo personalizado
    nodes = list(grafo.adj.keys())
    edges = [(u, v) for u in grafo.adj for v in grafo.adj[u]]

    # Cores dos nós
    node_colors = ['red' if node == equipamento_vermelho else 'green' if node == area_manutencao_verde else 'black' if imagem.getpixel(node) == (0, 0, 0) else 'white' for node in nodes]

    # Cores das arestas
    edge_colors = ['red' if ((u, v) in caminho or (v, u) in caminho) else 'black' for u, v in edges]

    # Cria um gráfico
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    
    # Desenha os nós
    for i, node in enumerate(nodes):
        color = node_colors[i]
        ax.plot(node[0], node[1], marker='o', markersize=10, color=color)

    # Desenha as arestas
    for i, (u, v) in enumerate(edges):
        color = edge_colors[i]
        ax.plot([u[0], v[0]], [u[1], v[1]], color=color)

    # Adiciona rótulos aos nós
    for node in nodes:
        ax.text(node[0], node[1], f"{node}", fontsize=8, ha='center', va='center', color='black')

    # Destaca o caminho percorrido
    if caminho:
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i + 1]
            ax.plot([u[0], v[0]], [u[1], v[1]], color='green')

    # Salva a figura
    plt.savefig("grafo_resultante_customizado.png")

    # Exibe a figura
    plt.show()

# Cria o grafo a partir da imagem
grafo_resultante = criar_grafo_a_partir_de_imagem()
print(grafo_resultante)

# Busca um caminho usando BFS
caminho = buscar_caminho_bfs(grafo_resultante, equipamento_vermelho, area_manutencao_verde)

# Exibe o caminho encontrado ou informa que não é possível deslocar o equipamento
if caminho:
    print("Caminho encontrado:")
    exibir_caminho_com_setas(caminho)

else:
    print("Não é possível deslocar o equipamento até a área de manutenção.")

imagem2 = Image.open(bitmap_path)

visualizar_grafo_customizado(grafo_resultante, caminho, imagem2)
