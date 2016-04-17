__author__ = 'xiao'

'''
Query Generator
Input:
    domain - domain name of the page
    link - URL of the page
    linktype - Link Type = [results | ads_main ...]
    oldrank - original rank returned by Search Engine
    title - title of the page
Output:
    Medical Rank (integer, the smaller the better)
Process:
    Implement new page rank algorithm and update the rank, for example:
    1. Looking up the authList
    2. considering the domain, e.g. edu, org
    3...
'''

# Sun updated 2016-04-06
if __name__ == '__main__':
    import expertise
    import medicalkeywords
else:
    from app import expertise
    from app import medicalkeywords

# import re

def rank(domain, link, linktype, oldrank, title):

    # Sun replace basestring with str due to Python version
    assert isinstance(domain, str)
    assert isinstance(oldrank, int)
    assert isinstance(link, str)

    #assert isinstance(linktype, bool)
    assert isinstance(linktype, str)     # Sun replaced 2016-04-04

    assert isinstance(title, str)

    newrank = oldrank

    # Sun removed 2016-04-04
    #linktype = False

    #
    # ToDo: Implement page rank algorithm
    #

    # Credible domains.
    # Sun fixed 2016-04-04
    #if domain in expertise.domains:
    if domain[-4:] in expertise.domains:
        print(domain + " site found")
        newrank -= 100

    # Advertisements.
    # Sun replaced 2016-04-04
    ## from
    '''
    for d in expertise.ads:
        if d in link:
            print d + " ad found"
            linktype = True
            newrank -= 50
    '''
    ## to
    if linktype == 'ads_main':      # Google indicates this link is an AD.
        newrank+=1000
    else:
        for d in expertise.ads:
            if d in link:           # We believe this link is an AD.
                print(d + " ad found")
                newrank += 500      # degrade the rank

    # Credible source matching.
    for s in expertise.sources_armughan:
        if s in link:
            print("Credible site confirmed by Doctor")
            newrank -= 200

    for s in expertise.sources_umich:
        if s in link:
            print("Credible site confirmed by University of Michigan")
            newrank -= 100

    for s in expertise.sources_jhu:
        if s in link:
            print("Credible site confirmed by Johns Hopkins University")
            newrank -= 100

    for s in expertise.sources_huffington:
        if s in link:
            print("Credible site confirmed by Huffington Post")
            newrank -= 50

    # Sun added 2016-04-06, search keywords in Medical Keywords List
    lowerTitle = title.lower()
    titleWeight = 0
    for wlists in medicalkeywords.keywordList:
        lstweight = 0
        for kword in wlists['list']:
            if kword in lowerTitle:
                lstweight += wlists['weight']
                if lstweight > wlists['maxweight']:
                    lstweight = wlists['maxweight']
                    break
        if lstweight > 0:
            print("Update MR with value (-%d) according to %s" % (lstweight, wlists['name']))
            titleWeight += lstweight
    newrank -= titleWeight

    print("Ranking value: Original MR = %d, optimized MR = %d" % (oldrank, newrank))
    return newrank

# Simple test code

if __name__ == '__main__':
    # Sun replaced 2016-04-04
    #rank('.gov', 'http://www.cdc.gov/', False, 0, 'Centers for Disease Control and Prevention')
    rank('.gov', 'http://www.cdc.gov/', 'result', 1000, 'Centers for Disease Control and Prevention')
    rank('.gov', 'http://www.cdc.gov/', 'ads_main', 1000, 'Centers for Disease Control and Prevention')

    # Sun added 2016-04-06
    rank('.com', 'http://www.datatellit.com/', 'result', 1000, 'gallstones diagnosed x-ray')    # match 2 keywords
    rank('.com', 'http://www.datatellit.com/', 'result', 1000, 'abdomen biliary biopsy enzyme gallstones diagnosed x-ray')    # match 6 keywords