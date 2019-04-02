# Projeto Cetus
<img src="https://github.com/WilsonCazarre/ProjetoCetus/blob/master/assets/logo.jpeg" width="200" height="200">

_Esse projeto se encontra nos seus estados mais iniciais de desenvolvimento._

O Projeto Cetus tem como proposta desenvolver uma máquina PCR de baixo custo (também chamado de Termociclador). A elaboração está sendo feita por alunos do 3° Mecatrônica Integrado ao Ensino Médio da ETEC Presidente Vargas como proposta para o Trabalho de Conclusão de Curso (TCC).

## Já existem outros Termocicladores no mercado, por que desenvolver outro?

O objetivo do projeto é auxiliar pequenos grupos de pesquisa e empresas pequenas de biotecnologia a ter acesso a um dispositivo que atualmente possuí um custo extremamente elevado no mercado. Grade parte desse custo está relacionado ao fato de não existir um bom investimento na produção nacional do equipamento, elevando seu custo por conta da exportação.

## Toda ajuda é bem-vinda

Por se tratar de um projeto desenvolvido por alunos do ensino médio (com ensino técnico em mecatrônica) estamos necessitados de pessoas com conhecimento na área principalmente na área da pesquisa, você pode nos ajudar apenas preenchendo um simples questionário:
https://docs.google.com/forms/d/1ex0j7108DEeMFs5fmkvnsLnFZ41qZkHM9fczb70snag/edit?usp=sharing

Para dúvidas e/ou sugestões sobre o projeto:

Contatos:

Wilson Cazarré: 

Email: wcs0486@gmail.com

Twitter: @WilsonCazarre


Lucas Felipe:

Email: outrolucas2002@gmail.com

Twitter: @LukaxFeh

## Notas de desenvolvimento
Estruturalmente, a máquina é composta por uma pastilha peltier (entre outros dispositivos para auxiliar no resfriamento) controlada por um microcontrolador ATmega302P, o qual é comandado por um software no computador.

Toda a interface está sendo desenvolvida em Python 3.7 (`tkinter`) e a comunicação via porta
serial se utilizando da biblioteca `PySerial`, tal biblioteca possibilita a
conexão entre o software em python e o microcontrolador.
