from time import time
import os
import shutil

import configparser
import csv


class Files:
    def __init__(self, folder):
        os.chdir('{}/simulations'.format(os.path.abspath(os.path.join('', os.pardir))))

        self.folder = folder  # folder with simulations
        self.time = time()  # current time
        self.destination = str(self.time)  # destination folder for simulation

        # go to output folder and create current one
        os.chdir(self.folder)
        os.mkdir(self.destination)

        # parse config
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # go to the new folder
        os.chdir(self.destination)

    # creates config in a current folder and returns it
    def create_сonfig(self):
        with open('config.ini', 'w') as config:
            self.config.write(config)

        return self.config

    def change_config(self, config):
        self.config = config

    def get_config(self):
        return self.config

    def make_csv(self, build, filename='data.cvs'):
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            [writer.writerow(r) for r in build[0]]
            writer.writerow('')
            [writer.writerow(r) for r in build[1]]
