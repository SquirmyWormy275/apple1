
from pathlib import Path
from dataclasses import asdict
from datetime import datetime,timezone
import json,subprocess,hashlib,time
from neural1.field_library import FieldLibraryAssistant,LessonCorpus
from neural1.models import OllamaHttpProvider,RecordingProvider
root=Path(__file__).parent
out=root/'ask-current'
out.mkdir()
temp=int(Path('/sys/class/thermal/thermal_zone0/temp').read_text())/1000
available=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
uuid=subprocess.run(['findmnt','-n','-o','UUID','/mnt/neural1-ssd'],capture_output=True,text=True).stdout.strip()
if temp>55 or available<3*1024**3 or uuid!='9a15851f-b8d7-4339-80b3-7b2aa6927192':raise SystemExit('Preflight resource/storage guard refused request')
provider=OllamaHttpProvider('phi4-mini:latest',api='chat',keep_alive=0,timeout_seconds=90,model_hash='78fad5d182a7c33065e153a5f8ba210754207ba9d91973f57dffa7f487363753',context_limit=4096,options={'num_predict':96,'temperature':0,'num_thread':2,'num_gpu':0,'num_batch':16})
recording=RecordingProvider(provider,out/'provider.jsonl')
corpus=LessonCorpus(root/'docs/field-library')
query='What are the three basic Monitor functions?'
started=datetime.now(timezone.utc).isoformat()
answer=FieldLibraryAssistant(corpus,recording).answer('ASK','M01',query,seed=7)
files=[root/'neural1/field_library.py',*(root/'docs/field-library/M01-meet-the-monitor').glob('*.md')]
receipt={'target':'STAGED_CURRENT_SOURCE_REAL_PI_VIRTUAL_APPLE1','started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'model':asdict(provider.record),'question':query,'answer':asdict(answer),'preflight_temperature_c':temp,'final_temperature_c':int(Path('/sys/class/thermal/thermal_zone0/temp').read_text())/1000,'preflight_available_memory_bytes':available,'uuid_verified':True,'serial_opened':False,'source_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n')
(out/'done').write_text('complete\n')
print(answer.text,flush=True)
