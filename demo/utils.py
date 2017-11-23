#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/29 下午1:45
# @Author  : OD
# @File    : utils.py
import datetime
import threading
import time
import random

from MySQLdb import Date

from base import *
from decimal import Decimal
import inspect

from demo.exception import InitializException, IllegalArgumentException


class DateUtils(object):
    """
    日期util
    """
    DEFAULT_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    DEFAULT_DATE_FORMAT = '%Y/%m/%d'
    DATE_FORMAT_YEAR = '%Y'
    DATE_FORMAT_MONTH = '%Y%m'
    DEFAULT_FORMAT_DAY = '%Y%m%d'
    DEFAULT_FORMAT_HOUR = '%H'

    @staticmethod
    def last_year():
        now = DateUtils.now()
        now_year = DateUtils.format(now, DateUtils.DATE_FORMAT_YEAR)
        last_year = int(now_year) - 1
        return last_year

    @staticmethod
    def addMinute(d1, minutes):
        return d1 + datetime.timedelta(minutes=minutes)

    @staticmethod
    def addHour(hour):
        d1 = datetime.datetime.now()
        return d1 + datetime.timedelta(hours=hour)

    @staticmethod
    def addDay(d1, days):
        return d1 + datetime.timedelta(days=days)

    @staticmethod
    def addMonth(d1, n=1):

        one_day = datetime.timedelta(days=1)

        q, r = divmod(d1.month + n, 12)

        datetime2 = datetime.datetime(
            d1.year + q, r + 1, 1) - one_day
        if d1.month != (d1 + one_day).month:
            return datetime2

        if d1.day >= datetime2.day:
            return datetime2

        return datetime2.replace(day=d1.day)

    @staticmethod
    def addYear(d1, years):
        return DateUtils.addDay(d1, years * 365)

    @staticmethod
    def month_differ(datetime1, datetime2):
        '''
        两个时间相差月，忽略天
        :param d1:
        :param d2:
        :return:
        '''
        return abs((datetime1.year - datetime2.year) * 12 + (datetime1.month - datetime2.month) * 1)

    @staticmethod
    def format(date, format=DEFAULT_FORMAT):
        return date.strftime(format)

    @staticmethod
    def parse(timestr, format=DEFAULT_FORMAT):
        return datetime.datetime.strptime(timestr, format)

    '''
    返回当前时间字符串
    '''

    @staticmethod
    def now():
        return datetime.datetime.now()

    '''
    datetime1与datetime2时间差(秒)
    '''

    @staticmethod
    def timeDiff(datetime1, datetime2):
        return (datetime1 - datetime2).seconds

    @staticmethod
    def day_diff(datetime1, datetime2):
        """
        时间差：天
        :param datetime1:
        :param datetime2:
        :return:
        """
        return (datetime1 - datetime2).days

    @staticmethod
    def datetime_timestamp(date):
        '''
        datetime转timestamp
        :param date:
        :return:
        '''
        t = date.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % date.microsecond)) / 1000000
        return timeStamp

    @staticmethod
    def date_2_week(date_str):
        # 20150101
        date = DateUtils.parse(date_str, '%Y%m%d')
        weekday = date.weekday()
        if weekday == 0:
            return "周一"
        elif weekday == 1:
            return "周二"
        elif weekday == 2:
            return "周三"
        elif weekday == 3:
            return "周四"
        elif weekday == 4:
            return "周五"
        elif weekday == 5:
            return "周六"
        elif weekday == 6:
            return "周日"
        return None


