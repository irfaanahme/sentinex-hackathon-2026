import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const root=process.cwd();
const skill=process.env.CODEX_PRESENTATIONS_SKILL;
if (!skill) throw new Error('Set CODEX_PRESENTATIONS_SKILL to your installed presentations skill directory.');
const python=process.env.CODEX_PYTHON || 'python3';
const source=path.join(root,'references/official/shared-template.pptx');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const blue='#224C87',cyan='#00A6E8',ink='#303030';
const identity=JSON.parse(await fs.readFile('archive/ppt-build/identity.json','utf8').catch(()=>'{}'));
const specs=[{
 key:'Problem_9_H4_Medication_Safety',title:'H4. The Medication Safety Second Pair of Eyes',track:'Healthcare / Problem 9 (H4)',
 source:'https://be.innosmart.in/media/talentap/H4.%20The%20Medication%20Safety%20Second%20Pair%20of%20Eyes_2.pdf',
 pain:['Patients may take medicines from several prescribers, with mixed names and incomplete lists.','Clinicians need to spot interactions, duplicate therapy and patient-specific risks.','Missed serious issues can harm patients. Too many minor alerts can hide urgent ones.'],
 market:['Initial users: clinicians and pharmacists reviewing patients on several medicines.','Proposed adoption: start with a small review workflow, then assess hospital integration.','Baseline: manual reference lookups. Our aim is one prioritized, explainable review.'],
 solution:['Match brand names and misspellings to the supplied drug reference before checking.','Check interactions, duplicate therapy, renal-dose concerns and contraindications.','Show severity, involved medicines, a reference-backed action and confidence.','Flag uncertain matches for confirmation. A clinician makes the final decision.'],
 flow:['Medication list\nPatient context','Name matching\nReference checks','Prioritized alerts\nClinician review'],
 steps:['1. Load supplied drug, interaction and synthetic patient data.','2. Resolve medicine names using exact matches, then cautious fuzzy matching.','3. Apply reference rules and rank alerts by severity.','4. Build a simple review screen and test serious cases plus non-issues.'],
 architecture:['Patient list and context','Name resolver + confidence','Rules + supplied references','Alert list for clinician review'],
 plan:'Planned stack: Python, RapidFuzz, pandas and Streamlit.\nDay 1: matching and rules. Day 2: evaluation, review screen and demo.',
 challenges:[['Wrong medicine match','Problem: similar names can refer to different medicines.','Mitigation: use exact matches first and require confirmation for ambiguity.'],['Alert fatigue','Problem: too many low-severity warnings can distract the clinician.','Mitigation: rank by severity, merge duplicates and measure excess alerts.'],['Incomplete clinical context','Problem: missing medicines or patient details limit the checks.','Mitigation: show missing context and limitations. Never declare the list safe.']],
 usp:['Resolve names first\nShow match confidence before applying safety rules.','Prioritize useful alerts\nBalance serious-issue detection against unnecessary warnings.','Explain each concern\nShow supporting rules, limitations and a clinician action.'],
 advantage:['Compared with a simple exact-name lookup, test whether cautious matching finds more valid cases.','Make uncertainty visible and keep every recommendation tied to the supplied references.'],
 demo:['PLANNED DEMO — prototype not yet built','1. Load a supplied synthetic patient with mixed medicine names.','2. Confirm uncertain matches and show prioritized safety alerts.','3. Compare a serious-risk case with a case containing no flagged issue.','Planned evaluation: serious-issue recall, name-match accuracy,\nlow-severity alerts per patient and recall on 300 seeded near-misses.'],
 limit:'No issue found means only in the available list and supplied references. A clinician decides.'
},{
 key:'Problem_11_BFSI_Data_Masking',title:'Smart Data Masking System for PII Protection',track:'BFSI / Problem 11',
 source:'https://be.innosmart.in/media/talentap/Smart%20Data%20Masking%20System%20for%20PII%20Protection_1.pdf',
 pain:['Sensitive customer fields can reach internal users who do not need the full values.','Support staff, analysts and administrators need different levels of access.','The task is to protect query results across databases while preserving the original records.'],
 market:['Initial users: financial institutions with support and analytics teams.','Proposed adoption: pilot a few sensitive tables, then expand approved policies.','Baseline: manually tagged fields or separate masked copies. We propose one reusable policy layer.'],
 solution:['Scan column names and row samples with rules to identify sensitive fields.','Tag fields as PII_HIGH or FINANCIAL_CONFIDENTIAL and apply role policies.','Admin gets full values, Support partial masking, Analyst redaction or keyed hashes.','Enforce the policy before returning results on PostgreSQL and SQLite. Keep raw data unchanged.'],
 flow:['Admin\nFull values','Support\nPartial masking','Analyst\nRedaction or hashes'],
 steps:['1. Connect read-only to PostgreSQL and SQLite.','2. Scan schema and samples, then review uncertain field tags.','3. Apply server-side role policies to approved query results.','4. Compare roles and test unchanged source records on both backends.'],
 architecture:['Verified user role + approved query','Read-only database adapter','Field tags + masking policy','Only permitted values reach user'],
 plan:'Planned stack: Python, SQLAlchemy and Streamlit.\nDay 1: scan and policy engine. Day 2: second backend, access tests and demo.',
 challenges:[['Missed sensitive fields','Problem: names alone can misclassify customer fields.','Mitigation: combine schema and sample patterns. Block uncertain fields pending review.'],['Access bypass','Problem: a forged role or unsupported query could expose data.','Mitigation: verify roles on the server, restrict queries and deny unsupported requests.'],['Different database behavior','Problem: field types and query results can differ between backends.','Mitigation: use adapters and run the same role-policy tests on both databases.']],
 usp:['Discover and protect\nConnect field detection directly to explicit masking policies.','One policy, two backends\nCheck consistent role behavior on PostgreSQL and SQLite.','Originals stay intact\nMask returned values without creating a second customer-data copy.'],
 advantage:['Test the scanner against a column-name-only baseline to measure detection errors.','Use a small, inspectable policy layer with access tests instead of relying on screen-only hiding.'],
 demo:['PLANNED DEMO — prototype not yet built','1. Scan an approved synthetic customer table and inspect its field tags.','2. Run the same approved query as Admin, Support and Analyst.','3. Repeat on both backends, reject a forbidden request and check originals.','Planned evaluation: scanner precision/recall, role-policy pass rate,\nsource-data equality and query latency against an unmasked baseline.'],
 limit:'MVP scope: approved read-only queries on two backends. Hashes are not a guarantee of anonymity.'
}];

