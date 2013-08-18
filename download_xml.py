import urllib2
import config as cfg
import string

def download_xml_data(filename, option='draftResults'):
    op1 = cfg.get_items_draftresults()
    op2 = cfg.get_items_players()
    op3 = cfg.get_items_league()
    op4 = cfg.get_items_projectedscores()
    op5 = cfg.get_items_nflschedule()
    dl_url = ''
    if op1 == option:
        dl_url = cfg.generate_draftresults_url()
    elif op2 == option:
        dl_url = cfg.generate_players_url()
    elif op3 == option:
        dl_url = cfg.generate_league_url()
    elif op4 == option:
        dl_url = cfg.generate_projectedscores_url()
    elif op5 == option:
        files = []
        for index in range(1, 18):
            try:
                urlp = urllib2.urlopen(cfg.generate_nflschedule_url(week=index))
                files.append(string.join(filename.split('.'), '_%s.' % index))
                fp = open(files[-1], 'w')
                fp.write(urlp.read())
                urlp.close()
                fp.close()
                return files
            except:
                return []
    if op5 != option:
        try:
            urlp = urllib2.urlopen(dl_url)
            fp = open(filename, 'w')
            fp.write(urlp.read())
            urlp.close()
            fp.close()
            return [filename]
       except:
           return []
    return []
    
