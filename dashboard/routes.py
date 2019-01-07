from flask import current_app,render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

import pickle, sys
from apscheduler.triggers import cron

from Robo import db, scheduler
from Robo.models import Job
from Robo.job_controller import JobController

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/")
@dashboard.route("/dashboard")
@login_required
def index():
    
    jobs = []
    flash(len(scheduler.scheduler.get_jobs()))
    for job in scheduler.scheduler.get_jobs():
        
        db_job = Job.query.filter_by(scheduler_id=job.id).first()
        
        if db_job:
            job = {
                "name": job.name,
                "script_path": job.name
            }
            
            jobs.append(job)
    
    return render_template('dashboard.html', jobs=jobs)


@dashboard.route("/add_job", methods=['GET', 'POST'])
@login_required
def add_job():
    
    if request.method == 'GET':
        return redirect(url_for('dashboard.index'))
    
    name = request.form.get('job_name')
    
    if name:
        
        trigger = cron.CronTrigger(second="*/10")
        
        job = scheduler.scheduler.add_job(func=run_job, 
                                          args=[name],
                                          trigger=trigger, 
                                          name=name)
        
        job_controller = JobController(job_id=job.id, 
                                       name=job.name, 
                                       script_path="", 
                                       arguments=[], 
                                       job_dependancies=[], 
                                       path_dependancies=[])
        
        scheduler.scheduler.add_job(func=job_controller.run, 
                                    args=[],
                                    trigger=trigger, 
                                    name="teste_123")
        
        db_job = Job(scheduler_id=job.id, 
                     name=job.name, 
                     job_controller=pickle.dumps(job_controller))
        db.session.add(db_job)
        db.session.commit()
    
    return redirect(url_for('dashboard.index'))


def run_job(job_name):
 
#    db_job = Job.query.filter_by(name=job_name).first()
#    
#    job_controller = pickle.load(db_job.job_controller)
#    job_controller.run()
    print(0)





