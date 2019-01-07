#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:03:39 2018

@author: Beno
"""

from apscheduler.events import EVENT_ALL
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError


class Scheduler(object):
    
    def __init__(self, scheduler=None, app=None):
        self._scheduler = scheduler or BackgroundScheduler()
        
        self.app = None
        if app:
            self.init_app(app)

    @property
    def running(self):
        return self._scheduler.running

    @property
    def state(self):
        return self._scheduler.state

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def task(self):
        return self._scheduler.scheduled_job

    def init_app(self, app):

        self.app = app
        self.app.apscheduler = self

        self._load_config()

    def start(self, paused=False):
        self._scheduler.start(paused=paused)

    def shutdown(self, wait=True):
        self._scheduler.shutdown(wait)

    def pause(self):
        self._scheduler.pause()

    def resume(self):
        self._scheduler.resume()

    def add_listener(self, callback, mask=EVENT_ALL):
        self._scheduler.add_listener(callback, mask)

    def remove_listener(self, callback):
        self._scheduler.remove_listener(callback)

    def add_job(self, id, func, **kwargs):
        
        job_def = dict(kwargs)
        job_def['id'] = id
        job_def['func'] = func
        job_def['name'] = job_def.get('name') or id

        return self._scheduler.add_job(**job_def)

    def remove_job(self, id, jobstore=None):
        self._scheduler.remove_job(id, jobstore)

    def remove_all_jobs(self, jobstore=None):
        self._scheduler.remove_all_jobs(jobstore)

    def get_job(self, id, jobstore=None):
        return self._scheduler.get_job(id, jobstore)

    def get_jobs(self, jobstore=None):
        return self._scheduler.get_jobs(jobstore)

    def modify_job(self, id, jobstore=None, **changes):
        return self._scheduler.modify_job(id, jobstore, **changes)

    def pause_job(self, id, jobstore=None):
        self._scheduler.pause_job(id, jobstore)

    def resume_job(self, id, jobstore=None):
        self._scheduler.resume_job(id, jobstore)

    def run_job(self, id, jobstore=None):
        job = self._scheduler.get_job(id, jobstore)

        if not job:
            raise JobLookupError(id)

        job.func(*job.args, **job.kwargs)

    def _load_config(self):
        
        options = dict()

        job_stores = self.app.config.get('SCHEDULER_JOBSTORES')
        if job_stores:
            options['jobstores'] = job_stores

        executors = self.app.config.get('SCHEDULER_EXECUTORS')
        if executors:
            options['executors'] = executors

        job_defaults = self.app.config.get('SCHEDULER_JOB_DEFAULTS')
        if job_defaults:
            options['job_defaults'] = job_defaults

        timezone = self.app.config.get('SCHEDULER_TIMEZONE')
        if timezone:
            options['timezone'] = timezone

        self._scheduler.configure(**options)
