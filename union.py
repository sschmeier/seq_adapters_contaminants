#!/usr/bin/env python
"""
NAME: union.py
=========

DESCRIPTION
===========

INSTALLATION
============

USAGE
=====

VERSION HISTORY
===============

0.0.1    2018    Initial version.

LICENCE
=======
2018, copyright Sebastian Schmeier
s.schmeier@gmail.com // https://www.sschmeier.com

template version: 2.0 (2018/12/19)
"""
import sys
import os
import argparse
import csv
import gzip
import bz2
import zipfile
import time
import collections

from Bio import SeqIO

__version__ = '0.0.1'
__date__ = '2018'
__email__ = 's.schmeier@gmail.com'
__author__ = 'Sebastian Schmeier'

# For color handling on the shell
try:
    from colorama import init, Fore
    # INIT color
    # Initialise colours for multi-platform support.
    init()
    reset = Fore.RESET
    colors = {'success': Fore.GREEN,
              'error': Fore.RED,
              'warning': Fore.YELLOW,
              'info': ''}
except ImportError:
    sys.stderr.write('colorama lib desirable. ' +
                     'Install with "conda install colorama".\n\n')
    reset = ''
    colors = {'success': '', 'error': '', 'warning': '', 'info': ''}


def alert(atype, text, log, repeat=False):
    if repeat:
        textout = '{} [{}] {}\r'.format(time.strftime('%Y%m%d-%H:%M:%S'),
                                        atype.rjust(7),
                                        text)
    else:
        textout = '{} [{}] {}\n'.format(time.strftime('%Y%m%d-%H:%M:%S'),
                                        atype.rjust(7),
                                        text)

    log.write('{}{}{}'.format(colors[atype], textout, reset))
    if atype == 'error':
        sys.exit()


def success(text, log=sys.stderr):
    alert('success', text, log)


def error(text, log=sys.stderr):
    alert('error', text, log)


def warning(text, log=sys.stderr):
    alert('warning', text, log)


def info(text, log=sys.stderr, repeat=False):
    alert('info', text, log)


def parse_cmdline():
    """ Parse command-line args. """
    # parse cmd-line ----------------------------------------------------------
    description = 'Read all fasta adapter files. Make a file with unique sequences. Id will be the first occurrence.'
    version = 'version {}, date {}'.format(__version__, __date__)
    epilog = 'Copyright {} ({})'.format(__author__, __email__)

    parser = argparse.ArgumentParser(description=description, epilog=epilog)

    parser.add_argument('--version',
                        action='version',
                        version='{}'.format(version))

    parser.add_argument(
        'files',
        metavar='FILE',
        nargs="+",
        help='Delimited file.')
    parser.add_argument('-o',
                        '--out',
                        metavar='STRING',
                        dest='outfile_name',
                        default=None,
                        help='Out-file. [default: "stdout"]')

    # if no arguments supplied print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args, parser


def load_file(filename):
    """ LOADING FILES """
    if filename in ['-', 'stdin']:
        filehandle = sys.stdin
    elif filename.split('.')[-1] == 'gz':
        filehandle = gzip.open(filename, 'rt')
    elif filename.split('.')[-1] == 'bz2':
        filehandle = bz2.open(filename, 'rt')
    elif filename.split('.')[-1] == 'zip':
        filehandle = zipfile.ZipFile(filename)
    else:
        filehandle = open(filename)
    return filehandle


def main():
    """ The main funtion. """
    args, parser = parse_cmdline()

   
    # create outfile object
    if not args.outfile_name:
        outfileobj = sys.stdout
    elif args.outfile_name in ['-', 'stdout']:
        outfileobj = sys.stdout
    elif args.outfile_name.split('.')[-1] == 'gz':
        outfileobj = gzip.open(args.outfile_name, 'wt')
    else:
        outfileobj = open(args.outfile_name, 'w')

    d = collections.OrderedDict()
    for file in args.files:
        
        try:
            iterator = SeqIO.parse(file, "fasta")
        except IOError:
            error('Could not load file "{}". EXIT.'.format(file))

        for record in iterator:
            seq = str(record.seq)
            id = record.id

            if seq not in d:
                d[seq] = id
                
    #d2 = {y:x for x,y in d.items()}
    #ids = list(d2.keys())
    #ids.sort()
    
    # For printing to stdout
    # SIGPIPE is throwing exception when piping output to other tools
    # like head. => http://docs.python.org/library/signal.html
    # use a try - except clause to handle
    try:
        for seq,id in d.items():
            outfileobj.write('>{}\n{}\n'.format(id, seq))
        # flush output here to force SIGPIPE to be triggered
        # while inside this try block.
        sys.stdout.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shut-down
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE

    # ------------------------------------------------------
    outfileobj.close()
    return


if __name__ == '__main__':
    sys.exit(main())
