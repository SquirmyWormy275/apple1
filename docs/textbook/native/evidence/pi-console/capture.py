
from pathlib import Path
from datetime import datetime, timezone
import subprocess,json
root=Path(__file__).parent
commands=[
 ('status-before','STATUS'),
 ('models','MODELS'),
 ('source','SOURCE A01 sources'),
 ('ask','ASK M01 What are the three basic Monitor functions?'),
 ('hint','HINT A03 How does BNE decide whether to repeat?'),
 ('explain','EXPLAIN C04 Why does the harness set bit 7 on keyboard input?'),
 ('check','CHECK M05 RTS always returns a program started with R to the Monitor.'),
 ('trace',r'TRACE A01 "LDA #$2A\nSTA $0400\nJMP $FF1F"'),
 ('status-after','STATUS'),
]
for label,command in commands:
 print('Starting native console',label,flush=True)
 start=datetime.now(timezone.utc).isoformat()
 try:
  r=subprocess.run(['/usr/local/bin/neural1','console','--command',command],capture_output=True,text=True,timeout=200)
  result={'started_utc':start,'command':command,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'target':'INSTALLED_REAL_PI_VIRTUAL_APPLE1','serial_opened':False}
 except subprocess.TimeoutExpired:
  result={'started_utc':start,'command':command,'exit_code':124,'error':'Console call exceeded 200 seconds; stopped','target':'INSTALLED_REAL_PI_VIRTUAL_APPLE1','serial_opened':False}
 (root/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(label,'exit',result['exit_code'],flush=True)
 if result['exit_code']:break
(root/'done.json').write_text(json.dumps({'finished_utc':datetime.now(timezone.utc).isoformat()})+'\n')
