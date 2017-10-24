#!/usr/bin/python
import gflags
import sys
import os
import edmonds_karp

FLAGS = gflags.FLAGS
gflags.DEFINE_string('mentors', 'test/mentors.txt', 'Mentors info file.')
gflags.DEFINE_string('teams', 'test/teams.txt', 'Teams info file.')

def read_file(file):
    if not os.path.isfile(file):
        print("File doesn't exist: `%s`" % file)
        sys.exit(1)
    return open(file, 'r').read().splitlines()

def extract_mentors(mentors_file):
    lines = read_file(mentors_file)
    d = {}
    for (i, m) in enumerate(lines):
        tks = m.split(",")
        if not tks:
            print("Can't parse line %s in file `%s`" % (i, mentors_file))
            sys.exit(1)
        if len(tks) < 2:
            continue
        mentor = tks[0]
        d[mentor] = tks[1:]

    return d


def extract_teams(teams_file):
    lines = read_file(teams_file)
    d = {}
    for (i, m) in enumerate(lines):
        tks = m.split(",")
        if len(tks) != 2:
            print("Can't parse line %s in file `%s`" % (i, teams_file))
            sys.exit(1)

        team = tks[0]
        d[team] = tks[1]

    return d

def make_graph(mentors, teams):
    graph = {}
    for m in mentors:
        exps = mentors[m]
        for t in teams:
            area = teams[t]
            if area in exps:
                graph[(t, m)] = edmonds_karp.Edge(1, 0)
                graph[(m, t)] = edmonds_karp.Edge(1, 1)

    for t in teams:
        graph[("src", t)] = edmonds_karp.Edge(1, 0)
        graph[(t, "src")] = edmonds_karp.Edge(1, 1)

    for m in mentors:
        graph[(m, "dst")] = edmonds_karp.Edge(1, 0)
        graph[("dst", m)] = edmonds_karp.Edge(1, 1)

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

    print flow
    for t in teams:
        for m in mentors:
            e = (t, m)
            if e in graph and graph[e].flow > 0:
                print t, m


if __name__ == '__main__':
    main(sys.argv)