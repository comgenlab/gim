import argparse
import sys
from . import blast
from . import rankings
from . import rbo


def main():

    if len(sys.argv) ==1:
      parser.print_usage()
      sys.stderr.write(sys.argv[0] + " Call with '-h' to get usage information.\n" )
      sys.exit(1)

    args = parser.parse_args()

    blasts = []
 
    for f in [args.blast1, args.blast2]:
        try:
            fh = open(f)
            try:
                b = blast.read(fh, args.evalue)
                blasts.append(b)
                fh.close()
            except:
                sys.stderr.write(sys.argv[0] + ": error: file {0} not in -m8/9 BLAST format\n".format(f))             
                sys.exit(1)
        except:
            sys.stderr.write(sys.argv[0] + ": error: file {0} does not exists\n".format(f))  
            sys.exit(1)



