import re
import sys
from collections import defaultdict

INT_RE = re.compile(r'\d+')
FLOAT_RE = re.compile(r'0\.\d+')
N_START = '/'
EXP_START = '='
EXP_END_START = '-'
STAT_START = '>'

EXP_NUM = 4
METHOD_NUM = 6

def parse_int_from(line):
    return int(INT_RE.search(line).group(0))


def parse_floats_from(line):
    return map(float, FLOAT_RE.findall(line))


def expect(start_str, lines):
    line = lines.next()
    while not line.startswith(start_str):
        line = lines.next()
    return line


def parse_method(lines):
    line = expect('Running', lines)
    method = line[8:line.index('[')]
    line = expect(STAT_START, lines)
    stats = parse_floats_from(line)
    return method, stats


def parse_experiment(exp_no, lines):
    start_line = expect(EXP_START, lines)
    #print '    experiment %d' % parse_int_from(start_line)

    results = []
    for i in range(METHOD_NUM):
        m, stats = parse_method(lines)
        results.append((m, stats))
        #print '        P: %.4f, R: %.4f - %s' % (stats[0], stats[1], m)

    expect(EXP_END_START, lines)

    return results


def parse_repeated_experiment_results(line):
    stats = parse_floats_from(line)
    method = line[line.rindex('-- ')+3:line.index('[')]
    return (method, stats)


def parse_repeated_experiment(N, lines):
    print 'N = %d' % N,
    line = lines.next()
    repeat = parse_int_from(line)
    print 'REPEAT = %d' % repeat

    exp_results = defaultdict(list)
    for i in range(repeat):
        for m, stats in parse_experiment(i+1, lines):
            exp_results[m].append(stats)

    # get average
    average_stats = dict(parse_repeated_experiment_results(expect('Precision', lines)) for i in range(METHOD_NUM))

    final_results = {}
    for m, avg_stats in average_stats.iteritems():
        avg_prec, avg_rec = avg_stats
        method_exp_results = exp_results[m]
        max_prec = max(method_exp_results, key=lambda t:t[0])[0]
        min_prec = min(method_exp_results, key=lambda t:t[0])[0]
        max_rec = max(method_exp_results, key=lambda t:t[1])[1]
        min_rec = min(method_exp_results, key=lambda t:t[1])[1]
        final_results[m] = (avg_prec, avg_prec-min_prec, max_prec-avg_prec, avg_rec, avg_rec-min_rec, max_rec-avg_rec)

        data = final_results[m] + (m,)
        #print 'P([-/+]): %.4f(%.4f/%.4f) | R([-/+]): %.4f(%.4f/%.4f) - %s' % data

    return final_results


def print_4f(l):
    return '[' + ', '.join('%.4f'%i for i in l) + ']'


f = open(sys.argv[1])
lines = iter(f)
db_info = lines.next()
db = re.search(r'\[((\w|_)+)\]', db_info).group(1)
print 'Database: %s' % db

results = defaultdict(lambda: ([], [], [], [], [], [],))
for i in range(EXP_NUM):
    line = expect(N_START, lines)
    N = parse_int_from(line)

    for m, res in parse_repeated_experiment(N, lines).iteritems():
        for i, d in enumerate(res):
            results[m][i].append(d)

# print data organized by methods
for m, res in results.iteritems():
    print m
    print '  Precision', print_4f(res[0])
    print '          -', print_4f(res[1])
    print '          +', print_4f(res[2])
    print '     Recall', print_4f(res[3])
    print '          -', print_4f(res[4])
    print '          +', print_4f(res[5])

f.close()
