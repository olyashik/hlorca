from lorettOrbital.orbital import *
from HardwareLorettRotator import *
from pprint import pprint
from time import sleep

DEBUG = True
class Main_Lorett_Rotator:
    '''Класс адаптер для организации взаимодействия между отдельными компонентами'''

    def __init__(self) -> None:
        self.stationName = 'r8s'

        #self.path = 'C:/Users/User/Desktop/Lorett-Rotator-main/level-up'
        self.path = '/home/pi/hlorca/level-up'

        self.lat = 54.5268
        self.lon = 36.1673
        self.alt = 159
        self.timeZone = 3

        self.schedule = []

        self.logger = LorettLogging(self.path)
        try:
            config = supportedStationTypes['r8s'].copy()
            config['horizon'] = 15
            config['minApogee'] = 40
            self.orbital = Scheduler(self.stationName, self.lat, self.lon, self.alt, self.path, timeZone=self.timeZone, config=config)
            self.logger.info('start lorettOrbital.Scheduler')
        except:
            self.logger.error('no start lorettOrbital.Scheduler')
        self.schedule += self.orbital.getSchedule(24, returnNameSatellite=True, returnTable=False)
        try:
            self.logger.info('start Rotator_SerialPort')
            self.rotator = Rotator_SerialPort(self.logger, DEBUG=DEBUG, port='COM4')
        except:
            self.logger.error('no start Rotator_SerialPort')


    def tracking(self, track: tuple) -> object:
        '''Функция для отслеживания спутника во время пролета'''
        self.logger.info(f'start tracking satellite')
        self.logger.debug(f"Go to start pozition: az: {track[1][0][1]} el: {track[1][0][2]}")
        self.rotator.rotate(track[1][0][1], track[1][0][2])
        sleep(5)
        for steps in track[1]:
            self.logger.debug(f'Go to pozitions: az: {steps[1]} el: {steps[2]}')
            self.rotator.rotate(steps[1], steps[2])
            sleep(1)

    def sleep_to_next(self, time_sleep:datetime, nameSatellite:str, timeRecord):
        print('поспал')
        time_sleep = int(time_sleep.total_seconds())
        self.logger.info(f'Next satellite {nameSatellite} pass to: {time_sleep} seconds')
        while time_sleep > 70:
            sleep(10)
            time_sleep -= 10
            self.logger.debug(f'Next satellite {nameSatellite} pass to: {time_sleep} seconds')
        #todo запустить скрипт записи
        self.recording(nameSatellite, timeRecord)
        while time_sleep > 1:
            sleep(1)
            time_sleep -= 1
            self.logger.debug(f'Next satellite {nameSatellite} pass to: {time_sleep} seconds')

    def recording(self, nameSatellite, timeRecord):
        #os.startfile(f'C:/Users/User/Desktop/Lorett-Rotator-main/level-up/канал2.py --s {nameSatellite} --t {timeRecord}')
        pass

    def main(self):
        while True:
            #print(self.schedule)
            # берем следующий пролет
            satPas = self.schedule[0]
            self.schedule = self.schedule[1:]
            # вычисляем время до пролета
            sleep_time = satPas[1][0] - datetime.utcnow()
            timeRecord = int((satPas[1][0] - satPas[1][2]).total_seconds())
            print('slee', sleep_time)
            self.sleep_to_next(sleep_time, satPas[0], timeRecord)
            self.tracking(self.orbital.nextPass())
            self.rotator.homing()


if __name__ == '__main__':
    station = Main_Lorett_Rotator()
    station.main()
