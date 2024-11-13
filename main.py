import csv
import random
from collections import Counter
from colorama import Fore, init
from tqdm import tqdm

# Inicializa o Colorama para compatibilidade com Windows
init(autoreset=True)

# Função para ler os números históricos a partir do CSV
def ler_resultados_csv(caminho_arquivo):
    resultados = []
    with open(caminho_arquivo, mode='r') as file:
        leitor = csv.reader(file)
        next(leitor)  # Ignora o cabeçalho
        for linha in leitor:
            resultados.append(list(map(int, linha[2:])))  # Pega os números dos concursos (colunas 2 a 7)
    return resultados

# Função para analisar os números quentes e frios
def analisar_numeros_anteriores(resultados_anteriores, num_quentes=6, num_frios=6):
    todos_os_numeros = [numero for resultado in resultados_anteriores for numero in resultado]
    contagem = Counter(todos_os_numeros)
    
    # Obter os 'num_quentes' números mais frequentes
    numeros_quentes = [numero for numero, _ in contagem.most_common(num_quentes)]
    
    # Obter os 'num_frios' números menos frequentes
    numeros_frios = [numero for numero, _ in contagem.most_common()[:-num_frios-1:-1]]
    
    return numeros_quentes, numeros_frios

# Função de fitness (ajustada para considerar os números "quentes" e "frios")
def fitness(combinacao, numeros_quentes, numeros_frios):
    pontuacao = 0
    for numero in combinacao:
        if numero in numeros_quentes:
            pontuacao += 2  # Pontuação maior para números "quentes"
        elif numero in numeros_frios:
            pontuacao += 1  # Pontuação menor para números "frios"
    # Penalidade para combinações com números duplicados
    pontuacao -= (6 - len(set(combinacao)))
    return pontuacao

# Função para criar uma combinação inicial aleatória
def gerar_combinacao():
    return random.sample(range(1, 61), 6)

# Algoritmo genético com critério de parada por fitness máximo
def algoritmo_genetico(caminho_arquivo, max_geracoes=10000):
    # Lê os resultados anteriores do CSV
    resultados_anteriores = ler_resultados_csv(caminho_arquivo)

    # Analisando números passados para determinar quentes e frios
    numeros_quentes, numeros_frios = analisar_numeros_anteriores(resultados_anteriores)

    # Inicializa a população
    populacao = [gerar_combinacao() for _ in range(100)]
    max_fitness = 12  # Valor de fitness máximo desejado

    print(Fore.YELLOW + "Iniciando o algoritmo genético...")

    # Barra de progresso para as gerações
    for geracao in tqdm(range(max_geracoes), desc=Fore.GREEN + "Gerando combinações...", ncols=100):
        # Avalia a fitness de cada combinação na população
        fitness_populacao = [(combinacao, fitness(combinacao, numeros_quentes, numeros_frios)) for combinacao in populacao]
        # Ordena a população pela fitness em ordem decrescente
        fitness_populacao.sort(key=lambda x: x[1], reverse=True)
        
        # Verifica se encontramos a combinação ideal
        if fitness_populacao[0][1] == max_fitness:
            print(Fore.CYAN + f"\nCombinação ideal encontrada na geração {geracao}: {fitness_populacao[0][0]} com fitness {fitness_populacao[0][1]}")
            return fitness_populacao[0][0]
        
        # Seleciona as melhores combinações para crossover
        pais = [individuo[0] for individuo in fitness_populacao[:50]]
        
        # Cria nova população através de crossover e mutação
        nova_populacao = pais[:]
        while len(nova_populacao) < 100:
            pai = random.choice(pais)
            mae = random.choice(pais)
            filho = pai[:3] + mae[3:]
            
            # Mutação
            if random.random() < 0.1:  # Probabilidade de mutação de 10%
                mutado = random.randint(1, 60)
                while mutado in filho:
                    mutado = random.randint(1, 60)
                filho[random.randint(0, 5)] = mutado
            
            nova_populacao.append(filho)
        
        # Atualiza a população para a próxima geração
        populacao = nova_populacao

    print(Fore.RED + "\nLimite de gerações alcançado sem encontrar a combinação ideal.")
    return None  # Caso não encontre uma combinação com o fitness máximo

# Caminho do arquivo CSV com os resultados da Mega-Sena
caminho_arquivo = 'historico_megasena.csv'  # Substitua pelo caminho correto do arquivo CSV

# Executando o algoritmo genético
melhor_combinacao = algoritmo_genetico(caminho_arquivo)
if melhor_combinacao:
    print(Fore.GREEN + "\nMelhor combinação encontrada:", melhor_combinacao)
else:
    print(Fore.YELLOW + "\nNenhuma combinação com o fitness máximo foi encontrada.")
