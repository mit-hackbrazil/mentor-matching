#!/usr/bin/python
# -*- coding: utf-8 -*-

import gflags
import sys
import os
import edmonds_karp

FLAGS = gflags.FLAGS
gflags.DEFINE_string('mentors', 'test/mentors.txt', 'Mentors info file.')
gflags.DEFINE_string('teams', 'test/teams.txt', 'Teams info file.')

class Mentor:
    def __init__(self, name, areas, preferences, nteams):
        self.name = name
        self.areas = areas
        self.preferences = preferences
        switcher = {
            "Times com idéia inicial , sem plano de negócios ou protótipo": 0,
            "Times um pouco mais avançados, mas ainda com desafios para lançar o produto no mercado": 1,
            "Times com soluções prontas e que já tem faturamento": 2,
        }
        self.preferences = [switcher[p] for p in preferences]
        self.nteams = int(nteams)

    def __str__(self):
        return self.name

class Team:
    def __init__(self, name, area, stage):
        if len(name) > 20:
            name = name[:20]

        self.name = name
        self.areas = area
        switcher = {
            "Ideia delineada, esboços do design"    : 0,
            "Protótipo sendo feito"                 : 0,
            "Protótipo ou produto em versão beta"   : 1,
            "Pré-venda"                             : 1,
            "Lançado no mercado"                    : 2,
        }
        self.stage = switcher[stage]

    def __str__(self):
        return self.name

def usage():
    print("python match.py --mentors [mentors_file] --teams [teams_file]")

def read_file(file):
    if not os.path.isfile(file):
        print("File doesn't exist: `%s`" % file)
        sys.exit(1)
    return open(file, 'r').read().splitlines()[1:] # skip header line

def extract_mentors(mentors_file):
    lines = read_file(mentors_file)
    mentors = []
    for (i, m) in enumerate(lines):
        tks = m.split("\t")
        if len(tks) != 14:
            print(len(tks))
            print("Can't parse line %s in file `%s`" % (i, mentors_file))
            sys.exit(1)

        name = tks[1]
        preferences = tks[6].split(";")
        areas = tks[10].split(";")
        nteams = tks[7]
        mentor = Mentor(name, areas, preferences, nteams)
        mentors.append(mentor)

    return mentors


def extract_teams(teams_file):
    lines = read_file(teams_file)
    teams = []
    for (i, m) in enumerate(lines):
        tks = m.split("\t")
        if len(tks) != 72:
            print(tks)
            print("Can't parse line %s in file `%s`" % (i, teams_file))
            sys.exit(1)

        name = tks[2]
        area = tks[-1].split(";")
        stage = tks[-8]
        team = Team(name, area, stage)
        teams.append(team)

    return teams

def make_graph(mentors, teams):
    graph = {}
    for m in mentors:
        for t in teams:
            # create an edge between a mentor and a team, if and only
            # if the mentor has expertise in one of the team's area and the
            # stage of the team is in the mentor's preference
            if set(t.areas).intersection(set(m.areas)) and t.stage in m.preferences:
                graph[(t, m)] = edmonds_karp.Edge(1, 0)
                graph[(m, t)] = edmonds_karp.Edge(1, 1)

    for t in teams:
        graph[("src", t)] = edmonds_karp.Edge(2, 0)
        graph[(t, "src")] = edmonds_karp.Edge(2, 2)

    # TODO: mentors can have multiple teams
    for m in mentors:
        graph[(m, "dst")] = edmonds_karp.Edge(m.nteams, 0)
        graph[("dst", m)] = edmonds_karp.Edge(m.nteams, m.nteams)

    return graph

def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError as e:
        print(e)
        usage()
        sys.exit(1)

    mentors = extract_mentors(FLAGS.mentors)
    teams = extract_teams(FLAGS.teams)
    graph = make_graph(mentors, teams)

    flow = edmonds_karp.max_flow("src", "dst", graph)

    print("%20s\t%40s" % ("Team", "Mentor"))
    for t in teams:
        for m in mentors:
            e = (t, m)
            if e in graph and graph[e].flow > 0:
                print("%20s\t%40s" % (t, m))

    print("Matched %s out of %s" % (flow, 2*len(teams)))

if __name__ == '__main__':
    main(sys.argv)