class MemCache(dict):
    '''
    缓存
    '''
    def __new__(cls, *args):

        if not hasattr(cls, '_instance'):
            cls._instance = dict.__new__(cls)
        else:
            raise InitializException(Message.INITIALIZ_EXCEPTION)

        return cls._instance

    @classmethod
    def getInstance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = dict.__new__(cls)
            cls._instance.start_gc_thread()

        return cls._instance

    '''
    获取name对应的value
    '''

    def get(self, name, default=None):
        if not name:
            return default
        if not self.has_key(name):
            return default
        return self[name]

    '''
    设置value
    '''

    def set(self, name, value, life_time=5):
        if name is None or value is None:
            return
        item = CacheItem(value=value, life_time=life_time)
        self[name] = item

    def pop(self, name, default=None):
        '''
        删除缓存
        :param name:
        :return:
        '''
        if not name:
            return default
        levels = name.split('.')
        data = self
        for level in levels:
            try:
                data = data[level]
                del self[level]
            except:
                return default
        return data

    def start_gc_thread(self):
        thread = threading.Thread(target=self.gc)
        thread.daemon = True
        thread.start()

    def gc(self):
        '''
        删除过期缓存
        :return:
        '''
        while True:
            for key in self.keys():
                item = self[key]
                if item.is_expired():
                    del self[key]
            time.sleep(5)

    def getset(self, name, value):
        g = self.get(name)
        if not g:
            g = value
            self.set(name, g)
        else:
            g.value = value
        return g


class CacheItem(object):
    '''
    缓存元素
    '''

    def __init__(self, value, life_time=2):
        self.value = value
        self.life_time = life_time
        self.create_time = DateUtils.now()

    def is_expired(self):
        '''
        是否超时
        :return:
        '''
        return DateUtils.addMinute(self.create_time, self.life_time) < DateUtils.now()


class StringUtils(object):
    """
    字符串工具类
    """
    REPLACE_DELIMETER = ':'

    @staticmethod
    def index(string, delimeter, n):
        '''
        查询delimeter第n次出现的位置
        :return:
        '''
        string = string.replace(delimeter, StringUtils.REPLACE_DELIMETER, n - 1)
        return string.index(delimeter)

    @staticmethod
    def year(string):
        if string is None:
            return string
        if string[0:4] == '2016':
            return '2016'
        return string


class UserManage(object):
    """
    用户相关
    """
    thread_local = threading.local()

    @staticmethod
    def get_current_user():
        """
        获取当前登录用户
        """
        return getattr(UserManage.thread_local, 'user', None)

    @staticmethod
    def get_user_id():
        """
        获取当前用户id
        """
        return UserManage.get_current_user().id


class PercentUtils(object):
    @staticmethod
    def repair(repair, *percents):
        """
        修复百分比数据异常（加起来不等于100%）

        :param repair: 待修复的数据，默认选择最后一组
        :param percents: 其他数据，多参数
        :return:
        """
        totalOther = sum(percent for percent in percents)
        total = totalOther + repair
        # 等于100%，直接返回
        # 总数和100% 差距超过 0.05 时，不过滤
        if total != 1.0 and (total >= 0.95 or total <= 1.05):
            repair = 1.0 - totalOther

        return repair

    @staticmethod
    def getAgeRange(age_18, age_18_24, age_25_34, age_35_44, age_45):
        result = [float(age_18), float(age_18_24), float(age_25_34), float(age_35_44)]
        repair = PercentUtils.repair(float(age_45), float(age_18), float(age_18_24), float(age_25_34), float(age_35_44))
        result.append(float("%.2f" % repair))
        return result


class Bean:
    def __init__(self, key, alias_name=None, accuracy=2, callback=None):
        self.key = key
        self.alias_name = alias_name
        self.accuracy = accuracy
        self.callback = callback


class DecimalUtils(object):
    @staticmethod
    def to_float(dec, accuracy=2):
        if not isinstance(dec, Decimal):
            return dec
        # return round(dec, accuracy)
        return float(('%.' + str(accuracy) + 'f') % dec)

    @staticmethod
    def sub(d1, d2, accuracy=2):
        """
        减法
        :param d1:
        :param d2:
        :param accuracy:
        :return:
        """
        if d1 is None or d2 is None:
            return None
        if d1 == 0 or d2 == 0:
            return None
        return DecimalUtils.to_float(Decimal(d1) - Decimal(d2), accuracy)

    @staticmethod
    def add(d1, d2, accuracy=2):
        """
        加法
        :param d1:
        :param d2:
        :param accuracy:
        :return:
        """
        if d1 == None or d2 == None:
            return None
        return DecimalUtils.to_float(Decimal(d1) + Decimal(d2), accuracy)

    @staticmethod
    def div(d1, d2, accuracy=2):
        if d1 == None or d2 == None or d2 == 0:
            return None
        return DecimalUtils.to_float(Decimal(d1) / Decimal(d2), accuracy)


