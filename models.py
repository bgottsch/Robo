#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:03:39 2018

@author: Beno
"""

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

from Robo import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    
    __tablename__ = "user"
    
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin    = db.Column(db.Boolean, nullable=False)

#    def get_reset_token(self, expires_sec=1800):
#        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
#        return s.dumps({'user_id': self.id}).decode('utf-8')
#
#    @staticmethod
#    def verify_reset_token(token):
#        s = Serializer(current_app.config['SECRET_KEY'])
#        try:
#            user_id = s.loads(token)['user_id']
#        except:
#            return None
#        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.admin}')"


class Job(db.Model):
    
    __tablename__ = "job"
    
    id                = db.Column(db.Integer, primary_key=True)
    scheduler_id      = db.Column(db.Integer, unique=True, nullable=False)
    name              = db.Column(db.String(20), unique=True, nullable=False)
    job_controller    = db.Column(db.PickleType, unique=False, nullable=False)
    
    def __repr__(self):
        return f"Job('{self.id}', '{self.name}', '{self.script_path}')"
    