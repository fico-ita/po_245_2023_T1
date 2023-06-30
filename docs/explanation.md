This part of the project documentation focuses on an **understanding-oriented**
approach. You'll get a chance to read about the background of the project, as well as
reasoning about how it was implemented.

# Contexto

Esse projeto foi inicialmente proposto pelo _Grupo de Interesse em Finanças Computacionais e Investimentos Sistemáticos_ do Instituto Tecnológico de Aeronáutica (ITA).

O desenvolvimento desse projeto foi baseado no livro [Machine Learning for Factor Investing](http://www.mlfactor.com) de 2018, escrito por Chapman. O livro apresenta uma metodologia de aplicação e avaliação de modelos e estratégias de investimentos derivadas do _Factor Investing_.

Nesse sentido, este projeto busca utilizar as técnicas propostas no livro para avaliar a influência do modelo de fatores no Mercado brasileiro.

# Solução

Utilizando os dados do mercado financeiro brasileiro, e seguindo a metodologia de construção dos fatores proposta por Fama e French (1993) é possível avaliar os fatores do Mercado brasileiro e identificar se essas anomalias conseguem explicar os retornos dos ativos da bolsa.

Além disso, foi realizado um teste de Modelo de Aprendizado de Máquina tradicional (Regressão Linear) para realizar a predição dos sinais de compra de um portfólio simplificado a fim de verificar o retorno acumulado dessa estratégia de investimentos.

# Desenvolvimento

Para desenvolvimento dessa solução foram realizadas as seguintes etapas:

1. Aquisição de dados.
2. Manipulação e pré-processamento dos dados.
3. Testes estatísiticos dos Fatores no Mercado Brasileiro.
4. Construção de Estratégia de Investimentos.

Os conhecimentos necessários para desenvolver essa solução foram:

- Noções de Análise Técnica de ativos.

- Aprendizado de Máquina

- Programação na Linguagem Python.

# Bibliotecas necessárias

A solução desenvolvida na linguagem Python utiliza as seguintes bibliotecas:

- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/stable/)

# Colaboração

Esse é um projeto Open source, e pode ser utilizado e modificado por outras pessoas.
