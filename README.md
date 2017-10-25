# Match de mentores e equipes da HackBrazil.

Esse programa match mentores e equipes da HackBrazil baseado nas seguintes variáveis:

- área de atuação das equipes;
- estágio do projeto da equipe;
- áreas de expertise dos mentores; e
- preferências dos mentores

Cada equipe recebe 2 mentores, e mentores podem especificar um número máximo de
equipes para mentorar.

## Algoritmo

Tratando o problema como um problema de fluxo máximo, onde existe mentores e equipes
são nodos e existe um arco entre uma equipe `t` e um mentor `m`, se e somente se, o
mentor `m` tem expertise na área de atuação de `t` e o estágio do projeto está dentro
das preferências dos mentores.

Usando o algoritmo de [Edmonds-Karp](https://pt.wikipedia.org/wiki/Algoritmo_de_Edmonds-Karp),
achamos o matching que satisfaz as preferências dos mentores e que garante que
cada equipe receba um mentor dentro da sua área de atuação.

## Modo de usar

```
python match.py --mentors mentors.txt --teams teams.txt
```