function shape(slide,id){return slide.shapes.items.find(s=>s.id===String(id));}
function write(slide,id,lines,size=20,options={}){
 const s=shape(slide,id);const paras=Array.isArray(lines)?lines:[lines];
 s.text=paras.map(t=>({runs:[{run:t,style:{typeface:'Calibri',fontSize:`${size}px`,color:options.color??ink,bold:options.bold??false}}],spaceAfter:options.spaceAfter??8}));
 s.text.style={typeface:'Calibri',fontSize:size,color:options.color??ink,bold:options.bold??false,alignment:options.align??'left',verticalAlignment:'top',autoFit:'none',wrap:'square',insets:8};
 return s;
}
function text(slide,name,txt,x,y,w,h,size=18,bold=false){const s=slide.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});s.text=txt;s.text.style={typeface:'Calibri',fontSize:size,color:ink,bold,autoFit:'none',insets:3,verticalAlignment:'top'};return s;}
function diagram(slide,labels,x,y,w,h,horizontal=false){
 const gap=horizontal?28:14, n=labels.length, bw=horizontal?(w-gap*(n-1))/n:w, bh=horizontal?h:(h-gap*(n-1))/n;
 let last;
 labels.forEach((label,i)=>{const s=slide.shapes.add({geometry:'rect',name:`Flow ${i+1}`,position:{left:x+(horizontal?i*(bw+gap):0),top:y+(horizontal?0:i*(bh+gap)),width:bw,height:bh},fill:'#FFFFFF',line:{fill:blue,width:1.2}});s.text=label;s.text.style={typeface:'Calibri',fontSize:18,color:blue,alignment:'center',verticalAlignment:'middle',insets:6,autoFit:'none'};
 if(last && !(horizontal&&labels[0].startsWith('Admin')))slide.shapes.connect(last,s,{kind:'straight',fromSide:horizontal?'right':'bottom',toSide:horizontal?'left':'top',line:{fill:cyan,width:1.5},tail:{type:'triangle'}}).bringToFront();last=s;});
}

