import os
import sys
from rs4.psutil.piped import Piped

class PreciseEngine (Piped):
    def __init__(self, exe_file, model_file, chunk_size=2048):
        self.chunk_size = chunk_size
        cmd = [self.abspath (exe_file)]
        cmd += [self.abspath (model_file), str(self.chunk_size)]
        Piped.__init__ (self, cmd)

    def abspath (self, path):
        return os.path.join (os.path.dirname (os.path.abspath (sys.argv [0])), path)

    def communicate (self, input):
        if len(input) != self.chunk_size:
            raise ValueError('Invalid chunk size: ' + str(len(input)))
        out = Piped.communicate (self, input)
        return float(out)

class TriggerDetector:
    def __init__(self, chunk_size, sensitivity=0.5, trigger_level=3):
        self.chunk_size = chunk_size
        self.configure (sensitivity, trigger_level)
        self.activation = 0

    def reset (self):
        self.activation = 0

    def configure (self, sensitivity, trigger_level):
        self.sensitivity = sensitivity
        self.trigger_level = int (trigger_level * (2048 // self.chunk_size))

    def update(self, prob):
        chunk_activated = prob > 1.0 - self.sensitivity
        if chunk_activated or self.activation < 0:
            self.activation += 1
            has_activated = self.activation >= self.trigger_level
            if has_activated or chunk_activated and self.activation < 0:
                self.activation = -(8 * 2048) // self.chunk_size
            if has_activated:
                return True
        elif self.activation > 0:
            self.activation -= 1
        return False

class PreciseRunner(object):
    def __init__(self, model, chunk_size, sensitivity=0.5, trigger_level=4, on_prediction=lambda x: None, engine = None):
        self.chunk_size = chunk_size
        self.trigger_level = trigger_level
        self.on_prediction = on_prediction
        self.engine = self.create_engine (engine, model, chunk_size)

        self.running = False
        self.detector = TriggerDetector(self.chunk_size, sensitivity, trigger_level)

    def configure (self, sensitivity = 0.5, trigger_level = 4):
        self.detector.configure (sensitivity, trigger_level)

    def create_engine (self, engine, model, chunk_size):
        return PreciseEngine (engine or os.path.join (os.path.dirname (__file__), 'engine.py'), model, chunk_size)

    def reset (self):
        self.detector.reset ()

    def start(self):
        self.engine.start()
        self.running = True

    def stop(self):
        self.engine.stop()
        self.running = False

    def detect (self, chunk):
        if not self.running:
            raise SystemError ('engine already stopped')
        prob = self.engine.communicate (chunk)
        self.on_prediction(prob)
        if self.detector.update(prob):
            return True
        return False
