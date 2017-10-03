from random import random
from math import log, exp


"""
each event return a tuple:
(time, 'type of the event', filament, position, ...)
where filament and position means
the actual coordinate of the action
and some special info
"""


class Events:
    def __init__(self, config):
        self.constants = {
            'c': float(config['general']['c']),
            'on': float(config['general']['on']),
            'str': float(config['general']['str']),
            'hydro': float(config['general']['hydro']),
            'T': {
                'bend': float(config['gtp']['bend']),
                'long': float(config['gtp']['long']),
                'lat': float(config['gtp']['lat'])
            },
            'D': {
                'bend': float(config['gdp']['bend']),
                'long': float(config['gdp']['long']),
                'lat': float(config['gdp']['lat'])
            },
        }
    
    def association(self, x, y):
        k = self.constants['c'] * self.constants['on']
        return -log(random())/k, 'association', x, y
    
    def straightening(self, x, y):
        k = self.constants['str']
        return -log(random())/k, 'straightening', x, y
    
    def dissociation(self, x, y, hydrolysed):
        c = self.constants['D'] if hydrolysed else self.constants['T']  # hydrolyzed or not
        k = self.constants['on'] * exp(-c['long'])
        return -log(random())/k, 'dissociation', x, y
    
    def bending(self, x, y, connections, hydrolysed):
        c = self.constants['D'] if hydrolysed else self.constants['T']  # hydrolyzed or not
        k = self.constants['str'] * exp(-(c['lat'] * connections - c['bend']))
        return -log(random())/k, 'bending', x, y
    
    def hydrolysis(self, x, y):
        k = self.constants['hydro']
        return -log(random())/k, 'hydrolysis', x, y