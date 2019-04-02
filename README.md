# Projeto Cetus
<img src="https://github.com/WilsonCazarre/ProjetoCetus/blob/master/assets/logo.jpeg" width="200" height="200">

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

O objetivo do projeto é auxiliar pequenos grupos de pesquisa, empresas pequenas de biotecnologia e alunos da área a ter acesso a um dispositivo que atualmente possuí um custo extremamente elevado no mercado. Grande parte desse custo está relacionado ao fato de não existir um bom investimento na produção nacional do equipamento, fazendo com que exista um elevado custo de exportação.


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
