# Cetus PCR
<img src="https://github.com/WilsonCazarre/ProjetoCetus/blob/master/assets/logo.png" alt="logo do projeto Cetus - o simbolo de sua constelação" width="200" height="200">

_Esse projeto se encontra nos seus estados mais iniciais de desenvolvimento._

O Projeto Cetus tem como proposta desenvolver uma máquina PCR de baixo custo (também chamado de Termociclador). A elaboração está sendo feita por alunos do 3° Mecatrônica Integrado ao Ensino Médio da ETEC Presidente Vargas como proposta para o Trabalho de Conclusão de Curso (TCC).

### Contribuidores do Projeto
Todos os integrantes do nosso grupo são participantes do 3° ano de Mecatrônica (2019) na ETEC Presidente Vargas. 

São eles: Joice Iris, Kleber Kato, Letícia Araújo, Lucas Souza, Vinicius Maehara e Wilson Cazarré.

## Por que Cetus?

O processo PCR foi desenvolvido em 1983, por Kary Mullis, junto de uma equipe de funcionários da Cetus Corporation, - uma empresa pioneira em biotecnologia e principal desenvolvedora de técnicas para amplificação de DNA, - os quais receberam o Nobel de química por tal invento. Cetus também é uma constelação equatorial que representa uma criatura marinha, sendo o logo do projeto sua representação astrológica.

## Mas afinal, o que é PCR?

PCR (Polymerase Chain Reaction - Reação em Cadeia Polimerase) é uma técnica da biologia molecular utilizada a fim de amplificar cópias de determinado segmento de DNA de forma exponencial, chegando a milhares e milhões de cópias em poucas repetições. Para tal processo é necessário um equipamento que controle a temperatura da amostra em diferentes estágios, formando ciclos.

## Já existem outros Termocicladores no mercado, por que desenvolver mais um?

O objetivo do projeto é auxiliar pequenos grupos de pesquisa, empresas pequenas de biotecnologia e alunos da área a ter acesso a um dispositivo que atualmente possuí um custo extremamente elevado no mercado. Grande parte desse custo está relacionado ao fato de não existir um bom investimento na produção nacional do equipamento, fazendo com que exista um elevado custo de importação.


## Toda ajuda é bem-vinda

Por se tratar de um projeto desenvolvido por alunos do ensino médio (com ensino técnico em mecatrônica) estamos necessitados de pessoas com conhecimento principalmente na área da pesquisa em DNA e processos PCR, você pode nos ajudar apenas preenchendo um simples questionário:

[Formulário do Google](https://docs.google.com/forms/d/e/1FAIpQLSeknZwfgxAJlUGq_nTI-9e_KZr4itc3aowXtJQsjgLXp6w6sQ/viewform)

### Para dúvidas e/ou sugestões sobre o projeto:

Contatos: 
- Wilson Cazarré:
  - Email: wcs0486@gmail.com
  - [Twitter](https://twitter.com/WilsonCazarre)


- Lucas Souza:
  - Email: outrolucas2002@gmail.com
  - [Twitter](https://twitter.com/lukaxfeh)


## Notas de desenvolvimento
Estruturalmente, a máquina é composta por uma pastilha peltier (entre outros dispositivos para auxiliar no resfriamento) controlada por um microcontrolador ATmega302P, o qual é comandado por um software no computador.

Toda a interface está sendo desenvolvida em Python 3.7 (`tkinter`) e a comunicação via porta
serial se utilizando da biblioteca `PySerial`, tal biblioteca possibilita a
conexão entre o software em python e o microcontrolador.

## Como iniciar a interface Cetus PCR
Considerando que a interface ainda não está pronta para lançamento, aqueles que querem testa-lá devem rodar no próprio ambiente do python.
Para isso basta seguir os seguintes passos:

### Pré-requisitos
* Cetus PCR necessita apenas do Python 3 instalado. Python 2 não é suportado.
   * É necessário que o Python esteja no Path do seu sistema (opção configurada na hora da instalação). Caso precise adicionar manualmente basta seguir as [instruções](https://python.org.br/instalacao-windows/).
   

### Configurar um novo ambiente virtual
Faça o download do repositório ProjetoCetus do GitHub.
Após isso, é recomendado criar um ambiente virtual para a aplicação.

Primeiro, tenha certeza de que possuí o Python 3 e o pip corretamente instalados e configurados em sua máquina, 
para isso rode os seguintes comandos no seu Command Prompt:

```
python3 --version
pip3 --version
```

Agora, abra o Command Prompt no diretório do ProjetoCetus e execute os seguintes comandos:

```
python3 -m venv venv
venv/Scripts/activate.bat
```

Se tudo estiver corretamente configurado, seu prompt deverá ter um `(venv)` escrito na frente de cada linha.

Por fim, instale as dependências do Projeto:

```
pip install -r requirements.txt
```

Agora você já deve ser capaz de iniciar a aplicação rodando o arquivo `Cetus PCR.py`.
