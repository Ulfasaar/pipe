import datetime as dt
import time

"""
    version 0.1 
    
    A library that makes caching data to improve performance incredibly easy
    It offers the ability to refresh data periodically, on external version change, a super effecient hybrid approach 
    and a way to refresh caches manually
"""
class Cache(object):
    __slots__ = ("data", "_refresh", "_empty", "isInit")

    def __init__(self,refresh,empty = None):
        self.data = None
        self.isInit = True
        self._refresh = refresh
        self._empty = empty

    def get(self):
        if self.isInit:
            self.data = self._refresh()
            self.isInit = False
        return self.data

    def refresh(self):
        self.data = self._refresh()

    def empty(self):
        self.data = self._empty()


class HybridCache(Cache):
    __slots__ = ("timeout", "hasElapsed", "current_time", "prev_time", "diff_time", "current_version", "get_version")

    def __init__(self,timeout_ms,refresh,get_version,empty = None):
        self.get_version = None
        self.current_version = None
        self.diff_time = None
        self.prev_time = None
        self.current_time = None
        self.timeout = None
        self.hasElapsed = False
        super(HybridCache, self).__init__(refresh,empty)
        self.timeout = timeout_ms
        self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
        self.prev_time = self.current_time
        self.diff_time = (self.current_time - self.prev_time)
        self.get_version = get_version
        self.current_version = self.get_version()

    def version(self):
        return self.current_version

    def refresh(self):
        self.current_version = self.get_version()
        self.diff_time = 0
        self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
        self.prev_time = self.current_time
        self.data = self._refresh()

    def get(self):
        if (self.isInit == False):
            if (self.timeout != -1):
                self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
                self.diff_time = (self.current_time - self.prev_time)
                if (self.diff_time >= self.timeout):
                    external_version = self.get_version()
                    if (self.current_version < external_version):
                        self.data = self._refresh()
                        self.current_version = external_version
                    self.prev_time = self.current_time
        else:
            self.refresh()
            self.isInit = False
        return self.data

class TimeoutCache(Cache):
    __slots__ = ("timeout", "hasElapsed", "current_time", "prev_time", "diff_time")

    def __init__(self,timeout_ms,refresh,empty = None):
        self.diff_time = None
        self.prev_time = None
        self.current_time = None
        self.timeout = None
        self.hasElapsed = False
        super(TimeoutCache, self).__init__(refresh,empty)
        self.timeout = timeout_ms
        self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
        self.prev_time = self.current_time
        self.diff_time = (self.current_time - self.prev_time)

    def refresh(self):
        self.diff_time = 0
        self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
        self.prev_time = self.current_time
        self.data = self._refresh()

    def get(self):
        if (self.isInit == False):
            if (self.timeout != -1):
                self.current_time = (time.mktime(dt.datetime.now().date().timetuple()) * 1000)
                self.diff_time = (self.current_time - self.prev_time)
                if (self.diff_time >= self.timeout):
                    self.data = self._refresh()
                    self.prev_time = self.current_time
        else:
            self.data = self._refresh()
            self.isInit = False
        return self.data



class VersionedCache(Cache):
    __slots__ = ("current_version", "get_version")

    def __init__(self,refresh,get_version,empty = None):
        self.get_version = None
        self.current_version = 0.0
        super(VersionedCache, self).__init__(refresh,empty)
        self.get_version = get_version
        self._empty = empty
        self.current_version = self.get_version()

    def version(self):
        return self.current_version

    def refresh(self):
        self.current_version = self.get_version()
        self.data = self._refresh()

    def get(self):
        if self.isInit:
            self.data = self._refresh()
            self.isInit = False
        else:
            external_version = self.get_version()
            if (self.current_version < external_version):
                self.data = self._refresh()
                self.current_version = external_version
        return self.data