from time import sleep, time, ctime
import threading
import datetime as dt
import pytz
from tzwhere import tzwhere
from geopy import geocoders
import ntplib
from work_with_site import WorkWithSite
from tsu_parser import ScheduleExtractor
import json

class MoodleParseLessons:

    def __init__(self):
        self.requestCorrectTime()
        self.current_faculty = "Институт прикладной математики и компьютерных наук"
        self.current_group = "932209"
        self.selected_day = "15.05.2023"
        # self.correctDayFromNTP = dt.datetime.strptime(self.selected_day, "%d.%m.%Y").date()
        self.strCorrectDayFromNTP = self.correctDayFromNTP.strftime("%d.%m.%Y")
        # self.actualTimePerMinute = dt.datetime.combine(self.correctDayFromNTP, dt.time(0,0,0))
        self.startLessonTime = self.actualTimePerMinute
        self.endLessonTime = self.startLessonTime
        self.login = ""
        self.password = ""
        self.city = "Tomsk"
        self.waitTimeRange = 4
        self.lessonStartNotificationTimeDelta = 10
        self.__waitThreadIsWorking = True
        self.__isLessonStart = False

        def knowTimezone():
            place, (lat, lng) = geocoders.Nominatim(user_agent="MyLocation").geocode(self.city)
            where = tzwhere.tzwhere()
            timezone = where.tzNameAt(lat, lng)
            return timezone

        self.timezone = knowTimezone()
        self.workWithMoodle = WorkWithSite()

    def requestCorrectTime(self):
        ntp_client = ntplib.NTPClient()
        countOfErrors = 0
        while(True):
            try:
                response = ntp_client.request('pool.ntp.org')
                c = ctime(response.tx_time)
                self.actualTimePerMinute = dt.datetime.strptime(c, "%a %b %d %H:%M:%S %Y")
                self.correctDayFromNTP = self.actualTimePerMinute.date()
                self.strCorrectDayFromNTP = self.correctDayFromNTP.strftime("%d.%m.%Y")
                break
            except ntplib.NTPException as exception:
                countOfErrors += 1
                if countOfErrors >= 15:
                    raise exception
                print(exception)
        return self.actualTimePerMinute

    def parseSchedule(self):
        selected_day = self.correctDayFromNTP.strftime("%d.%m.%Y")
        self.schedule = ScheduleExtractor(self.current_faculty, self.current_group, selected_day)
        self.schedule.save_to_json()

    def executeWorkWithSite(self):
        self.workWithMoodle.startBrowser()
        self.workWithMoodle.clickOn('//*[@id="login_url"]')
        self.workWithMoodle.setText('//*[@id="Email"]', self.login)  # Логин или email
        self.workWithMoodle.setText('//*[@id="Password"]', self.password)  # Пароль
        self.workWithMoodle.clickOn('//*[@id="loginForm"]/form/div[3]/input[2]')

    def get_schedule_from_JSONfile(self):
        with open("pure_schedule_Institut_prikladnoj_matematiki_i_komp'juternyh_nauk_932209.json") as json_file:
            self.schedule = json.load(json_file)

    def actualNextLesson(self):
        self.requestCorrectTime()
        self.iterLessons = iter(self.actualDayLessons.items())
        try:
            self.nextLesson = next(self.iterLessons)
            for lesson in self.actualDayLessons.values():
                if not (self.actualTimePerMinute <= self.nextLesson[1].get("ends")):
                    self.nextLesson = next(self.iterLessons)
                else:
                    break
        except StopIteration:
            pass
        self.startLessonTime = self.nextLesson[1].get("starts")
        self.endLessonTime = self.nextLesson[1].get("ends")

    def parseActualDayLessons(self):
        self.requestCorrectTime()
        self.actualDayLessons = self.schedule.get(str(self.correctDayFromNTP))
        for lesson in self.actualDayLessons.values():
            lesson["starts"] = dt.datetime.combine(self.correctDayFromNTP, dt.datetime.strptime(lesson.get("starts"), "%H:%M:%S").time())
            lesson["ends"] = dt.datetime.combine(self.correctDayFromNTP, dt.datetime.strptime(lesson.get("ends"), "%H:%M:%S").time())
        self.actualNextLesson()

    def isLessonStart(self):
        return self.__isLessonStart

    def StartWaitLesson(self):
        self.requestCorrectTime()
        self.actualNextLesson()

        isActualTimePerMinuteSet = False
        while not isActualTimePerMinuteSet:
            try:
                self.actualNextLesson()
                self.correctDayFromNTP = self.actualTimePerMinute.date()
                isActualTimePerMinuteSet = True
            except TypeError:
                True

        def waitLessonThread(self):
            print("Start waitLessonThread")
            self.__waitThreadIsWorking = True
            while(self.__waitThreadIsWorking):
                self.requestCorrectTime()
                if self.startLessonTime - dt.timedelta(
                        minutes=self.lessonStartNotificationTimeDelta) <= self.actualTimePerMinute <= self.endLessonTime:
                    self.__isLessonStart = True
                else:
                    self.__isLessonStart = False
                sleep(self.waitTimeRange)
            print("End of waitLessonThread")

        thread = threading.Thread(target=waitLessonThread, args=(self,))
        thread.name = "waitLessonThread"
        thread.start()

    def StopWaitLesson(self):
        self.__waitThreadIsWorking = False


if __name__ == '__main__':
    moodleParseLessons = MoodleParseLessons()
    moodleParseLessons.parseSchedule()
    # moodleParseLessons.executeWorkWithSite()
    moodleParseLessons.get_schedule_from_JSONfile()
    moodleParseLessons.parseActualDayLessons()
    moodleParseLessons.requestCorrectTime()
    moodleParseLessons.StartWaitLesson()

    # Не удаляйте следующие закомментированные строчки, они нужны для теста
    # Идет проверка работы потока функций ожидания занятия и его прекращения
    # start = time()
    # startOnce = True
    # endOnce = True
    # while(True):
    #     if time() - start >= 20 and endOnce:
    #         moodleParseLessons.StopWaitLesson()
    #         endOnce = False
    #     if moodleParseLessons.isLessonStart():
    #         print("Lesson {} is start!".format(moodleParseLessons.nextLesson[0]))
    #     else:
    #         print("Lesson {} is don't start".format(moodleParseLessons.nextLesson[0]))
    #     print("actualTimePerMinute", moodleParseLessons.actualTimePerMinute, moodleParseLessons.nextLesson[1])
    #     if time() - start >= 60 and startOnce:
    #         moodleParseLessons.StartWaitLesson()
    #         startOnce = False
    #     sleep(2)
    # print("end")
    sleep(100000)