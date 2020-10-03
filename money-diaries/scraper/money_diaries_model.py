""" Models for Money Diaries """
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PageMetaData:
    '''Class for keeping track of a page's metadata.'''
    title: str
    author: str
    publish_date: datetime

@dataclass
class OccupationData:
    '''Class for keeping track of a occupation data.'''
    occupation: str
    industry: str
    location: str
    extras: [(str, str, str)]

@dataclass
class ExpensesData:
    '''Class for keeping track of a expenses.'''
    expenses: [(str, str, str)]

@dataclass
class TimeEntry:
    '''Class for keeping track of a day's time entry.'''
    time_of_day: datetime
    description: str
    money_spent: str

@dataclass
class Day:
    '''Class for keeping track of a day.'''
    title: str
    total: str
    time_entries: TimeEntry

