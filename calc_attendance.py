'''
Calculate attendance (working hours?) in a month.

To use:
- Create a StaffRecord to hold the staff's attendance.
- Fill the StaffRecord with timestamps for the staff.
  Timestamps should be records of date and time, and either "IN" or "OUT".
- CallÅ@the calc_staff_month_time() function with the required parameters.

Created on Mar 16, 2017

@author: vivian
'''
import datetime
from timestamp import TimeStamp


class StaffRecord(object):
    """ Class to store staff records.
    """
    def __init__(self, staff_id, staff_name):
        """Constructor"""
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.staff_attendance = {} # empty dictionary to hold attendance timestamps

    def add_time_stamp(self, time_stamp_type, date_time_group=""):
        """ Method to add a time stamp to the staff's record.
            
            @param time_stamp_type: Either an "IN" or an "OUT"
            @param date_time_group: Date and time using Python's datetime 
                                    class, defaults to current time if left blank
        """
        time_stamp = TimeStamp(time_stamp_type)
        if date_time_group != "":
            time_stamp.date_time_group = date_time_group
        year_mth = time_stamp.get_year_mth()
        if not year_mth in self.staff_attendance.keys():
            self.staff_attendance[year_mth] = []
        self.staff_attendance[year_mth].append(time_stamp)


def calc_staff_month_time(default_start, default_end, staff, year_mth):
    """ Method to calculate hours and minutes attended in given month.
    
        @param default_start: default start time in "HH:MM"
        @param default_end: default end time in "HH:MM"
        @param staff: StaffRecord to calculate for
        @param year_mth: target month to calculate for, in format "YYYY-MM"
    """
    # Get default start and end times from configuration file.
    staff_default_start_hour = default_start.split(":")[0]
    staff_default_start_minute = default_start.split(":")[1]
    staff_default_end_hour = default_end.split(":")[0]
    staff_default_end_minute = default_end.split(":")[1]
    # Initialize counters for month and day.
    hours_attended = 0
    minutes_attended = 0
    day_hours = 0
    day_minutes = 0
    target_date = 0
    target_date_record = None
    # Tally time utilized for the month if the staff has attendance records in the target month.
    if year_mth in staff.staff_attendance.keys():
        records = staff.staff_attendance[year_mth]
        for record in records:
            record_date = record.get_date()
            if target_date != 0: # If this is not the first record
                if record_date == target_date: # Record on the same date as previous record.
                    if record.time_stamp_type == "OUT":
                        # Records on same day, "IN" followed by "OUT", or "OUT" followed by "OUT".
                        time_diff = record.date_time_group - target_date_record.date_time_group
                        m, s = divmod(time_diff.total_seconds(), 60)
                        day_hours, day_minutes = divmod (m, 60)
                        target_date_record = record
                    elif target_date_record.time_stamp_type == "OUT":
                        # Records on same day, "OUT" followed by "IN".
                        target_date = record.get_date()
                        target_date_record = record
                        day_hours = 0
                        day_minutes = 0
                    else:
                        # Records on same day, "IN" followed by "IN".
                        pass
                else: # Record on another date
                    if target_date_record.time_stamp_type == "IN":
                        # "IN" record on previous date not closed,
                        # so just assume the previous record ended at the default end time.
                        y, m, d = target_date_record.get_year_mth_day()
                        target_date_end_time = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=staff_default_end_hour, minute=staff_default_end_minute)
                        time_diff = target_date_end_time - target_date_record.date_time_group
                        m, s = divmod(time_diff.total_seconds(), 60)
                        day_hours, day_minutes = divmod (m, 60)
                        hours_attended += day_hours
                        minutes_attended += day_minutes
                    if record.time_stamp_type == "OUT":
                        # No "IN" record for the day,
                        # so just assume the day started at the default start time.
                        y, m, d = record.get_year_mth_day()
                        target_date_start_time = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=staff_default_start_hour, minute=staff_default_start_minute)
                        time_diff = record.date_time_group - target_date_start_time 
                        m, s = divmod(time_diff.total_seconds(), 60)
                        day_hours, day_minutes = divmod (m, 60)
                        hours_attended += day_hours
                        minutes_attended += day_minutes
                    # Sets this record as the new day.
                    target_date = record.get_date()
                    target_date_record = record
                    day_hours = 0
                    day_minutes = 0
            else: # first record, so just set the date
                if record.time_stamp_type == "OUT":
                    # No "IN" record for the first day,
                    # so just assume the day started at the default start time.
                    y, m, d = record.get_year_mth_day()
                    target_date_start_time = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=staff_default_start_hour, minute=staff_default_start_minute)
                    time_diff = record.date_time_group - target_date_start_time 
                    m, s = divmod(time_diff.total_seconds(), 60)
                    day_hours, day_minutes = divmod (m, 60)
                    hours_attended += day_hours
                    minutes_attended += day_minutes
                target_date = record.get_date()
                target_date_record = record
                day_hours = 0
                day_minutes = 0

            # Add the time utilized for the day to the month's time.
            hours_attended += day_hours
            minutes_attended += day_minutes
            # Reset the time utilized for the day since it has been tallied to the month's time.
            day_hours = 0
            day_minutes = 0
        
        if target_date_record.time_stamp_type == "IN":
            # "IN" record on previous date not closed,
            # so just assume the previous record ended at the default end time.
            y, m, d = target_date_record.get_year_mth_day()
            target_date_end_time = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=staff_default_end_hour, minute=staff_default_end_minute)
            time_diff = target_date_end_time - target_date_record.date_time_group
            m, s = divmod(time_diff.total_seconds(), 60)
            day_hours, day_minutes = divmod (m, 60)
            hours_attended += day_hours
            minutes_attended += day_minutes
                
    return hours_attended, minutes_attended
