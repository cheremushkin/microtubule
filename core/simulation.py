from core.microtubule import Microtubule

from core.files import Files
from core.events import Events


def build(files):
    config = files.get_config()

    # создание микротрубочки
    mt = Microtubule(
        columns=int(config['mt']['protofilaments']),
        timer=float(config['time']['timer']),
        fps=float(config['time']['fps']),
        events=Events(config),
        mode='window',
        window=5
    )

    #return
    mt.build()


if __name__ == "__main__":
    files = Files('flat')
    files.get_config()

    # build and generate output
    build(files)
    #files.make_csv(build(files))

#print("Выполнено за {} секунд".format((stop - start)))