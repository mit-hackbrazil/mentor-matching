#!/usr/bin/python
# -*- coding: utf-8 -*-

import gflags
import sys
import os
import edmonds_karp

FLAGS = gflags.FLAGS
gflags.DEFINE_string('mentors', 'mentors.txt', 'Mentors info file.')
gflags.DEFINE_string('teams', 'teams.txt', 'Teams info file.')
gflags.DEFINE_string('initial', 'initial.txt', 'Initial matches.')

MENTORS_PER_TEAM = 2
MAX_TEAMS_PER_MENTOR = 2

class Mentor:
    def __init__(self, name, areas, preferences, nteams):
        self.name = name
        self.areas = areas
        self.preferences = []
        switcher = {
            "Times com idéia inicial , sem plano de negócios ou protótipo": 0,
            "Times um pouco mais avançados, mas ainda com desafios para lançar o produto no mercado": 1,
            "Times com soluções prontas e que já tem faturamento": 2,
        }

        for k in switcher:
            if preferences.find(k) >= 0:
                self.preferences.append(switcher[k])

        self.nteams = int(nteams)
        self.match = 0

    def __str__(self):
        return self.name

    def __repr__(self):
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
        self.nmentors = MENTORS_PER_TEAM
        self.match = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def usage():
    print("python match.py --mentors [mentors_file] --teams [teams_file]")

def read_file(file, start):
    if not os.path.isfile(file):
        print("File doesn't exist: `%s`" % file)
        sys.exit(1)
    return open(file, 'r').read().splitlines()[start:]

def extract_mentors(mentors_file):
    lines = read_file(mentors_file, 1)
    mentors = {}
    for (i, m) in enumerate(lines):
        tks = m.split("\t")
        if len(tks) != 14:
            print(len(tks))
            print("Can't parse line %s in file `%s`" % (i, mentors_file))
            sys.exit(1)

        name = tks[2].rstrip()
        preferences = tks[7]
        areas = tks[11].replace(", ", ";").split(";")
        nteams = tks[8]
        mentor = Mentor(name, areas, preferences, nteams)
        mentors[name] = mentor

    return mentors


def extract_teams(teams_file):
    lines = read_file(teams_file, 1)
    teams = {}
    for (i, m) in enumerate(lines):
        tks = m.split("\t")
        if len(tks) != 72:
            print("Can't parse line %s in file `%s`" % (i, teams_file))
            sys.exit(1)

        name = tks[2].rstrip()
        area = tks[-1].replace(",", ";").split(";")
        stage = tks[-9]
        team = Team(name, area, stage)
        teams[name] = team

    return teams

def extract_initial(initial_file):
    lines = read_file(initial_file, 0)
    initial = set()
    for (i, l) in enumerate(lines):
        tks = l.split("\t")
        if len(tks) != 2:
            print("Can't parse line %s in file `%s`" % (i, initial_file))
            sys.exit(1)

        team = tks[0]
        mentor = tks[1]
        initial.add((mentor, team))

    return initial

def make_graph(mentors, teams, initial=set()):
    graph = {}
    for m in mentors.values():
        for t in teams.values():
            # create an edge between a mentor and a team, if and only
            # if the mentor has expertise in one of the team's area and the
            # stage of the team is in the mentor's preference
            if set(t.areas).intersection(set(m.areas)) and t.stage in m.preferences:
                graph[(t, m)] = edmonds_karp.Edge(1, 0)
                graph[(m, t)] = edmonds_karp.Edge(1, 1)

    # fill up initial matches
    for (m, t) in initial:
        t = teams[t]
        m = mentors[m]
        graph[(t, m)] = edmonds_karp.Edge(1, 1)
        graph[(m, t)] = edmonds_karp.Edge(0, 0)

        t.match += 1
        m.match += 1

    for t in teams.values():
        graph[("src", t)] = edmonds_karp.Edge(t.nmentors, t.match)
        graph[(t, "src")] = edmonds_karp.Edge(t.nmentors, t.nmentors)

    for m in mentors.values():
        nteams = max(min(1, m.nteams), m.match)
        graph[(m, "dst")] = edmonds_karp.Edge(nteams, m.match)
        graph[("dst", m)] = edmonds_karp.Edge(nteams, nteams)

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
    initial = extract_initial(FLAGS.initial)
    graph = make_graph(mentors, teams, initial)

    flow = edmonds_karp.max_flow("src", "dst", graph, len(initial))
    if flow < MENTORS_PER_TEAM * len(teams):
        for m in mentors.values():
            e = (m, "dst")
            nteams = min(MAX_TEAMS_PER_MENTOR, m.nteams, graph[e].cap + 1)
            graph[e].cap = nteams
        flow = edmonds_karp.max_flow("src", "dst", graph, flow)

    print("%20s\t%40s" % ("Team", "Mentor"))
    for t in teams.values():
        for m in mentors.values():
            e = (t, m)
            if e in graph and graph[e].flow > 0:
                print("%20s\t%40s" % (t, m))

    # some mentor stats
    unmatched = []
    two_teams = 0
    many_teams = 0
    for m in mentors.values():
        e = (m, "dst")
        if graph[e].flow == 0:
            unmatched.append(m)
        if graph[e].flow == 2:
            two_teams += 1
        if graph[e].flow > 2:
            many_teams += 1

    print("Matched %s out of %s" % (flow, MENTORS_PER_TEAM*len(teams)))
    print("Unmatched mentors: %s %s" % (len(unmatched), unmatched))
    print("Mentors with two teams: %s" % two_teams)
    print("Mentors with many teams: %s" % many_teams)




if __name__ == '__main__':
    main(sys.argv)