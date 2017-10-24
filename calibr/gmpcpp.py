from core.files import Files
from core.events import Events
import core.simulation

import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('cheremushkin', 'fsdjBUr906AXZS6CsKmT')

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

    x = np.linspace(lateral_start, lateral_end, num=lateral_steps)
    y = np.linspace(koff_start, koff_end, num=koff_steps)
    xv, yv = np.meshgrid(x, y)
    zv = np.zeros_like(xv)

    # seeded mt
    seed = ['00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' for i in range(int(config['mt']['protofilaments']))]

    for i in range(x.size):
        config['gtp']['lat'] = str(x[i])

        for j in range(y.size):
            config['general']['koff'] = str(y[j])

            files.change_config(config)
            files.create_сonfig()
            build = core.simulation.build(files, seed)

            print('{}-{}, calc {}-{} finished'.format(i, j, x[i], y[j]))
            files.make_csv(build, '{}_{}.csv'.format(i, j))

            #SPEED = 100 56250 dimers/sec
            zv[i][j] = (build[1][1][1] - build[1][2][-1]) / float(config['time']['timer'])
    print(zv)
    data = [
        go.Surface(
            x=xv,
            y=yv,
            z=zv
        ),
        go.Surface(
            x=xv,
            y=yv,
            z=np.ones_like(zv) * 30000,
            opacity=0.7
        )
    ]

    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='3d-scatter-colorscale')