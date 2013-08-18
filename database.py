import MySQLdb as mysql
import copy
import string

__POSITIONS = ['Def', 'PK', 'QB', 'RB', 'TE', 'WR']

class db_info:
    def __init__(self, host, dbname, user, passwd):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.passwd = passwd
    
    def g_host(self): return copy.copy(self.host)
    def g_dbname(self): return copy.copy(self.dbname)
    def g_user(self): return copy.copy(self.user)
    def g_passwd(self): return copy.copy(self.passwd)
    
    def s_host(host): self.host = host
    def s_dbname(dbname): self.dbname = dbname
    def s_user(user): self.user = user
    def s_passwd(passwd): self.passwd = passwd

def db_connect(info):
    db = mysql.connect(host=info.g_host(), user=info.g_user(), passwd=info.g_passwd(), db=info.g_dbname())
    return (db, db.cursor())

def db_close(cursor):
    conn.close()

def db_query(info, query, **kwargs):
    db = db_connect(info)
    db[1].execute(query, kwargs)
    db[0].commit()
    return db[1].fetchall()

def db_insert(info, query, **kwargs):
    db_query(info, query, **kwargs)
    return None

def db_update(info, query, **kwargs):
    db_query(info, query, **kwargs)
    return None

def db_delete(info, query, **kwargs):
    db_query(info, query, **kwargs)
    return None

def db_select(info, query, **kwargs):
    results = db_query(info, query, **kwargs)
    return results

def db_insert_team(info, id, name, abbrev, bye_week):
    return db_insert(info, """
      INSERT INTO Team (id, name, abbrev, bye_week)
      VALUES (%(id)s, %(name)s, %(abbrev)s, %(bye_week)s)""", id=id, name=name, abbrev=abbrev, bye_week=bye_week)

def db_update_team(info, id, **kwargs):
    query = """UPDATE Team SET """
    values = []
    if kwargs.has_key('name'):
        if kwargs['name'] != None: values.append("""name=%(name)s""")
    if kwargs.has_key('abbrev'):
        if kwargs['abbrev'] != None: values.append("""abbrev=%(abbrev)s""")
    if kwargs.has_key('bye_week'):
        if kwargs['bye_week'] != None: values.append("""bye_week=%(bye_week)s""")
    query += string.join(values, ', ')
    query += """ WHERE id=%(id)s"""
    if len(values) > 0 and id != None:
        return db_update(info, query, id=id, **kwargs)
    else:
        return None

def db_delete_team(info, id):
    return db_delete(info, """DELETE FROM Team WHERE id=%(id)s""", id=id)

def db_insert_position(info, id, pos):
    return db_delete(info, """INSERT INTO Position VALUES (%(id)s, %(pos)s)""", id=id, pos=pos)

def db_update_position(info, id, pos):
    return db_update(info, """UPDATE Position SET pos=%(pos)s WHERE id=%(id)s""", id=id, pos=pos)

def db_delete_position(info, id):
    return db_delete(info, """DELETE FROM Position WHERE id=%(id)s""", id=id)

def db_insert_player(info, id, name, Position_id, Team_id, injury, injury_detail, projected_score, isrookie):
    return db_insert(info, """
        INSERT INTO Player (id, name, Position_id, Team_id, injury, injury_detail, projected_score, isrookie)
        VALUES (%(id)s, %(name)s, %(Position_id)s, %(Team_id)s, %(injury)s, %(injury_detail)s, %(projected_score)s, %(isrookie)s)""",
          id=id, name=name, Position_id=Position_id, Team_id=Team_id, injury=injury, injury_detail=injury_detail, projected_score=projected_score, isrookie=isrookie)

def db_update_player(info, id, **kwargs):
    query = """UPDATE Player SET """
    values = []
    for key in kwargs.keys():
        values.append(str(key)+"""=%("""+key+""")s""")
    query += string.join(values, ', ')
    query += """ WHERE id=%(id)s"""
    if len(values) > 0 and id != None:
        return db_update(info, query, id=id, **kwargs)
    else:
        return None

def db_delete_player(info, id):
    return db_delete(info, """DELETE FROM Player WHERE id=%(id)s""", id=id)

def db_insert_franchise(info, id, name):
    return db_insert(info, """INSERT INTO Franchise (id, name) VALUES (%(id)s, %(name)s)""", id=id, name=name)

def db_update_franchise(info, id, name):
    return db_update(info, """UPDATE Franchise SET name=%(name)s WHERE id=%(id)s""", id=id, name=name)

def db_delete_franchise(info, id):
    return db_delete(info, """DELETE FROM Franchise WHERE id=%(id)s""", id=id)

def db_insert_draft(info, round, pick, Franchise_id, Player_id):
    return db_insert(info, """
      INSERT INTO Draft (round, pick, Franchise_id, Player_id)
      VALUES (%(round)s, %(pick)s, %(Franchise_id)s, %(Player_id)s)""", pick=pick, round=round, Franchise_id=Franchise_id, Player_id=Player_id)

def db_update_draft(info, round, pick, **kwargs):
    query = """UPDATE Draft SET """
    values = []
    for key in kwargs.keys():
        values.append(str(key)+"""=%("""+key+""")s""")
    query += string.join(values, ', ')
    query += """ WHERE round=%(round)s AND pick=%(pick)s"""
    if len(values) > 0 and id != None:
        return db_update(info, query, round=round, pick=pick, **kwargs)
    else:
        return None

def db_delete_draft(info, round, pick):
    return db_delete(info, """DELETE FROM Draft WHERE round=%(round)s AND pick=%(pick)s""", round=round, pick=pick)

