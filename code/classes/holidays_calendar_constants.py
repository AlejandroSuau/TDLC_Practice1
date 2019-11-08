# -*- coding: utf-8 -*-

from classes.holiday_row import HolidayType

class Constants(object):
    DATES_FORMAT = "%d-%m-%Y"
    MOVED_STRING_INDICATOR = 'se traslada'
    HREF_PROPERTY = 'href'
    
    LEFT_PROVINCES_DIV_ID = 'columnaIzquierda'
    LEFT_PROVINCES_TAG_NAME = 'a'

    YEARS_DIV_CLASS_NAME = 'wrapAnteriorSiguiente'
    YEARS_TAG_NAME = 'a'
    
    MONTHS_CONTAINER_ID = 'wrapIntoMeses'
    MONTHS_DIV_CLASS_NAME = 'mes'
    
    BOX_DAY_REF = 'COLORED_BOXES_CLASS_NAME'
    STRING_DAY_REF = 'STRING_SPAN_CLASS_NAME'
    
    HOLIDAYS_REFS = {
        HolidayType.NATIONAL: {
            BOX_DAY_REF: 'cajaFestivoN',
            STRING_DAY_REF: 'festivoN'
        },
        HolidayType.AUTONOMOUS: {
            BOX_DAY_REF: 'cajaFestivoR',
            STRING_DAY_REF: 'festivoR'
        },
        HolidayType.LOCAL: {
            BOX_DAY_REF: 'cajaFestivoP',
            STRING_DAY_REF: 'festivoP'
        }   
    }