class ReflectUtils(object):
    """
    # 示例:
    class DivisionPo:

        _config = [
            Bean('id'),
            Bean('level'),
            Bean('name'),
            Bean('time'),
            Bean('parent.name', 'parentName', StringUtils.callback)
        ]

    class Division:
        def __init__(self):
            pass

    if __name__ == '__main__':
        division = Division()
        division.id = 1
        division.name = '123'
        division.full_name = '上海市'
        division.level = Decimal(10.8098)
        division.time = datetime.datetime.today()
        parent = Division()
        parent.id = 10
        parent.name = '上海市'
        division.parent = parent

        divisionPo = DivisionPo()
        ReflectUtils.copy(division, divisionPo)
        print(obj2json(divisionPo))
    """
    DELIMETER = '.'

    @staticmethod
    def copy(source, target):
        """
        将source上的属性拷贝到target上
        """
        for bean in target._config:
            k = bean.key
            ele = ReflectUtils.getattr(source, k)
            ele = ReflectUtils.obj2_string(ele, bean.accuracy)
            if inspect.isfunction(bean.callback):
                ele = bean.callback(ele)
            setattr(target, bean.alias_name if bean.alias_name else k.replace('.', '_'), ele)

    @staticmethod
    def getattr(obj, attr):
        index = attr.find(ReflectUtils.DELIMETER)
        if index > 0:
            return ReflectUtils.getattr(getattr(obj, attr[0:index]), attr[index + 1:len(attr)])
        return getattr(obj, attr)

    @staticmethod
    def obj2_string(ele, accuracy=2, default=None):
        """
        转换 数据 为 string
        :param ele:
        :param accuracy: 小数点精读
        :param default: 默认值
        :return:
        """
        if ele is None:
            return default
        elif isinstance(ele, float):
            ele = float(('%.' + str(accuracy) + 'f') % ele)
        elif isinstance(ele, Decimal):
            ele = DecimalUtils.to_float(ele, accuracy)
        elif isinstance(ele, datetime.datetime):
            ele = DateUtils.format(ele)
        elif isinstance(ele, Date):
            ele = DateUtils.format(ele, DateUtils.DATE_FORMAT)
        return ele


class CheckUtil(object):
    @staticmethod
    def check_none(param, desc):
        if param is None:
            raise IllegalArgumentException(desc + '不能为空')


class PrecisionUtil(object):
    @staticmethod
    def array_4_to_2(objs):
        """
        更新数组的精度，从4位，调整到2位
        """
        result = list()
        sum = 0
        for obj in objs[0:len(objs) - 1]:
            value = ReflectUtils.obj2_string(obj, accuracy=2)
            sum += value
            result.append(value)
        result.append(ReflectUtils.obj2_string((1 - sum), accuracy=2))
        return result

    @staticmethod
    def marriage_dict_repair(objs):
        # 通过未婚计算已婚数据
        marriaged = 1 - objs['unmarriage']
        objs['marriaged'] = ReflectUtils.obj2_string(marriaged, accuracy=4)
        # 确保 已婚 = 已婚已育 + 已婚未育
        marriaged_birth = marriaged - objs['marriaged_childless']
        objs['marriaged_birth'] = ReflectUtils.obj2_string(marriaged_birth, accuracy=4)
        return objs

    @staticmethod
    def dict_repair2(objs, accuracy=4):
        keys = objs.keys()
        sum = 0
        for key in keys[0:len(keys) - 1]:
            value = ReflectUtils.obj2_string(objs.get(key), accuracy=accuracy)
            sum += value
            objs[key] = value
        objs[keys[len(keys) - 1]] = ReflectUtils.obj2_string((1 - sum), accuracy=accuracy)
        return objs


class CodeUtil(object):
    '''
    生成验证码
    '''
    @staticmethod
    def generate_verification_code(length=6):
        code_list = []
        for i in range(length):
            random_num = random.randint(0, 9)
            code_list.append(str(random_num))
        verification_code = ''.join(code_list)
        return verification_code

