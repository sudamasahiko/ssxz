# -*- coding:utf-8 -*-

from Vminterface import Vminterface

class DataCenterManager():
    def __init__(self):

        # interface object
        self.instance0 = Vminterface('centos7_2', '192.168.122.2')

        # launch vm like this
        # self.instance0.make_instance(1, 1024, 4)

        # if you want to completely delete instance, do like
        # self.instance0.undefine()

        # if you want to start instance0 which is down, do like
        # self.instance0.start()

        # check if the instance is up
        if self.instance0.is_up():
            print('instance is running or initializing')
        
        # check if the instance is ready to communicate
        if self.instance0.is_ssh_up():
            print('instance is running')

        # che if the instance is installed
        if self.instance0.has_instance():
            print('there is an instance, which may be either running or down')