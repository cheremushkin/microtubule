from time import time
import os
import shutil

import configparser
import csv


class Output:
    folder: ''
    time: 0
    current: ''

    def __init__(self, folder):
        os.chdir('{}/output'.format(os.path.abspath(os.path.join('', os.pardir))))

        self.folder = '{}'.format(folder)  # folder with simulations
        self.time = time()  # current time
        self.current = '{}/{}'.format(self.folder, self.time)  # destination folder for simulation

        # output directory for current simulation
        os.mkdir(self.current)
        shutil.copyfile('{}/config.ini'.format(self.folder), '{}/config.ini'.format(self.current))  # copy config
        os.chdir(self.current)

    def config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        return config

    def make(self, build):
        with open('data.csv', 'w') as file:
            writer = csv.writer(file)
            [writer.writerow(r) for r in build[0]]
            writer.writerow('')
            [writer.writerow(r) for r in build[1]]
