from abc import ABC, abstractmethod
from datetime import datetime
import threading
import math

class Module(ABC):
    def __init__(self) -> None:
        self._thread    = None
        self._stop      = threading.Event()
        self._lock      = threading.Lock()

        self._period: float = 0 
        self._offset: float = 0
    

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()
    
    
    def start(self, period:float=1, offset:float=0):
        # Defaults to every second on the second
        if self._thread and self._thread.is_alive(): return

        self._period = period
        self._offset = offset
        
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    
    def stop(self):
        self._stop.set()
        try: self._cleanup()
        except: pass
        if self._thread: self._thread.join()
        self._stop.clear()
     
    
    def _run(self):
        while not self._stop.is_set():
            now = datetime.now()
            index = now.hour*3600 + now.minute*60 + now.second + now.microsecond/1e6
            next = math.ceil(index/self._period) * self._period + self._offset 
            if next <= index: next += self._period 
            if self._stop.wait(timeout= next - index): break
            self._update()

    
    @abstractmethod
    def _update(self):
        pass

    
    def _cleanup(self):
        pass
