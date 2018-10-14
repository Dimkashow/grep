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
    next_print = 0
    buffer = []
    buffer_count = max(params.context,params.before_context)

    for line in lines:
        if params.count:
            line = line.rstrip()
            if comparison(params,line):
                kol += 1
        else:
            line = line.rstrip()
            if comparison(params,line):
                if params.after_context or params.context:
                    next_print = max(params.after_context,params.context)
                if params.before_context or params.context:
                    buffer.reverse()
                    for out in buffer:
                        if out != 0:
                            output_test(out,params,lines)
                    buffer.clear()
                output_test(line,params,lines)

            else:
                if next_print != 0:
                    output_test(line,params,lines)
                    next_print -= 1
                    line = 0
                if buffer_count != 0:
                    if len(buffer) >= buffer_count:
                        buffer.insert(0,line)
                        buffer.pop()
                    else:
                        buffer.insert(0,line)
    if params.count:
        kol = str(kol)
        output_test(kol,params,lines)

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
