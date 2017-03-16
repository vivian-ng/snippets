'''
Created on Mar 16, 2017

@author: vivian
'''

import datetime


class TimeStamp(object):
    def __init__(self, time_stamp_type):
        """ Class to hold a time stamp.
            Creates the time stamp with the current date and time.
        
            @param time_stamp_type: type of time stamp, specified by user
        """
        self.date_time_group = datetime.datetime.now()
        self.time_stamp_type = time_stamp_type
        
        
    def get_date(self):
        """ Returns the date of the time stamp.
        
            @return: date in the format YYYY-MM-DD
        """
        return self.date_time_group.strftime("%Y-%m-%d")


    def get_year_mth_day(self):
        """ Returns the date of the time stamp separately for year, month, and day.
        
            @return: date in the format YYYY, MM, DD
        """
        y = self.date_time_group.strftime("%Y")
        m = self.date_time_group.strftime("%m")
        d = self.date_time_group.strftime("%d")
        return y, m, d
    
    
    def get_time(self):
        """ Returns the time of the time stamp.
        
            @return: time in format HH:MM
        """
        return self.date_time_group.time().strftime("%H:%M")
    

    def get_year_mth(self):
        """ Returns the year and month of the time stamp.
        
            @return: year and month in format YYYY-MM
        """
        return self.date_time_group.strftime("%Y-%m")
