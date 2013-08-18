import copy

class player:
    def __init__(self, name="", team="", pos="", bye=-1):
        self.name = name
        self.team = team
        self.pos = pos
        self.bye = bye
  
    def s_name(self, name): self.name = name
    def g_name(self): return copy.copy(self.name)
    def s_team(self, team): self.team = team
    def g_team(self): return copy.copy(self.team)
    def s_pos(self, pos): self.pos = pos
    def g_pos(self): return copy.copy(self.pos)
    def s_bye(self, bye): self.bye = bye
    def g_bye(self): return copy.copy(self.bye)
    
    def is_empty(self):
        return ((self.name == "") or (self.team == "") or (self.pos == "") or (self.bye == -1))
