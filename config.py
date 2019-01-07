#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:03:39 2018

@author: Beno
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Config:
    
    SECRET_KEY = 'c10d090bfa57f47fbe7408fc1fc43a4cc5e2311814e191b0'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'robo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#    MAIL_SERVER = 'smtp.googlemail.com'
#    MAIL_PORT = 587
#    MAIL_USE_TLS = True
#    MAIL_USERNAME = os.environ.get('EMAIL_USER')
#    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///'+os.path.join(basedir, 'job_store.db'))
    }

#    SCHEDULER_EXECUTORS = {
#        'default': {'type': 'threadpool', 'max_workers': 20}
#    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }

    SCHEDULER_TIMEZONE = 'America/Sao_Paulo'
