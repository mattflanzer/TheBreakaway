#! python3
import sys
import argparse

def record_to_league(team, points, league, verbose):
    if (verbose and points > 0):
        print("{} +{} points".format(team, points))
    if team in league:
        league[team] = league[team] + points
    else:
        league[team] = points

def extract_team_and_score(team_line):
    tokenized = team_line.split(" ")
    try:
        score = int(tokenized[-1])
    except:
        raise Exception("unable to parse score from {}".format(team_line))
    name_start = 0
    first = tokenized[0]
    if (len(first) == 0):
        name_start = 1
    elif (first[-1] == '.'): # might be indexed start
        try:
            int(tokenized[0][:-1])
            name_start = 1 # yes it is, skip it
        except:
            pass
    name = " ".join(tokenized[name_start:-1])
    return (name, score)


def record_game(game, league, verbose):
    (team1, team2)= game.split(",")[-2:]
    (name1, score1) = extract_team_and_score(team1)
    (name2, score2) = extract_team_and_score(team2)
    points1 = 0
    points2 = 0
    if (score1 == score2):
        points1 = 3
        points2 = 3
        result = "Tie"
    elif (score1 > score2):
        points1 = 6
        result = "{} wins".format(name1)
    else:
        points2 = 6
        result = "{} wins".format(name2)
    if (verbose):
        print("recording: {}: {}".format(game, result))
    record_to_league(name1, points1, league, verbose)
    record_to_league(name2, points2, league, verbose)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose',action="store_true", help="turn on verbosity", default=False)
    parser.add_argument('inputfile', type=str, nargs=1, help="input file", default=None)
    args = parser.parse_args()
    if not args.inputfile:
        if args.verbose:
            print('no input file specified')
        return -1
    try:
        [filename] = args.inputfile
        with open(filename) as f:
            if (args.verbose):
                print("reading file {}".format(filename))
            league = {}
            games = 0
            for game in f:
                record_game(game.strip(), league, args.verbose)
                games += 1
            if (args.verbose):
                print("recorded {} games with {} teams".format(games, len(league)))
            rankings = sorted(league.items(), key=lambda team: team[1], reverse=True)
            for (index, (name, points)) in enumerate(rankings):
                print("{}. {}, {} points".format(index + 1, name, points))
            pass
    except Exception as e:
        if args.verbose:
            print('unable to parse input {}'.format(str(e)))
        return -1
    return 0

if __name__ == '__main__':
    sys.exit(main())