def db_select_available_players(info, **kwargs):
    values = []
    query = """      SELECT p.id, p.name, pos.pos, t.abbrev, p.injury, p.injury_detail, p.projected_score, p.isrookie
      FROM (Player p INNER JOIN Team t ON p.Team_id=t.id) INNER JOIN Position pos ON p.Position_id=pos.id
      WHERE """
    for key in kwargs.keys():
        if key == 'abbrev':
            values.append("""t.id IN (SELECT id FROM Team WHERE abbrev=%(abbrev)s)""")
        elif key == 'pos':
            values.append("""pos.id IN (SELECT id FROM Position WHERE pos=%(pos)s)""")
    values.append("""p.id NOT IN (SELECT Player_id FROM Draft)""")
    query += string.join(values, "\n        AND ")
    query += """\n      ORDER BY p.projected_score DESC, p.name ASC"""
    results = db_select(info, query, **kwargs)
    results_dict = []
    for each in results:
        results_dict.append({'ID':each[0], 'Name':each[1], 'Position':each[2], 'Team':each[3], 'Injury':each[4], 'Detail':each[5], 'Score':each[6], 'Rookie':each[7]})
    return results_dict

def db_select_franchise_players(info, **kwargs):
    values = []
    query = """
      SELECT p.id, p.name, pos.pos, t.abbrev, p.injury, p.isrookie
      FROM (Player p INNER JOIN Team t ON p.Team_id=t.id) INNER JOIN Position pos ON p.Position_id=pos.id
      WHERE p.id IN (SELECT Player_id FROM Draft WHERE Franchise_id=%(Franchise_id)s)
      ORDER BY p.projected_score DESC, p.name ASC"""
    results = db_select(info, query, **kwargs)
    results_dict = []
    for each in results:
        results_dict.append({'ID':each[0], 'Name':each[1], 'Position':each[2], 'Team':each[3], 'Injury':each[4], 'Rookie':each[5]})
    return results_dict

if __name__ == '__main__':
    info = db_info('localhost', 'asxffl-draft', 'root', 'fanevviena1')
    
    db_delete_draft(info, 1, 2)
    db_delete_draft(info, 1, 1)
    db_delete_franchise(info, 1)
    db_delete_player(info, 12)
    db_delete_player(info, 11)
    db_delete_player(info, 10)
    db_delete_player(info, 9)
    db_delete_player(info, 8)
    db_delete_player(info, 7)
    db_delete_player(info, 6)
    db_delete_player(info, 5)
    db_delete_player(info, 4)
    db_delete_player(info, 3)
    db_delete_player(info, 2)
    db_delete_player(info, 1)
    db_delete_position(info, 6)
    db_delete_position(info, 5)
    db_delete_position(info, 4)
    db_delete_position(info, 3)
    db_delete_position(info, 2)
    db_delete_position(info, 1)
    db_delete_team(info, 2)
    db_delete_team(info, 1)
    
    db_insert_team(info, 1, 'Cowboys, Dallas', 'DAL', 8)
    db_insert_team(info, 2, 'Colts, Indianapolis', 'IND', 9)
    
    db_insert_position(info, 1, 'Def')
    db_insert_position(info, 2, 'PK')
    db_insert_position(info, 3, 'QB')
    db_insert_position(info, 4, 'RB')
    db_insert_position(info, 5, 'TE')
    db_insert_position(info, 6, 'WR')
    
    db_insert_player(info, 1, 'a, b', 1, 1, '', '', 1.0, False)
    db_insert_player(info, 2, 'b, c', 2, 1, '', '', 1.2, False)
    db_insert_player(info, 3, 'c, d', 3, 1, '', '', 1.3, False)
    db_insert_player(info, 4, 'd, e', 4, 1, '', '', 1.4, False)
    db_insert_player(info, 5, 'e, f', 5, 1, '', '', 1.5, False)
    db_insert_player(info, 6, 'f, g', 6, 1, '', '', 1.6, False)
    
    db_insert_player(info, 7, 'b, b', 1, 1, '', '', 1.7, False)
    db_insert_player(info, 8, 'c, c', 2, 1, '', '', 1.8, False)
    db_insert_player(info, 9, 'd, d', 3, 1, '', '', 1.9, False)
    db_insert_player(info, 10, 'e, e', 4, 1, '', '', 2.0, False)
    db_insert_player(info, 11, 'f, f', 5, 1, '', '', 2.1, False)
    db_insert_player(info, 12, 'g, g', 6, 1, '', '', 2.2, False)
    
    db_insert_franchise(info, 1, 'Adventure Seekers')
    
    db_insert_draft(info, 1, 1, 1, 1)
    db_insert_draft(info, 1, 2, 1, 11)
    
    #select
    print db_select_available_players(info)
    print db_select_available_players(info, abbrev='DAL')
    print db_select_available_players(info, pos='RB')
    print db_select_available_players(info, abbrev='DAL', pos='WR')
    
    print db_select_franchise_players(info, Franchise_id=1)
    
    db_delete_draft(info, 1, 2)
    db_delete_draft(info, 1, 1)
    db_delete_franchise(info, 1)
    db_delete_player(info, 12)
    db_delete_player(info, 11)
    db_delete_player(info, 10)
    db_delete_player(info, 9)
    db_delete_player(info, 8)
    db_delete_player(info, 7)
    db_delete_player(info, 6)
    db_delete_player(info, 5)
    db_delete_player(info, 4)
    db_delete_player(info, 3)
    db_delete_player(info, 2)
    db_delete_player(info, 1)
    db_delete_position(info, 6)
    db_delete_position(info, 5)
    db_delete_position(info, 4)
    db_delete_position(info, 3)
    db_delete_position(info, 2)
    db_delete_position(info, 1)
    db_delete_team(info, 2)
    db_delete_team(info, 1)
