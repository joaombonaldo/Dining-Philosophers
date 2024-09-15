from __future__ import annotations
import logging
from dataclasses import dataclass, field
from threading import Lock, Condition, Semaphore
from typing import TYPE_CHECKING

from constants import ForkState

if TYPE_CHECKING:
    from philosophers import Philosopher 

logger = logging.getLogger(__name__)

@dataclass
class Fork:
    id: int
    _owner: Philosopher = field(init=False, default=None)
    state: ForkState = field(init=False, default=ForkState.DIRTY)
    lock: Lock = field(init=False, default_factory=Lock)
    condition: Condition = field(init=False, default_factory=Condition)
    semaphore: Semaphore = field(init=False, default_factory=lambda: Semaphore(1))

    def request(self, philosopher: Philosopher):
        with self.semaphore:
            if self._owner == philosopher:
                logger.info(f'{philosopher} is already the owner of {self}, clean it')
                self.state = ForkState.CLEAN
                return

            if self.state is ForkState.DIRTY:
                logger.info(f'{philosopher} getting the dirty {self} and cleaning it')
                self.state = ForkState.CLEAN
                self._owner = philosopher
                return

            if self.state is ForkState.CLEAN:
                with self.condition:
                    logger.info(f'{philosopher} is waiting for {self}')
                    self.condition.wait()
                    logger.info(f'{philosopher} getting ownership of {self} and cleaning it')
                    self._owner = philosopher
                    self.state = ForkState.CLEAN

    def done(self):
        with self.lock:
            self.state = ForkState.DIRTY

        with self.condition:
            self.condition.notify_all()

    def __repr__(self) -> str:
        return f'Fork {self.id}'
