from flask import render_template
from app import app

@app.route('/')
def index():

  import subprocess
  cmd = subprocess.Popen(['sudo', './ps_mem'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout,error = cmd.communicate()
  memory = stdout.splitlines()
 
  cmd1 = subprocess.Popen(['uptime'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout1,error1 = cmd1.communicate()
  uptime = stdout1.splitlines()
 
  cmd2 = subprocess.Popen(['sar','1','3'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout2,error2 = cmd2.communicate()
  sar = stdout2.splitlines() 
   
  return render_template('index.html', memory=memory, uptime=uptime, sar=sar) 
