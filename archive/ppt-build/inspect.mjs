import fs from 'node:fs/promises';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('references/official/shared-template.pptx'));
await fs.writeFile('tmp/ppt-build/inspection.txt',(await p.inspect({kind:'slide,textbox,shape,layout',maxChars:100000})).ndjson);
await fs.writeFile('tmp/ppt-build/layout.json',JSON.stringify(p.slides.items.map(s=>({id:s.id,shapes:s.shapes.items.map(x=>({id:x.id,name:x.name,text:x.text.toString(),position:x.position,style:x.text.style}))})),null,2));
await (await PresentationFile.exportPptx(p)).save('tmp/ppt-build/roundtrip.pptx');
console.log('Imported',p.slides.items.length,'slides');
