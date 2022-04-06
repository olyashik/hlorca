from os import name
from sched import scheduler
from lorettOrbital.orbital import Scheduler
from HardwareLorettRotator import *
from orbital import *
from threading import Thread
from pprint import pprint
from time import sleep


class Main_Lorett_Rotator:
    '''Класс адаптер для организации взаимодействия между отдельными компонентами'''
    def __init__(self) -> None:

        self.stationName = 'r8s' 

        self.path = '.'
        # self.path = '/home/pi/Desktop/Lorett-Rotator/level-up'

        self.lat = 55.3970
        self.lon = 55.3970
        self.alt = 130 
        self.timeZone = 3

        self.schedule = []

        self.logger = LorettLogging(self.path)
        try:
            self.orbital = Scheduler(self.stationName, self.lon, self.lat, self.alt, self.path, timeZone=self.timeZone)
            self.logger.info('start lorettOrbital.Scheduler')
        except:
            self.logger.error('no start lorettOrbital.Scheduler')
        self.schedule += self.orbital.getSchedule(24, returnNameSatellite=True, returnTable=False)
        '''
       try:
            self.logger.info('start Rotator_SerialPort')
            self.rotator = Rotator_SerialPort(self.logger, DEBUG=True, port='COM5')
        except:
            self.logger.error('no start Rotator_SerialPort')
        '''


    def tracking(self,track:tuple):
        '''Функция для отслеживания спутника во время пролета'''
        self.logger.info(f'start tracking satellite {track[0]}')

        for steps in track[1]:
            self.logger.debug(f'Go to pozitions: az: {steps[1]} el: {steps[2]}')

            sleep(1)
  

    def sleep_to_next(self, time_sleep:datetime, nameSatellite:str):
        time_sleep = int(time_sleep.total_seconds())
        self.logger.info(f'Next satellite {nameSatellite} pass to: {time_sleep} seconds')
        while time_sleep > 70:
            sleep(10)
            time_sleep -= 10
            self.logger.debug(f'Next satellite {nameSatellite} pass to: {time_sleep} seconds')
        
            
    def main(self):
        while True:
            # print(self.schedule)
            # берем следующий пролет
            satPas = self.schedule[0]
            self.schedule = self.schedule[1:]
            # вычисляем время до пролета
            sleep_time = satPas[1][0] - datetime.utcnow()
            self.tracking(self.orbital.nextPass())
            break
            


if __name__ == '__main__':
    station = Main_Lorett_Rotator()
    station.main()