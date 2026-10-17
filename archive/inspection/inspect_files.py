import concurrent.futures, hashlib, json, urllib.request, urllib.parse, zipfile, re
from pathlib import Path
from xml.etree import ElementTree as ET
from pypdf import PdfReader

root=Path(__file__).resolve().parent
pdfs=[
('R1','R1. The Phantom Stock-Out Detector.pdf'),
('R2','R2. The Returns Fraud vs. Genuine Grievance Sorter.pdf'),
('R3',"R3. The Conversational Shopping Assistant That Doesn't Lie_9.pdf"),
('R4','R4. Demand Forecasting for the New Product With No History_1.pdf'),
('R5','R5.Turning Store Chatter Into Action.pdf'),
('H1','H1. OPD Triage Assistant for an Overloaded Government Hospital_6.pdf'),
('H2','H2.Discharge Summary to Patient-Understandable Care Plan_6.pdf'),
('H3','H3. Predicting the 30-Day Readmission- And Doing Something About It.pdf'),
('H4','H4. The Medication Safety Second Pair of Eyes_2.pdf'),
('H5','H5. Frontline Health-Worker Companion for Low-Connectivity Areas_2.pdf'),
('BFSI11','Smart Data Masking System for PII Protection_1.pdf'),
('BFSI12','Intelligent Life Insurance Needs Finder & Digital Advisory Platform_1.pdf')]
templates=['Round1_Template submission.pptx','Round1_Template submission_1.pptx','TalentAP-MegaHackathon2026_Idea_Submission_Template_Final (2) (1)_3.pptx']+['Round1_Template submission_'+str(n)+'.pptx' for n in range(2,11)]
jobs=[(label,'pdf',name) for label,name in pdfs]+[(pdfs[i][0],'pptx',name) for i,name in enumerate(templates)]
def inspect(job):
    label,ext,name=job
    url='https://be.innosmart.in/media/talentap/'+urllib.parse.quote(name)
    path=root/(label+'.'+ext)
    with urllib.request.urlopen(url,timeout=40) as response: data=response.read()
    path.write_bytes(data)
    result=dict(label=label,kind=ext,url=url,path=str(path),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
    if ext=='pdf':
        reader=PdfReader(path)
        texts=[p.extract_text() or '' for p in reader.pages]
        result.update(pages=len(texts),metadata={str(k):str(v) for k,v in (reader.metadata or {}).items()})
    else:
        with zipfile.ZipFile(path) as z:
            names=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1)))
            texts=['\n'.join(ET.fromstring(z.read(n)).itertext()) for n in names]
            result.update(slides=len(names),core=z.read('docProps/core.xml').decode() if 'docProps/core.xml' in z.namelist() else '')
    text='\n\n'.join(texts)
    (root/(label+'-'+ext+'.txt')).write_text(text,encoding='utf-8')
    result['text_sha256']=hashlib.sha256(text.encode()).hexdigest()
    return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(inspect,jobs): results.append(result)
(root/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k not in ('metadata','core','path','url')} for r in results],indent=2))
print('R3 TEMPLATE TEXT\n'+(root/'R3-pptx.txt').read_text(encoding='utf-8'))
print('R1 TEMPLATE TEXT\n'+(root/'R1-pptx.txt').read_text(encoding='utf-8'))
