import bs4, requests


MODS_URL = "https://search.mcbbs.net/forum.php?mod=forumdisplay&fid=45&sortall=1&sortall=1&filter=sortall&page={pagenum}" 
# www.mcbbs.net 403, but search.mcbbs.net seems to be the same site without 403
def fetch_modlist():
    for i in range(1, 101):
        r = requests.get(MODS_URL.format(i))
        r.raise_for_status()
        # beautifulsoup filter: table#threadlisttableid > th.common
        
        
        yield r # use a generator to provide more and more pages when required