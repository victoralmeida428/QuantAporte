# 🚀 QuantAport: Motor de Alocação Quantitativa

O **AlphaTerminal** é uma ferramenta profissional de gestão de portfólio e rebalanceamento de carteiras. Construído sob os pilares da teoria moderna de portfólios (Fronteira Eficiente de Markowitz), o sistema auxilia investidores a tomarem decisões de aporte mensal baseadas em eficiência estatística (Risco vs. Retorno), eliminando o viés emocional do mercado.

## 📊 Tese de Investimento (Features)

* **Otimização Institucional:** Utiliza a covariância robusta de *Ledoit-Wolf Shrinkage* para evitar que o modelo sofra com ruídos e anomalias de curto prazo do mercado.
* **Perfis de Risco Dinâmicos:** Ajuste automático da alocação macro (Ações vs. FIIs) de acordo com o apetite a risco do investidor (Conservador, Moderado, Arrojado).
* **Execução Realista:** O motor de rebalanceamento calcula a quantidade exata de cotas inteiras possíveis de se comprar com o aporte disponível, respeitando o saldo em caixa e evitando alavancagem não intencional.
* **Resiliência de Dados:** Tratamento automático de tickers inválidos, dados faltantes e matrizes não-convexas (*KKT Matrix Errors*), garantindo que o sistema gere ordens seguras mesmo em dias de instabilidade na B3 ou na API do Yahoo Finance.
* **Interface Visual Integrada:** Painel web interativo construído em Streamlit para visualização consolidada do patrimônio e geração da "boleta" de ordens.

## 🏛️ Arquitetura do Sistema (SOLID)

O projeto foi desenhado para ser escalável e de fácil manutenção, separando claramente as responsabilidades:

```text
meu_terminal/
│
├── core/
│   └── config.py          # Parâmetros macro e perfis de risco
├── data/
│   └── market_data.py     # Conexão com B3/Yahoo Finance e limpeza de dados
├── domain/
│   ├── optimizer.py       # Motor matemático (Markowitz + PyPortfolioOpt)
│   └── rebalancer.py      # Tesouraria (Cruzamento da meta com o aporte e caixa)
├── ui/
│   └── charts.py          # Geração de visualizações e gráficos da carteira
├── app.py                 # Ponto de entrada (Interface Streamlit)
├── Makefile               # Automação de comandos
└── requirements.txt       # Dependências blindadas do projeto
```

## ⚙️ Pré-requisitos e Setup

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para um gerenciamento de pacotes e ambientes virtuais de altíssima performance. 

1. Certifique-se de ter o `uv` instalado na sua máquina.
2. Clone este repositório.
3. Na raiz do projeto, execute o comando de setup automatizado pelo Makefile:

```bash
make setup
```

*Isso criará o ambiente virtual (`.venv`) e instalará as dependências financeiras (`yfinance`, `PyPortfolioOpt`, `streamlit`, `pandas`, etc.) em frações de segundo.*

## 🕹️ Como Operar a Mesa (Uso)

Para iniciar a interface do AlphaTerminal no seu navegador, execute:

```bash
make run
```

1. **Configure o Aporte:** Selecione seu perfil de risco e o valor financeiro disponível para o mês na barra lateral.
2. **Defina o Universo:** Insira os tickers das Ações e FIIs que passaram pelo seu *screener* fundamentalista.
3. **Posição Atual:** Preencha a tabela central com o valor financeiro (R$) que você já possui de cada ativo na sua corretora.
4. **Execução:** Clique em "Calcular Otimização e Gerar Ordens" e copie a boleta gerada para o seu Home Broker.

Para limpar arquivos de cache temporários gerados durante o uso, utilize:

```bash
make clean
```

## ⚠️ Disclaimer Financeiro

**Este software é uma ferramenta de apoio à decisão matemática e estatística, não uma recomendação de investimento.** O mercado financeiro é volátil e retornos passados não garantem rentabilidade futura. O algoritmo calcula a Fronteira Eficiente com base no histórico recente dos preços, o que não substitui a análise fundamentalista da saúde financeira das empresas e fundos imobiliários que compõem a sua carteira. Opere com responsabilidade.
