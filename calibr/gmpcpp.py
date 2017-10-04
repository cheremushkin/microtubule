from core.output import Output
import core.simulation

import numpy as np

def config(self):
    print(self.config['general']['c'])

Output.create_сonfig = config

if __name__ == "__main__":
    out = Output('gmpcpp')
    config = out.get_config()

    lateral_start = float(config['gtp']['lat-start'])
    lateral_end = float(config['gtp']['lat-end'])
    lateral_steps = int(config['gtp']['lat-steps'])
    for i in np.linspace(lateral_start, lateral_end, num = lateral_steps):
        print(i)
    #out.create_сonfig()

    #core.simulation.start(out)