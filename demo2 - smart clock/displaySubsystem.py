import busio
import board
#from adafruit_ds3231 import adafruit_ds3231
import adafruit_ds3231
import adafruit_display_text.label
import math
import time

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday" )

i2c = busio.I2C(board.GP7,board.GP6)  # uses board.SCL and board.SDA
rtc = adafruit_ds3231.DS3231(i2c)

firstEnteringPageFlag = 1
_DAYS_IN_MONTH = (None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
_DAYS_BEFORE_MONTH = (None, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)

def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]

def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, "month must be in 1..12"
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


def _days_before_year(year):
    "year -> number of days before January 1st of year."
    year = year - 1
    return year * 365 + year // 4 - year // 100 + year // 400


def _ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, "month must be in 1..12"
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, "day must be in 1..%d" % dim
    return _days_before_year(year) + _days_before_month(year, month) + day

class DISPLAYSUBSYSTEM:
    def __init__(self, timeFormat):
        self.time_format = timeFormat
        
    def showDateTimePage(self,line1,line2,line3):
        line1.x = 2
        line1.y = 4
        line2.x = 8
        line2.y = 14
        line3.x = 10
        line3.y = 24
        t = rtc.datetime  
        date =  "%04d" % t.tm_year + '-' + "%02d" % t.tm_mon + '-' + "%02d" % t.tm_mday
        if self.time_format == 0: # 12 hour
            if t.tm_hour == 0:
                hour = 12
            elif t.tm_hour < 13:
                hour = t.tm_hour
            else:
                hour = t.tm_hour - 12
                
            dayOfTime = "{:2d}:{:02d} {}".format(
                hour,
                t.tm_min,
                "PM" if t.tm_hour > 11 else "AM")
        else: # 24 hour
            dayOfTime = "%02d" % t.tm_hour + ':' + "%02d" % t.tm_min + ':' + "%02d" % t.tm_sec
            
        line1.text = date
        line2.text = dayOfTime
        line3.text=days[int(t.tm_wday)]

    

    def showSetListPage(self,line1,line2,_selectSettingOptions):
        global firstEnteringPageFlag
        line1.x = 8
        line1.y = 7
        line2.x = 8
        line2.y = 23
        line1.text = "SET LIST"
        if _selectSettingOptions == 0:
            line2.text = "TIME SET"
        if _selectSettingOptions == 1:
            line2.text = "DATE SET"
        if _selectSettingOptions == 2:
            line2.text = "BEEP SET"
        if _selectSettingOptions == 3:
            line2.text = "autolight"
        if _selectSettingOptions == 4:
            line2.text = "12/24 hr"
        if firstEnteringPageFlag == 0:
            firstEnteringPageFlag = 1
            

    def timeSettingPage(self,line2,line3,_timeSettingLabel,_timeTemp):
        global firstEnteringPageFlag
        if firstEnteringPageFlag == 1:
            line2.x = 8
            line2.y = 13
            currentT = rtc.datetime
            _timeTemp[0] = currentT.tm_hour
            _timeTemp[1] = currentT.tm_min
            _timeTemp[2] = currentT.tm_sec
            firstEnteringPageFlag = 0
        currentTime = "%02d" % _timeTemp[0] + ':' + "%02d" % _timeTemp[1] + ':' + "%02d" % _timeTemp[2]
        line2.text = currentTime
        line3.text = "^"
        if _timeSettingLabel == 0:
            line3.x = 12
            line3.y = 24
        elif _timeSettingLabel == 1:
            line3.x = 29
            line3.y = 24
        else:
            line3.x = 47
            line3.y = 24


    def dateSettingPage(self,line2,line3,_timeSettingLabel,_dateTemp):
        global firstEnteringPageFlag
        if firstEnteringPageFlag == 1:
            line2.x = 3
            line2.y = 13
            currentD = rtc.datetime
            _dateTemp[0] = currentD.tm_year
            _dateTemp[1] = currentD.tm_mon
            _dateTemp[2] = currentD.tm_mday
            firstEnteringPageFlag = 0
        currentDate = "%02d" % _dateTemp[0] + '-' + "%02d" % _dateTemp[1] + '-' + "%02d" % _dateTemp[2]
        line2.text = currentDate
        line3.text = "^"
        if _timeSettingLabel == 0:
            line3.x = 12
            line3.y = 24
        elif _timeSettingLabel == 1:
            line3.x = 36
            line3.y = 24
        else:
            line3.x = 54
            line3.y = 24
            
    def onOffPage(self,line2,line3,_selectSettingOptions,_beepFlag,_autoLightFlag, _timeFormatFlag):
        if _selectSettingOptions == 2:
            line2.x = 20
            line2.y = 7
            line3.x = 20
            line3.y = 23            
            if _beepFlag:
                line2.text = "> on"
                line3.text = "  off"
            else:
                line2.text = "  on"
                line3.text = "> off"
        if _selectSettingOptions == 3:
            line2.x = 20
            line2.y = 7
            line3.x = 20
            line3.y = 23            
            
            if _autoLightFlag:
                line2.text = "> on"
                line3.text = "  off"
            else:
                line2.text = "  on"
                line3.text = "> off"
        if _selectSettingOptions == 4:
            line2.x = 10
            line2.y = 7
            line3.x = 10
            line3.y = 23            

            if _timeFormatFlag:
                line2.text = "  12 Hr"
                line3.text = "> 24 Hr"                
            else:
                line2.text = "> 12 Hr"
                line3.text = "  24 Hr"                
                
        
    
    def setDateTime(self,_selectSettingOptions,_dateTemp,_timeTemp):
        getTime = rtc.datetime
        if _selectSettingOptions == 0:
            t = time.struct_time((getTime.tm_year, getTime.tm_mon, getTime.tm_mday, _timeTemp[0], _timeTemp[1], _timeTemp[2], getTime.tm_wday, -1, -1))
            rtc.datetime = t
        if _selectSettingOptions == 1:
            w = (_ymd2ord(_dateTemp[0],_dateTemp[1], _dateTemp[2]) + 6) % 7
            t = time.struct_time((_dateTemp[0], _dateTemp[1], _dateTemp[2], getTime.tm_hour, getTime.tm_min, getTime.tm_sec, w, -1, -1))
            rtc.datetime = t


    def setTimeFormat(self, _selectFormat):
        self.time_format = _selectFormat
