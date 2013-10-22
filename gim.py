import argparse
from libs import blast
from libs import rankings

parser = argparse.ArgumentParser(
             description='Calculate RBO between BLAST output lists.')
parser.add_argument('blast1', help="blast output (-outfmt 6, -m8)")
parser.add_argument('blast2', help="blast output (-outfmt 6, -m8)")
parser.add_argument('-e','-evalue','--evalue', dest='evalue', type=float,
           default='1e-05', help='E-value cutoff [default=%(default)s]')
parser.add_argument('-p','--p', dest='p', default='0.95', type=float,
            help='parameter P of RBO (0 <= p < 1) [default=%(default)s]')

args = parser.parse_args()


b1 = blast.read(open(args.blast1), args.evalue)
b2 = blast.read(open(args.blast2), args.evalue)
c = rankings.Blasts(b1, b2)

print(c.RBO(args.p))
