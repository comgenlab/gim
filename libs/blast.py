# Copyright 2013 by comgen.pl. All rights reserved.

# This module is for handling BLAST output lists (in -outfmt 6/ -m8 format).


from itertools import groupby
import re

class Hsp:
    """Store information about single HSP in an alignment hit. 

    Members: 
    qid       Query Id
    sid       Subject Id
    pident    Percentage of identical matches
    length    Alignment length
    mismatch  Number of mismatches
    gaps      Total number of gaps
    qstart    Start of alignment in query
    qend      End of alignment in query
    sstart    Start of alignment in subject
    send      End of alignment in subject
    evalue    Expect value
    bitscore  Bit score

    USAGE:
    >>> line = 'qid\tsid\t83.99\t37\t14\t15\t1\t147\t1\t149\t0.0\t219\n'
    >>> hsp = Hsp(line)
    >>> hsp.bitscore
    219
    >>> hsp.pident
    83.99

    """

    def __init__(self,entry):
        bt_fields = entry.split('\t')
        self.qid = bt_fields[0]
        self.sid = bt_fields[1]
        self.pident = float(bt_fields[2])
        self.length = int(bt_fields[3])
        self.mismatch = int(bt_fields[4])
        self.gaps = int(bt_fields[5])
        self.qstart = int(bt_fields[6])
        self.qend = int(bt_fields[7])
        self.sstart = int(bt_fields[8])
        self.send = int(bt_fields[9])
        self.evalue = float(bt_fields[10])
        self.bitscore = float(bt_fields[11])


class BlastRecord:
    """Object representing a Blast Record. 

    Arguments: 
    qid       - Query sequence id
    hits      - Blast hits

    """

    def __init__(self, qid=None, hits=None):
        """Initialize Blast Record instance"""
        self.qid = qid
        self.hits = hits

    def evalue_cutoff(self, evalue):
        """Filter HSPs by given e-value."""
        l = []
        for hsp in self.hits:
            if hsp.evalue <= evalue:
                l.append(hsp)
        self.hits = l



#This is a generator function!
def parse(handle, eval_thresh=10):
     """Generator function to iterate over Blast records.
     
     Arguments: 
     handle      - input file handle containg Blast tabular 
                   outputs (-outfmt 6, -m8).
     eval_thresh - E-value cutoff for Blast results.

     """
     for qid, hsps in groupby(handle, lambda l: l.split()[0]):
         hits = []
         prev_sid = False
         for line in hsps:
             hsp = Hsp(line)
             if hsp.evalue<=eval_thresh:
                 if prev_sid != hsp.sid:
                     hits.append(hsp)
             prev_sid = hsp.sid
         yield BlastRecord(qid=qid, hits=hits)


def read(handle,eval_thresh=10):
     """
     Read only one Blast record.
 
     USAGE:
     >>> import Blast
     >>> record = Blast.read(open('output.txt'))

     If the handle contains no records an exception is raised.
     If the handle contains multiple records, the first one is read.

     Use the Blast.parse(handle) function if you want
     to read multiple records from the handle.

     """
     iterator = parse(handle,eval_thresh)
     try:
         first = next(iterator)
     except StopIteration:
         first = None
     return first
