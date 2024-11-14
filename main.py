import csv
import random
import os
from collections import Counter
from colorama import Fore, init
from tqdm import tqdm

# Inicializa o Colorama para compatibilidade com Windows
init(autoreset=True)

# Configurações de apostas para diferentes tipos de jogos
CONFIGURACOES_JOGOS = {
    "mega_sena": {
        "intervalo_numeros": 60,
        "tamanho_combinacao": 6,
        "num_quentes": 10,
        "num_frios": 10,
        "num_combinacoes": 100,
        "num_geracoes": 10000,
        "max_fitness": 5
    },
    "lotofacil": {
        "intervalo_numeros": 25,
        "tamanho_combinacao": 15,
        "num_quentes": 8,
        "num_frios": 8,
        "num_combinacoes": 100,
        "num_geracoes": 10000,
        "max_fitness": 12
    },
    "quina": {"intervalo_numeros": 80, "tamanho_combinacao": 5, "num_quentes": 20, "num_frios": 20, "num_combinacoes": 50, "num_geracoes": 8000, "max_fitness": 3},
    "dupla_sena": {"intervalo_numeros": 50, "tamanho_combinacao": 6, "num_quentes": 12, "num_frios": 12, "num_combinacoes": 50, "num_geracoes": 10000, "max_fitness": 4},
    "lotomania": {"intervalo_numeros": 100, "tamanho_combinacao": 50, "num_quentes": 25, "num_frios": 25, "num_combinacoes": 100, "num_geracoes": 15000, "max_fitness": 25},
    "timemania": {"intervalo_numeros": 80, "tamanho_combinacao": 10, "num_quentes": 20, "num_frios": 20, "num_combinacoes": 80, "num_geracoes": 8000, "max_fitness": 8}
}

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
def analisar_numeros_anteriores(resultados_anteriores, num_quentes, num_frios):
    todos_os_numeros = [numero for resultado in resultados_anteriores for numero in resultado]
    contagem = Counter(todos_os_numeros)
    
    # Obter os 'num_quentes' números mais frequentes
    numeros_quentes = [numero for numero, _ in contagem.most_common(num_quentes)]
    
    # Obter os 'num_frios' números menos frequentes
    numeros_frios = [numero for numero, _ in contagem.most_common()[:-num_frios-1:-1]]
    
    return numeros_quentes, numeros_frios

# Função de fitness (ajustada para considerar os números "quentes" e "frios")
def fitness(combinacao, numeros_quentes, numeros_frios, configuracao):
    pontuacao = 0
    for numero in combinacao:
        if numero in numeros_quentes:
            pontuacao += 2  # Pontuação maior para números "quentes"
        elif numero in numeros_frios:
            pontuacao += 1  # Pontuação menor para números "frios"
    # Penalidade para combinações com números duplicados
    pontuacao -= (configuracao["tamanho_combinacao"] - len(set(combinacao)))
    return pontuacao

# Função para criar uma combinação inicial aleatória
def gerar_combinacao(intervalo_numeros, tamanho_combinacao):
    return random.sample(range(1, intervalo_numeros + 1), tamanho_combinacao)

