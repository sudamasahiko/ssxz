# -*- coding:utf-8 -*-

# 
# ssxz.py
# 

from was import WebAPIServer
from dcm import DataCenterManager

class Ssxz():
    def __init__(self):
        self.was = WebAPIServer()
        self.dcm = DataCenterManager()