import sys
import argparse
from libs import validator
from libs import blast
from libs import rankings
from libs import rbo


description = "Calculate RBO metrics between two BLAST tabular outputs."
parser = argparse.ArgumentParser(description=description)
parser.add_argument('blast1', help="blast output (-outfmt 6, -m8)")
parser.add_argument('blast2', help="blast output (-outfmt 6, -m8)")
parser.add_argument('-e','-evalue','--evalue', dest='evalue', type=float,
  default='1e-05', help='E-value cutoff [default=%(default)s]')
parser.add_argument('-p','--p', dest='p', default='0.95', type=float,
  help='parameter P of RBO (0 <= p < 1) [default=%(default)s]')

args = parser.parse_args()



b1, b2 = validator.validate_args(sys.argv, args)
c = rankings.Blasts(b1, b2)
print(c.RBO(args.p))

