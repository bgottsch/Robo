#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:03:39 2018

@author: Beno
"""


import os, glob
import sys
import datetime
import pytz

utc = pytz.UTC

from Robo import db, scheduler
from Robo.models import Job


class JobController:
    
    def __init__(self, job_id, name, script_path, arguments, job_dependancies, path_dependancies):
        self.job_id = job_id
        self.name = name
        self.script_path = script_path
        self.arguments = arguments
        self.job_dependancies = job_dependancies
        self.path_dependancies = path_dependancies
        
        self.status = 0
        self.pending_jobs = []
        
    
    def run(self):
        
        now = utc.localize(datetime.datetime.now())
        
        job = scheduler.get_job(self.job_id)
        
        if job.next_run_time < now:
            
            for dependancy_id in self.job_dependancies:
                job_dependancy = scheduler.get_job(dependancy_id)
                if job_dependancy.next_run_time < now:
                    self.print_log("Esperando {0} finalizar".format(job_dependancy.name))
                    self.pending_jobs.append(dependancy_id)
                    return
            
            if self.call_script():
                self.status = 1
                self.pending_jobs = []
                self.print_log("Rotina concluida")
            else:
                self.status = 0
                self.print_log("Rotina falhou")
            
        else:
            self.print_log("Rotina já foi rodada")
            
    
    def call_script(self):
        
        try:
#            with open(self.script_path,"r") as file:
#                exec(file.read())
            return True
        except Exception as e:
            self.print_log(e)
            return False
        
        
    def print_log(self, text):
        date = datetime.datetime.strftime(datetime.datetime.now(), 
                                          format="%Y-%m-%d %H:%M:%S")
        sys.stdout.write("[{0}][{1}] - {2}\n".format(date, self.name, text))
        sys.stdout.flush()