from core.files import Files
from core.events import Events
import core.simulation

import numpy as np


# edit Events parameter for this calibration
def dissociation(self, x, y, hydrolysed):
    return -np.log(np.random.random()) / float(self.config['general']['koff']), 'dissociation', x, y

Events.dissociation = dissociation


if __name__ == "__main__":
    files = Files('gmpcpp')
    config = files.get_config()

    # get config data
    lateral_start = float(config['calibration']['lat-start'])
    lateral_end = float(config['calibration']['lat-end'])
    lateral_steps = int(config['calibration']['lat-steps'])
    koff_start = float(config['calibration']['koff-start'])
    koff_end = float(config['calibration']['koff-end'])
    koff_steps = int(config['calibration']['koff-steps'])

    # remove config data
    config.remove_section('calibration')
    files.change_config(config)
    files.create_сonfig()

    for i in np.linspace(lateral_start, lateral_end, num=lateral_steps):
        config['gtp']['lat'] = str(i)

        # seeded mt
        seed = ['00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' for i in range(int(config['mt']['protofilaments']))]

        for j in np.linspace(koff_start, koff_end, num=koff_steps):
            config['general']['koff'] = str(j)

            files.change_config(config)
            files.create_сonfig()
            build = core.simulation.build(files, seed)

            SPEED = 100 #56250  # dimers/sec
            if 1000 > (build[1][1][1] - build[1][2][-1]) / float(config['time']['timer']) > 50:
                print(build[0])

            #files.make_csv(core.simulation.build(files), '{}_{}.csv'.format(i, j))