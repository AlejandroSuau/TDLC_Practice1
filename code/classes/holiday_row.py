# -*- coding: utf-8 -*-

class HolidayType(object):
    NATIONAL = "Nacional"
    AUTONOMOUS = "Autonómica"
    LOCAL = "Local"

"""
The HolidayRow implementation.
"""
class HolidayRow:
    
    def __init__(self, name, date, province, holiday_type, moved_date_from):
        self.name = name
        self.date = date
        self.province = province
        self.holiday_type = holiday_type
        self.moved_date_from = moved_date_from
    
    def __repr__(self):
        object_repr = [
            self.name,
            self.date,
            self.province,
            self.holiday_type
        ]
        
        if self.moved_date_from is None:
            object_repr.append('')
        else:
            object_repr.append(self.moved_date_from)
        
        return object_repr
    
    def __str__(self):
        return ("{}, {}, {}, {}, {}".format(
                self.name, self.date, self.province, self.holiday_type, self.moved_date_from))