# Algoritmo genético com critério de parada por fitness máximo
def algoritmo_genetico(configuracao, caminho_arquivo):
    # Lê os resultados anteriores do CSV
    resultados_anteriores = ler_resultados_csv(caminho_arquivo)

    # Analisando números passados para determinar quentes e frios
    numeros_quentes, numeros_frios = analisar_numeros_anteriores(
        resultados_anteriores,
        configuracao["num_quentes"],
        configuracao["num_frios"]
    )

    # Inicializa a população
    populacao = [gerar_combinacao(configuracao["intervalo_numeros"], configuracao["tamanho_combinacao"]) for _ in range(configuracao["num_combinacoes"])]
    max_fitness = configuracao["max_fitness"]

    # Lista para armazenar todas as combinações com fitness máximo
    combinacoes_fitness_maximo = []

    print(Fore.YELLOW + "Iniciando o algoritmo genético...")

    # Barra de progresso para as gerações
    for geracao in tqdm(range(configuracao["num_geracoes"]), desc=Fore.GREEN + "Gerando combinações...", ncols=100):
        # Avalia a fitness de cada combinação na população
        fitness_populacao = [(combinacao, fitness(combinacao, numeros_quentes, numeros_frios, configuracao)) for combinacao in populacao]
        # Ordena a população pela fitness em ordem decrescente
        fitness_populacao.sort(key=lambda x: x[1], reverse=True)
        
        # Filtra combinações que atingiram o fitness máximo e as acumula
        for combinacao, score in fitness_populacao:
            if score == max_fitness and combinacao not in combinacoes_fitness_maximo:
                combinacoes_fitness_maximo.append(combinacao)
        
        # Seleciona as melhores combinações para crossover
        pais = [individuo[0] for individuo in fitness_populacao[:50]]
        
        # Cria nova população através de crossover e mutação
        nova_populacao = pais[:]
        while len(nova_populacao) < configuracao["num_combinacoes"]:
            pai = random.choice(pais)
            mae = random.choice(pais)
            filho = pai[:3] + mae[3:]
            
            # Mutação
            if random.random() < 0.1:  # Probabilidade de mutação de 10%
                mutado = random.randint(1, configuracao["intervalo_numeros"])
                while mutado in filho:
                    mutado = random.randint(1, configuracao["intervalo_numeros"])
                filho[random.randint(0, configuracao["tamanho_combinacao"] - 1)] = mutado
            
            nova_populacao.append(filho)
        
        # Atualiza a população para a próxima geração
        populacao = nova_populacao

    # Exibe todas as combinações com o fitness máximo
    if combinacoes_fitness_maximo:
        print(Fore.CYAN + f"\nTotal de combinações com fitness {max_fitness}: {len(combinacoes_fitness_maximo)}")
        for combinacao in combinacoes_fitness_maximo:
            print(Fore.GREEN + f"Combinação: {combinacao}")
    else:
        print(Fore.RED + "\nNenhuma combinação com o fitness máximo foi encontrada.")

    return combinacoes_fitness_maximo

# Função para escolher o jogo e o arquivo de histórico
def selecionar_jogo_e_arquivo():
    print(Fore.BLUE + "\nEscolha o tipo de jogo:")
    for idx, jogo in enumerate(CONFIGURACOES_JOGOS, start=1):
        print(Fore.CYAN + f"{idx}. {jogo.capitalize()}")
    
    opcao_jogo = int(input(Fore.BLUE + "\nDigite o número do jogo: ")) - 1
    nome_jogo = list(CONFIGURACOES_JOGOS.keys())[opcao_jogo]
    configuracao = CONFIGURACOES_JOGOS[nome_jogo]
    
    print(Fore.BLUE + "\nArquivos de histórico disponíveis:")
    arquivos = [f for f in os.listdir() if f.startswith("historico") and f.endswith(".csv")]
    for idx, arquivo in enumerate(arquivos, start=1):
        print(Fore.CYAN + f"{idx}. {arquivo}")
    
    opcao_arquivo = int(input(Fore.BLUE + "\nDigite o número do arquivo de histórico: ")) - 1
    caminho_arquivo = arquivos[opcao_arquivo]
    
    return configuracao, caminho_arquivo

# Executa o programa
def main():
    configuracao, caminho_arquivo = selecionar_jogo_e_arquivo()
    combinacoes_maximas = algoritmo_genetico(configuracao, caminho_arquivo)
    if combinacoes_maximas:
        print(Fore.GREEN + "\nCombinações com o fitness máximo encontradas!")
    else:
        print(Fore.YELLOW + "\nNenhuma combinação com o fitness máximo foi encontrada.")

if __name__ == "__main__":
    main()
