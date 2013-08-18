import ConfigParser as cfg
import xml.dom.minidom as xml
import urllib as url

__CONFIG_FILE = "config.ini"

def read_config():
    global __CONFIG_FILE
    cfgf = cfg.ConfigParser()
    cfgf.read(__CONFIG_FILE)
    return cfgf

def write_config(config):
    global __CONFIG_FILE
    with open(__CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)

def set_league_id(_id=-1):
    cfgf = read_config(); cfgf.set('league', 'id', str(_id)); write_config(cfgf)

def get_league_id():
    cfgf = read_config(); return cfgf.getint('league', 'id')

def set_database_user(user):
    cfgf = read_config(); cfgf.set('database', 'user', str(user)); write_config(cfgf)

def get_database_user():
    cfgf = read_config(); return cfgf.get('database', 'user')

def set_database_password(password):
    cfgf = read_config(); cfgf.set('database', 'password', str(password)); write_config(cfgf)

def get_database_password():
    cfgf = read_config(); return cfgf.get('database', 'password')

def set_database_dbname(dbname):
    cfgf = read_config(); cfgf.set('database', 'dbname', str(dbname)); write_config(cfgf)

def get_database_dbname():
    cfgf = read_config(); return cfgf.get('database', 'dbname')

def set_database_host(host):
    cfgf = read_config(); cfgf.set('database', 'host', str(host)); write_config(cfgf)

def get_database_host():
    cfgf = read_config(); return cfgf.get('database', 'host')

def set_items_draftresults(item):
    cfgf = read_config(); cfgf.set('items', 'draftresults', str(item)); write_config(cfgf)

def get_items_draftresults():
    cfgf = read_config(); return cfgf.get('items', 'draftresults')

def set_items_players(item):
    cfgf = read_config(); cfgf.set('items', 'players', str(item)); write_config(cfgf)

def get_items_players():
    cfgf = read_config(); return cfgf.get('items', 'players')

def set_items_league(item):
    cfgf = read_config(); cfgf.set('items', 'league', str(item)); write_config(cfgf)

def get_items_league():
    cfgf = read_config(); return cfgf.get('items', 'league')

def set_items_projectedscores(item):
    cfgf = read_config(); cfgf.set('items', 'projectedscores', item); write_config(cfgf)

def get_items_projectedscores():
    cfgf = read_config(); return cfgf.get('items', 'projectedscores')

def set_items_nflschedule(item):
    cfgf = read_config(); cfgf.set('items', 'nflschedule', item); write_config(cfgf)

def get_items_nflschedule():
    cfgf = read_config(); return cfgf.get('items', 'nflschedule')

def set_draft_frequency(item):
    cfgf = read_config(); cfgf.set('draft', 'frequency', str(item)); write_config(cfgf)

def get_draft_frequency():
    cfgf = read_config(); return cfgf.getint('draft', 'frequency')

def generate_data_url(item_type="", league_id=0, week=-1):
    if week == -1:
        return "football19.myfantasyleague.com/2013/export?TYPE=%s&L=%s&W=&JSON=0" % (item_type, league_id)
    else:
        return "football19.myfantasyleague.com/2013/export?TYPE=%s&L=%s&W=%s&JSON=0" % (item_type, league_id, week)

def generate_draftresults_url(week=-1):
    cfgf = read_config()
    return generate_data_url(get_items_draftresults(), get_league_id(), week)

def generate_players_url(week=-1):
    cfgf = read_config()
    return generate_data_url(get_items_players(), get_league_id(), week)

def generate_league_url(week=-1):
    cfgf = read_config()
    return generate_data_url(get_items_league(), get_league_id(), week)

def generate_projectedscores_url(week=-1):
    cfgf = read_config()
    return generate_data_url(get_items_projectedscores(), get_league_id(), week)

def generate_nflschedule_url(week=-1):
    cfgf = read_config()
    return generate_data_url(get_items_nflschedule(), get_league_id(), week)

if __name__ == '__main__':
    print generate_draftresults_url(1)
    print generate_players_url(1)
    print generate_league_url(1)
    print generate_projectedscores_url(1)
    print generate_nflschedule_url(1)
