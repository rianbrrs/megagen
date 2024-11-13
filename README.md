# Algoritmo Genético para Previsão de Números da Mega-Sena

Este projeto utiliza **algoritmos genéticos** para tentar prever os números da **Mega-Sena** com base nos resultados históricos. O objetivo é usar uma abordagem de inteligência artificial para evoluir combinações de números e tentar identificar padrões que aumentem as chances de acerto.

## Como Funciona

1. **Análise dos Resultados Históricos**:
   - O algoritmo analisa os números de sorteios passados para identificar os números mais frequentes (quentes) e os menos frequentes (frios).
2. **Algoritmo Genético**:
   - Uma população inicial de combinações de números é gerada aleatoriamente.
   - As combinações são avaliadas com base em sua "fitness" (probabilidade de acerto) e evoluem ao longo de várias gerações.
   - A cada geração, ocorre a **seleção**, o **crossover** (cruzamento) e a **mutação** das combinações.
3. **Objetivo**:
   - Encontrar a combinação de números com o **fitness máximo**, ou seja, a combinação mais provável de ser sorteada.

## Funcionalidades

- **Geração de Combinações**: O algoritmo cria várias combinações de números aleatórias e as avalia.
- **Fitness**: A avaliação das combinações é baseada na frequência de números quentes e frios dos sorteios anteriores.
- **Barra de Progresso**: Uma barra de progresso foi adicionada para exibir o avanço do algoritmo durante as gerações.
- **Saída Visual**: O código usa cores para destacar as informações importantes e tornar a execução mais interessante.

## Instalação

### Requisitos

- Python 3.x
- Bibliotecas:
  - `colorama`
  - `tqdm`

### Instalação das Dependências

Para instalar as dependências necessárias, basta rodar o comando:

```bash
pip install colorama tqdm
```

### Como Usar

- Prepare o Arquivo CSV:

Crie um arquivo CSV com os resultados históricos da Mega-Sena no seguinte formato:

```code
concurso,data,n1,n2,n3,n4,n5,n6
2795,09/11/2024,13,16,55,43,46,33
2794,07/11/2024,3,14,28,52,20,9
```

### Execute o Script:

- Para rodar o script, basta executar o arquivo Python no terminal:

```bash
python main.py
```

### Resultado:

O algoritmo irá rodar até encontrar uma combinação com o máximo fitness ou atingir o número máximo de gerações. O progresso será exibido no terminal com uma barra de progresso e saídas coloridas para facilitar o acompanhamento.

### Exemplo de Saída

- Durante a execução, você verá mensagens como:

```bash
Iniciando o algoritmo genético...
Gerando combinações... |██████████████████████████████████████████████████████████████████████| 100% [geração 10000/10000]
Combinação ideal encontrada na geração 5400: [13, 16, 55, 43, 46, 33] com fitness 12
```

- Ou, caso não encontre a combinação ideal:

```bash
Limite de gerações alcançado sem encontrar a combinação ideal.
```

### Contribuição

Sinta-se à vontade para contribuir com melhorias, sugestões ou correções. Para isso, basta abrir uma issue ou enviar um pull request.

### Licença

Este projeto está licenciado sob a MIT License.

### Explicação do `README.md`

1. **Título e Descrição**: O título descreve o projeto e a descrição explica o objetivo do algoritmo genético para previsão de números da Mega-Sena.
2. **Funcionalidades**: Lista as principais funcionalidades do código.
3. **Instalação**: Orientações sobre como configurar o ambiente para rodar o código, incluindo requisitos e instalação das dependências.
4. **Como Usar**: Passos para usar o código, incluindo a preparação do arquivo CSV e a execução do script.
5. **Exemplo de Saída**: Mostra como o terminal será exibido durante a execução.
6. **Contribuição**: Instruções para quem quiser contribuir com o projeto.
7. **Licença**: Informa a licença sob a qual o código está sendo compartilhado (MIT, neste caso).
