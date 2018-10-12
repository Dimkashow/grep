import argparse
import sys
import re


def comparison(params, st2):
    st1 = params.pattern
    if params.ignore_case:
        st1 = st1.lower()
        st2 = st2.lower()
    st1 = st1.replace('*','\w*')
    st1 = st1.replace('?','.')
    if st1 in st2:
        res = True
    else:
        if st1.replace('\w*','')=="":
            res = True
        else:
            if st1.replace('.','')=="":
                if len(st1) <= len(st2):
                    res = True
                else:
                    res = False
            else:
                if re.search(st1,st2) is None:
                    res = False
                else:
                    res = True
    if params.invert:
        if res:
            return False
        else:
            return True
    else:
        return res


def output_test(line,params,lines):
    if params.line_number is True:
        nomer = lines.index(line) + 1
        nomer = str(nomer)
        if comparison(params,line):
            result = nomer + ':' + line
        else:
            result = nomer + '-' + line
        output(result)
    else:
        output(line)


def output(line):
    print(line)


def grep(lines,params):
    kol = 0
    lines_set = set()
    for line in lines:
        if params.count:
            line = line.rstrip()
            if params.invert:
                if comparison(params,line) is False:
                    kol += 1
            else:
                if comparison(params,line) is True:
                    kol += 1
        else:
            line = line.rstrip()
            i = lines.index(line)
            if params.after_context >= 1:
                if comparison(params,line):
                    for g in range(i,i + params.after_context + 1):
                        lines_set.add(g)
            elif params.before_context >= 1:
                if comparison(params,line):
                    for g in range(i - params.before_context,i + 1):
                        lines_set.add(g)
            elif params.context >= 1:
                if comparison(params,line):
                    for g in range(i - params.context,i + params.context + 1,1):
                        lines_set.add(g)
            else:
                if comparison(params,line):
                    output_test(lines[i],params,lines)
    if params.count:
        kol = str(kol)
        output_test(kol,params,lines)
    if len(lines_set)!= 0:
        for kol in lines_set:
            if 0 <= kol < len(lines):
                output_test(lines[kol],params,lines)


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
    parser.add_argument('pattern',action="store",help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(),params)


if __name__=='__main__':
    main()
