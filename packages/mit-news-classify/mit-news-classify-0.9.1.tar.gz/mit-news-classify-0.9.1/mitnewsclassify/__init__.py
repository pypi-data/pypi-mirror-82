"""
Created Wednesday August 26 2020 21:17 +0700

@author: arunwpm
"""
def lite(txt):
    from mitnewsclassify import ensemble
    return ensemble.gettags(txt)

def medium(txt):
    from mitnewsclassify import trisemble
    return trisemble.gettags(txt)

def badass(txt):
    from mitnewsclassify import quadsemble
    return quadsemble.gettags(txt)