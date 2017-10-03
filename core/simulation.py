from core.microtubule import Microtubule

from core.output import Output
from core.events import Events


def start(dir):
    out = Output(dir)
    config = out.config()
    events = Events(config)

    # создание микротрубочки
    columns = int(config['mt']['protofilaments'])
    timer = float(config['time']['timer'])
    fps = float(config['time']['fps'])
    depth = float(config['mt']['depth'])

    mt = Microtubule(columns, timer, depth, fps, events)
    build = mt.build()

    # generate output
    out.make(build)


if __name__ == "__main__":
    start('simulations')

#print("Выполнено за {} секунд".format((stop - start)))