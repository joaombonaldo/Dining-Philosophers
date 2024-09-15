from __future__ import annotations
import threading
import logging
from random import uniform
from typing import Tuple

from constants import PhilosopherState
from forks import Fork

logger = logging.getLogger(__name__)

class Philosopher(threading.Thread):
    EAT_TIMES_UNTIL_FULL = 3

    def __init__(self, id: int, forks: Tuple[Fork, Fork]) -> None:
        threading.Thread.__init__(self)
        self.id = id
        self.state = PhilosopherState.THINKING
        self.forks = forks
        self.full = 0

    def run(self):
        while self.full < self.EAT_TIMES_UNTIL_FULL:
            self.think()
            self.eat()
            self.full += 1
        logger.info(f'{self} is full')

    def eat(self):
        logger.info(f'{self} is hungry, trying to eat')
        
        # Request both forks
        # for fork in self.forks:
        #     fork.request(self)


        fork1, fork2 = sorted(self.forks, key=lambda f: f.id)
    
        
        fork1.request(self)
        fork2.request(self)
        


        self.state = PhilosopherState.EATING
        logger.info(f'{self} is eating')
        # Instead of sleeping, just let other philosophers run
        # Release forks after eating
        for fork in self.forks:
            fork.done()

    def think(self):
        self.state = PhilosopherState.THINKING
        logger.info(f'{self} is thinking')
        # Simulate thinking without sleeping; real implementation would involve work
        # This placeholder is for simulation; in practice, remove sleep and use actual logic

    def __repr__(self) -> str:
        return f'Philosopher {self.id}'
