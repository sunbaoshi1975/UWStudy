#!env/bin/python3.4

import sys
import json
from GoogleScraper import scrape_with_config, GoogleSearchError
from GoogleScraper.output_converter import row2dict

if __name__ != '__main__':
    from app import pageranker

# very basic search
def basic_search(query, engines, pages):
    # See in the config.cfg file for possible values
    config = {
        'use_own_ip': True,
        'keyword': query,
        'search_engines': [engines],
        'num_pages_for_keyword': pages,
        'scrape_method': 'http',
        'loglevel': 'WARN',
        'print_results': 'summarize',
        'do_caching': False
    }

    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

    # let's inspect what we got
    '''
    for serp in search.serps:
        #print(serp)
        print(serp.status)
        print(serp.scrape_method)
        print(serp.page_number)
        print(serp.requested_at)
        print(serp.num_results)
        for link in serp.links:
            print(link)
    '''
    return search

# simulating a image search for all search engines that support image search
# then download all found images :)
def image_search(query, engines, pages):
    target_directory = 'images/'

    # See in the config.cfg file for possible values
    config = {
        'use_own_ip': True,
        'keyword': query,
        'search_engines': [engines],
        'search_type': 'image',
        'num_pages_for_keyword': pages,
        'scrape_method': 'http',
        'do_caching': False
    }

    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

    image_urls = []
    search = search.query(ScraperSearch).all()[-1]

    for serp in search.serps:
        image_urls.extend(
            [link.link for link in serp.links]
        )

    print('[i] Going to scrape {num} images and saving them in "{dir}"'.format(
        num=len(image_urls),
        dir=target_directory
    ))

    import threading,requests, os, urllib

    class FetchResource(threading.Thread):
        """Grabs a web resource and stores it in the target directory"""
        def __init__(self, target, urls):
            super().__init__()
            self.target = target
            self.urls = urls

        def run(self):
            for url in self.urls:
                url = urllib.parse.unquote(url)
                with open(os.path.join(self.target, url.split('/')[-1]), 'wb') as f:
                    try:
                        content = requests.get(url).content
                        f.write(content)
                    except Exception as e:
                        pass
                    print('[+] Fetched {}'.format(url))

    # make a directory for the results
    try:
        os.mkdir(target_directory)
    except FileExistsError:
        pass

    # fire up 100 threads to get the images
    num_threads = 100

    threads = [FetchResource('images/', []) for i in range(num_threads)]

    while image_urls:
        for t in threads:
            try:
                t.urls.append(image_urls.pop())
            except IndexError as e:
                break

    threads = [t for t in threads if t.urls]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

'''
Execute query by calling GoogleScraper.
Output is returned in GS Object.
'''
def query(query, method='basic', engines='Google', pages=1):
    if method == 'image':
        results = image_search(query, engines, pages)
    else:
        results = basic_search(query, engines, pages)

    return results

'''
Convert GS Object to JSON string.
'''
def Convert2JSON(gsobj, skinny = True):
    # Return JSON
    if skinny:
        results = ''
    else:
        results = '['

    for serp in gsobj.serps:
        data = row2dict(serp)
        data['results'] = []
        for link in serp.links:
            data['results'].append(row2dict(link))
        if skinny:
            recordJSON = json.dumps(data['results'])
            # Remove '[' and ']' at each ends
            if recordJSON.strip() != '':
                if recordJSON.startswith('['):
                    recordJSON = recordJSON[1:-1]
                if results != '':
                    results += ', '
                results += recordJSON
        else:
            recordJSON = json.dumps(data, indent=2, sort_keys=True)
            if recordJSON.strip() != '':
                if results != '[':
                    results += ', '
                results += recordJSON

    if not skinny:
        results += ']'

    return results

'''
Convert GS Object to Array Object.
'''
def Convert2Dictionary(gsobj):
    # Dictionary
    results = []

    for serp in gsobj.serps:
        for link in serp.links:
            results.append(row2dict(link))

    return results

'''
Re-ranking pages
'''
def PageRanking(gsobj):

    count = 0
    for serp in gsobj.serps:
        if not serp.no_results:
            count += int(serp.num_results)
            for link in serp.links:
                # Re-ranking
                link.rank = pageranker.rank(link.domain, link.link, link.link_type, link.rank, link.title)

    return [count, gsobj]

'''
Re-ranking pages and return Array
'''
def PageRankingExpress(gsobj):
    # Array
    results = []
    baserank = 1000

    for serp in gsobj.serps:
        if not serp.no_results:
            for link in serp.links:
                # Re-ranking
                baserank+=1
                if link.link_type != 'ads_main':
                    link.rank = pageranker.rank(link.domain, link.link, link.link_type, baserank, link.title)
                    results.append(row2dict(link))
                    # ToDo: We may also need to filter and reorder the list
                    # SBS: let's do it in client side by using AngularJS

    return results

### MAIN FUNCTION ###
if __name__ == '__main__':
    import pageranker

    usage = 'Usage: {} [query] [basic|image] [skinny=0|1]'.format(sys.argv[0])
    if len(sys.argv) != 4:
        print(usage)
    else:
        query = sys.argv[1]
        method = sys.argv[2]
        skinny = (sys.argv[3] == '1')
        if method == 'basic':
            result = basic_search(query, 'google', 1)
            result = PageRanking(result)
            print('>>>>>>>>>>>>> Got Records: %d <<<<<<<<<<<<<<<' % result[0])
            print(Convert2JSON(result[1], skinny))
        elif method == 'image':
            result = image_search(query, 'google', 1)
            print('>>>>>>>>>>>>>Got Result:<<<<<<<<<<<<<<<')
            print(Convert2JSON(result))
        else:
            print(usage)