for(const spec of specs){
 const p=await PresentationFile.importPptx(await FileBlob.load(source)); const s=p.slides.items;
 write(s[0],3,spec.title,28,{color:cyan,align:'center'}).position={left:48,top:182,width:864,height:72};
 write(s[0],5,identity.team??'[Team name required]',24,{color:'#FFFFFF'});
 write(s[0],7,identity.lead??'[Team leader required]',24,{color:'#FFFFFF'});
 write(s[0],9,spec.track,24,{color:'#FFFFFF'});
 write(s[0],11,'17 October 2026',24,{color:'#FFFFFF'});
 write(s[1],5,spec.pain);write(s[1],7,spec.market);
 write(s[2],5,spec.solution);
 write(s[2],6,'',20); text(s[2],'Proposed flow label',spec.key.includes('H4')?'Proposed review flow':'Proposed role views',58,377,840,25,18,true);
 diagram(s[2],spec.flow,72,412,816,60,true);
 write(s[3],5,spec.steps,18);
 write(s[3],7,'');diagram(s[3],spec.architecture,527,157,365,222);
 text(s[3],'Build plan',spec.plan,56,410,848,90,18);
 for(let k=0;k<3;k++){
  const [name,problem,mitigation]=spec.challenges[k];
  write(s[4],[4,7,10][k],`Challenge ${k+1}: ${name}`,22,{bold:true});
  write(s[4],[5,8,11][k],[problem,mitigation],18,{spaceAfter:3});
 }
 [6,9,12].forEach((id,k)=>write(s[5],id,spec.usp[k],20,{align:'center'}));
 write(s[5],14,spec.advantage,20);
 write(s[6],4,'Live Demonstration: proposed walkthrough',25,{color:blue,bold:true});
 write(s[6],6,spec.demo,19,{spaceAfter:12}).position={left:159,top:167,width:642,height:273};
 write(s[6],7,'No video or measured results yet. Demo will follow implementation.',17,{align:'center'}).position={left:144,top:442,width:672,height:38};
 text(s[6],'Limitations',spec.limit,48,486,864,25,14);
 text(s[6],'AI disclosure','AI assistance: Gemini, Claude and ChatGPT/Codex for ideation and proposal drafting.',48,514,864,22,13);
 for(let i=0;i<7;i++)s[i].speakerNotes.text=`Source: official problem statement, ${spec.source}\nOfficial seven-slide template linked under this problem on the InnoSmart portal, reviewed 17 October 2026.\nThis is a proposed design. Implementation, testing and performance measurements are planned. Initial audience and adoption path are hypotheses, not measured market estimates. Build timing and permitted tools remain subject to organizer rules.`;
 const candidate=path.join(root,'tmp/ppt-build',`${spec.key}.pptx`);
 await (await PresentationFile.exportPptx(p)).save(candidate);
 const final=path.join(root,'submissions',`SENTINEX_${spec.key}.pptx`);
 const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','9144000,5143500','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:7,fontPolicy:{basis:'reference',families:['Calibri'],referencePath:source,referenceSha256:createHash('sha256').update(await fs.readFile(source)).digest('hex')},verifyArtifactToolImport:true,receiptPath:path.join(root,'tmp/ppt-build',`SENTINEX_${spec.key}.validation.json`)});
 console.log(JSON.stringify({deck:spec.key,result}));
}


