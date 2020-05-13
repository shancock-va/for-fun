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
    extras: [(str, str)]

@dataclass
class ExpensesData:
    '''Class for keeping track of a expenses.'''
    expenses: [(str, str)]

