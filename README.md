# Match de mentores e equipes da HackBrazil.

Esse programa match mentores e equipes da HackBrazil baseado nas seguintes variáveis:

- área de atuação das equipes;
- áreas de expertise dos mentores; e
- preferências dos mentores para cada equipe

## Algoritmo

Tratando o problema como um problema de fluxo máximo, onde existe mentores e equipes
são nodos e existe um arco entre uma equipe t e um mentor m, se e somente se, o
mentor m tem expertise na área de atuação de t. Além disso, as preferências dos
mentores para cada equipe servem como peso para a capacidade do arco entre o
mentor e a equipe.

Usando o algoritmo de [Edmonds-Karp](https://pt.wikipedia.org/wiki/Algoritmo_de_Edmonds-Karp),
achamos o matching que maximiza as preferências globais dos mentores, garantindo que
cada equipe receba um mentor dentro da sua área de atuação.

## Modo de usar

```python
python match.py --mentors mentors.txt teams teams.txt
```

onde `teams.txt` contém as áreas de atuações dos times no formato
```
team1,area1
team2,area2
```

e mentors.tst contém as áreas de expertise dos times no formato
```
mentor1,area1,area2
mentor2,area2,area3,area4
```


