from core.microtubule import Microtubule

from core.files import Files
from core.events import Events


def build(files):
    config = files.get_config()
    events = Events(config)

    # создание микротрубочки
    columns = int(config['mt']['protofilaments'])
    timer = float(config['time']['timer'])
    fps = float(config['time']['fps'])
    depth = float(config['mt']['depth'])

    mt = Microtubule(columns, timer, depth, fps, events)
    return mt.build()


if __name__ == "__main__":
    files = Files('flat')
    files.create_сonfig()

    # build and generate output
    files.make_csv(build(files))

#print("Выполнено за {} секунд".format((stop - start)))