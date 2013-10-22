# Copyright 2013 by comgen.pl. All rights reserved.

# This module is for handling hit lists.

from . import rbo

class Blasts:
    """Framework for pair-wise comparing of Blast Records.

    USAGE:
    >>> import blast
    >>> import rankings
    >>> evalue = 1e-05
    >>> bl1 = blast.read(open("blast1.out"), evalue)
    >>> bl2 = blast.read(open("blast2.out"), evalue)
    >>> pair = rankings.Blasts(bl1, bl2)

    """
    
    def __init__(self, b1, b2):
        """Create a framework object.

        Arguments:
        b1 - Blast Record (instance of BlastRecord object)
        b2 - same as above

        Attributes:
        ranks1   -  Blast hits converted into rankings
        ranks2   -  same as above
        overlap  -  Boolean logic; 
                    whether hit ids overlap between both blasts.
        """
        self.ranks1, self.ranks2 = __class__.create_ranks(b1.hits, b2.hits)
        self.overlap = __class__.isoverlap(b1.hits, b2.hits) 

    def isoverlap(hits1, hits2):
        """Return True if any of the subject_id in one Blast Record 
        are present in another Blast Record.
        """
        for hsp1 in hits1:
            for hsp2 in hits2:
                if hsp1.sid == hsp2.sid:
                    return True
        else:
            return False

    @staticmethod
    def _merge(hits1, hits2):
        """Merge two lists of blast hits into a single list 
        sorted by score. 

        This is private method, used by create_ranks method.

        """
        l = []
        for i,hits in enumerate([hits1,hits2]):
            for hsp in hits:
                # Mark each list hit by 'i' in order to know
                # the membership of hits.
                l.append([hsp.sid, hsp.bitscore, i])
        l.sort(key=lambda x: x[1], reverse=True)
        return l

    # This method is called on instance initialization.
    @staticmethod
    def create_ranks(hits1, hits2):
        """Convert blast hits into ranking lists.
        
        USAGE:
        >>> pair = rankings.Blasts(bl1, bl2)
        >>> hits1 = bl1.hits
        >>> hits2 = bl2.hits
        >>> ranks1, ranks2 = create_ranks(hits1, hits2))
        >>> print(ranks1)
        ... {1: ['sid1', 'sid2'], 2:[], 3:['sid3']}
        >>> print(ranks2)
        ... {1: [], 2:['sid3'], 3: []}

        """
        l = __class__._merge(hits1, hits2)
        prev_score = 'blah'
        i = 0
        rlists = ({},{}) 
        for hit, score, mark in l:
            if prev_score!=score:
                i+=1
                rlists[0][i] = []
                rlists[1][i] = []
            rlists[mark][i].append(hit)
            prev_score = score
        return rlists

    def RBO(self, p):
        """Calculate RBO metric between ranking lists (ranks1 & ranks2)
        based on a given P parameter (level of top-weightness of RBO).
        
        If hits do not overlap, RBO = 0.
        """
        return rbo.calc(self.ranks1, self.ranks2, p) if self.overlap else 0.0
