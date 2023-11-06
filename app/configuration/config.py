from pydantic import BaseSettings
from datetime import date
import os

class FacultySettings(BaseSettings): 
    application:str = 'Faculty Management System' 
    webmaster:str = 'sjctrags@university.com'
    created:date = '2021-11-10'