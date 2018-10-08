import argparse
import sys
import re


def sravnenie(st1, st2):
    if st1 in st2:
        return True
    else:
        if re.match(st1, st2) is None:
            return False
        else:
            return True




def output_test (line, params):
    if (params.line_number is True) and (params.after_context or params.before_context or params.context):
        d = line.index(line)
        d = str(d)
        stri = d+'-'+line
        output(stri)
    elif params.line_number:
        d = line.index(line)
        d = str(d)
        stri = d + ':' + line
        output(stri)
    else:
        output(line)


def output(line):
        print(line)


def grep(lines, params):
    test = []
    aaa = set()
    if (params.pattern.find('?') >= 0) or (params.pattern.find('*') >= 0):
        params.pattern = params.pattern.replace('*','\w*')
        params.pattern = params.pattern.replace('?','.')
        params.pattern = '\w*' + params.pattern + '\w*'
    for i in range(len(lines)):
        test.append(lines[i])

    if params.ignore_case:
        for i in range(len(lines)):
            test[i] = test[i].lower()
    if params.count:
        k = 0
        for i in range(len(lines)):
            test[i] = test[i].rstrip()
            if params.invert:
                if sravnenie(params.pattern, test[i]) is False:
                    k += 1
            else:
                if sravnenie(params.pattern, test[i]) is True:
                    k += 1
        k = str(k)
        output_test(k, params)
    else:
        for i in range(len(lines)):
            test[i] = test[i].rstrip()
            if params.invert is True:
                if params.after_context >= 1:
                    if sravnenie(params.pattern, test[i]) is False:
                        for g in range(i, i + params.after_context + 1):
                            aaa.add(g)
                elif params.before_context >= 1:
                    if sravnenie(params.pattern, test[i]) is False:
                        for g in range(i - params.before_context, i + 1):
                            aaa.add(g)
                elif params.context >= 1:
                    if sravnenie(params.pattern, test[i]) is False:
                        for g in range(i - params.context, i + params.context + 1, 1):
                            aaa.add(g)
                else:
                    if sravnenie(params.pattern, test[i]) is False:
                        output_test(lines[i], params)
            else:
                if params.after_context >= 1:
                    if sravnenie(params.pattern, test[i]):
                        for g in range(i, i + params.after_context + 1):
                            aaa.add(g)
                elif params.before_context >= 1:
                    if sravnenie(params.pattern, test[i]):
                        for g in range(i - params.before_context, i + 1):
                            aaa.add(g)
                elif params.context >= 1:
                    if sravnenie(params.pattern, test[i]):
                        for g in range(i - params.context, i + params.context + 1, 1):
                            aaa.add(g)
                else:
                    if sravnenie(params.pattern, test[i]):
                        output_test(lines[i], params)
        for k in aaa:
            if 0 <= k < len(lines):
                output_test(lines[k], params)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v',
        action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i',
        action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(['?b'])
    grep(['baab', 'abbb', 'fc', 'AA'], params)


if __name__ == '__main__':
    main()
