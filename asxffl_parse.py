import xml.dom.minidom as xml

def draftResults_parse(filename):
    dom = xml.parse(filename)
    picks = dom.getElementsByTagName('draftResults')[0].getElementsByTagName('draftUnit')[0].getElementsByTagName('draftPick')
    results = []
    for pick in picks:
        rnd = pick.getAttribute('round').lstrip('0')
        pck = pick.getAttribute('pick').lstrip('0')
        frn = pick.getAttribute('franchise').lstrip('0')
        plr = pick.getAttribute('player').lstrip('0')
        if plr != '' and plr != ' ':
            results.append([int(rnd), int(pck), int(frn), int(plr)])
    return results

def player_parse(filename):
    dom = xml.parse(filename)
    players = dom.getElementsByTagName('players')[0].getElementsByTagName('player')
    results = []
    for p in players:
        _id = p.getAttribute('id').lstrip('0')
        name = p.getAttribute('name')
        pos = p.getAttribute('position')
        team = p.getAttribute('team').lstrip('0')
        try:
            isrookie = p.getAttribute('status') == 'R'
        except:
            isrookie = False
        if pos in ['Def', 'PK', 'QB', 'RB', 'TE', 'WR']:
            results.append([int(_id), name, pos, team, isrookie])
    return results

def league_parse(filename):
    dom = xml.parse(filename)
    league = dom.getElementsByTagName('league')[0]
    franchise = league.getElementsByTagName('franchises')[0].getElementsByTagName('franchise')
    results = []
    for f in franchise:
        name = f.getAttribute('name')
        _id = f.getAttribute('id').lstrip('0')
        results.append([int(_id), name])
    return results

def projectedScores_parse(filename):
    dom = xml.parse(filename)
    projected = dom.getElementsByTagName('projectedScores')[0].getElementsByTagName('playerScore')
    results = []
    for score in projected:
        _id = score.getAttribute('id').lstrip('0')
        score = score.getAttribute('score').strip('0')
        if _id != '' and _id != ' ':
            results.append([int(_id), float(score)])
    return results

def injuries_parse(filename):
    dom = xml.parse(filename)
    injuries = dom.getElementsByTagName('injuries')[0].getElementsByTagName('injury')
    results = []
    for injury in injuries:
        _id = injury.getAttribute('id').lstrip('0')
        status = injury.getAttribute('status')
        detail = injury.getAttribute('details')
        results.append([int(_id), status, detail])
    return results

def nflSchedule_parse(filename):
    dom = xml.parse(filename)
    nfl = dom.getElementsByTagName('nflSchedule')[0]
    week = int(nfl.getAttribute('week').lstrip('0'))
    matches = nfl.getElementsByTagName('matchup')
    teams = []
    for each in matches:
        for team in each.getElementsByTagName('team'):
            teams.append(team.getAttribute('id'))
    teams.sort()
    return (week, teams)

if __name__ == '__main__':
    results = draftResults_parse('draftResults_test.xml')
    if len(results) > 0: print 'Test 1: Success'
    else: print 'Test 1: Failure'
    
    results = player_parse('players_test.xml')
    if len(results) > 0: print 'Test 2: Success'
    else: print 'Test 2: Failure'
    
    results = league_parse('league_test.xml')
    if len(results) > 0: print 'Test 3: Success'
    else: print 'Test 3: Failure'
    
    results = projectedScores_parse('projectedScores_test.xml')
    if len(results) > 0: print 'Test 4: Success'
    else: print 'Test 4: Failure'
    
    results = injuries_parse('injuries_test.xml')
    if len(results) > 0: print 'Test 5: Success'
    else: print 'Test 5: Failure'
    
    results = nflSchedule_parse('nflSchedule_test.xml')
    if len(results) > 0: print 'Test 6: Success'
    else: print 'Test 6: Failure'
