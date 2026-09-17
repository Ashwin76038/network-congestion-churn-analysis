from pathlib import Path
import json, shutil, hashlib, re, uuid
import pandas as pd

ROOT=Path(r'C:\Users\Admin\Documents\Network Congestion and Churn analysis')
OLD=ROOT/'dashboard'/'OLT_Automation'
NEW=ROOT/'dashboard'/'OLT_Professional_Project'
REPORT=NEW/'OLT.Report'
MODEL=NEW/'OLT.SemanticModel'
S='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/'
def dump(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2),encoding='utf-8')
def lit(v): return {'expr':{'Literal':{'Value':str(v).lower() if isinstance(v,bool) else str(v)+'D' if isinstance(v,(int,float)) else "'"+v.replace("'","''")+"'"}}}
def color(v): return {'solid':{'color':lit(v)}}
def obj(**p): return [{'properties':p}]
def f(t,c,m=False): return {('Measure' if m else 'Column'):{'Expression':{'SourceRef':{'Entity':t}},'Property':c}}
def proj(t,c,m=False,label=None): return {'field':f(t,c,m),'queryRef':t+'.'+c,'nativeQueryRef':c,**({'displayName':label} if label else {})}
def mp(c,label=None): return proj('_Measures',c,True,label)
if not NEW.exists():
    NEW.mkdir(parents=True)
    shutil.copytree(OLD/'OLT.SemanticModel',MODEL,ignore=shutil.ignore_patterns('.platform'))
    shutil.copytree(OLD/'OLT.Report'/'StaticResources',REPORT/'StaticResources')
    shutil.copytree(OLD/'data',NEW/'data')
    dump(REPORT/'definition.pbir',{'version':'4.0','datasetReference':{'byPath':{'path':'../OLT.SemanticModel'}}})
    dump(NEW/'OLT_Churn_Network_Risk_Professional.pbip',{'version':'1.0','artifacts':[{'report':{'path':'OLT.Report'}}],'settings':{'enableAutoRecovery':True}})
# Preserve the established TMDL model; only redirect its existing CSV paths to the working project.
for p in (MODEL/'definition'/'tables').glob('*.tmdl'):
    content=p.read_text(encoding='utf-8')
    revised=content.replace(str(OLD/'data'),str(NEW/'data'))
    if revised!=content: p.write_text(revised,encoding='utf-8')
extra={
'Avg Downtime Minutes':('AVERAGE(customer_daily_metrics[downtime_minutes])','0.0'),
'Avg Latency Ms':('AVERAGE(customer_daily_metrics[latency_ms])','0.0'),
'Avg Risk Score':('AVERAGE(customer_daily_metrics[churn_risk_score])','0.0'),
'Max Risk Score':('MAX(customer_daily_metrics[churn_risk_score])','0'),
'Total Usage GB':('SUM(usage_logs_clean[data_usage_gb])','#,0'),
'Utilization Status':('VAR R=[Avg Congestion Ratio] RETURN IF(ISBLANK(R),"No telemetry",SWITCH(TRUE(),R<0.6,"Healthy",R<=0.8,"Moderate","High"))',''),
'Utilization Color':('VAR R=[Avg Congestion Ratio] RETURN IF(ISBLANK(R),"#94A3B8",SWITCH(TRUE(),R<0.6,"#149C8B",R<=0.8,"#E5A028","#D94668"))',''),
'Network Coverage Summary':('FORMAT([Monitored OLTs],"0") & " / " & FORMAT([Total OLTs],"0") & " OLTs monitored | 24h average estimate; peak congestion unavailable"',''),
'Executive Insight':('FORMAT([High Risk Customers],"0") & " customers had high-risk observations. " & FORMAT([Complaint Leakage Customers],"0") & " complaint leakage cases in the selected period."',''),
'Worst Risk Customers':('VAR Category = SELECTEDVALUE(customer_daily_metrics[churn_risk_category]) VAR PerCustomer = CALCULATETABLE(SUMMARIZE(customer_daily_metrics,customer_daily_metrics[customer_id],"Worst",MAX(customer_daily_metrics[churn_risk_score])),ALLSELECTED(customer_daily_metrics[churn_risk_category])) RETURN COUNTROWS(FILTER(PerCustomer,SWITCH(TRUE(),[Worst]>=70,"High Risk",[Worst]>=40,"Medium Risk","Low Risk")=Category))','#,0'),
}
measurefile=MODEL/'definition'/'tables'/'_Measures.tmdl'
content=measurefile.read_text()
for n,(e,fmt) in extra.items():
    if "measure '"+n+"' =" not in content:
        content+='\n\tmeasure \''+n+"' = "+e+'\n'+('\t\tformatString: '+fmt+'\n' if fmt else '')+'\t\tdisplayFolder: Professional Diagnostics\n\t\tlineageTag: '+str(uuid.uuid4())+'\n'
measurefile.write_text(content,encoding='utf-8')
base=json.loads((OLD/'OLT.Report'/'definition'/'report.json').read_text())
base['themeCollection']['customTheme']['name']='OLTProfessional'
base['resourcePackages']=[p for p in base['resourcePackages'] if p['type']!='RegisteredResources']+[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'OLTProfessional','path':'OLTProfessional.json','type':'CustomTheme'}]}]
theme={'name':'OLTProfessional','dataColors':['#D94668','#149C8B','#E5A028','#1666C0','#6C4CCF'],'background':'#FFFFFF','foreground':'#25334A','tableAccent':'#1666C0','visualStyles':{'*':{'*':{'title':[{'color':{'solid':{'color':'#25334A'}},'fontSize':13}],'categoryAxis':[{'labelColor':{'solid':{'color':'#52617A'}}}],'valueAxis':[{'labelColor':{'solid':{'color':'#52617A'}}}],'legend':[{'labelColor':{'solid':{'color':'#52617A'}}}]}}}}
dump(REPORT/'StaticResources'/'RegisteredResources'/'OLTProfessional.json',theme)
dump(REPORT/'definition'/'report.json',base)
dump(REPORT/'definition'/'version.json',{'$schema':S+'versionMetadata/1.0.0/schema.json','version':'2.0.0'})
pages=[('executive','Executive Overview'),('diagnostics','Network & Churn Analysis')]
dump(REPORT/'definition'/'pages'/'pages.json',{'$schema':S+'pagesMetadata/1.0.0/schema.json','pageOrder':[p[0] for p in pages],'activePageName':'executive'})
count=0
V={}
def visual(page,name,kind,x,y,w,h,title='',roles=None,objects=None):
    global count
    count+=1; name=page+'_'+name
    v={'$schema':S+'visualContainer/2.7.0/schema.json','name':name,'position':{'x':x,'y':y,'width':w,'height':h,'z':count,'tabOrder':count},'visual':{'visualType':kind,'drillFilterOtherVisuals':True,'visualContainerObjects':{'background':obj(show=lit(True),color=color('#FFFFFF'),transparency=lit(0)),'border':obj(show=lit(True),color=color('#DFE5EF'),radius=lit(6)),'title':obj(show=lit(bool(title)),text=lit(title),fontColor=color('#25334A'),fontSize=lit(13)),'subTitle':obj(show=lit(False))}}}
    if roles: v['visual']['query']={'queryState':{k:{'projections':p} for k,p in roles.items()}}
    if objects: v['visual']['objects']=objects
    V[name]=v
    return v
def text(page,name,string,x,y,w,h,size=12,c='#52617A'):
    v=visual(page,name,'textbox',x,y,w,h,objects={'general':obj(paragraphs=[{'textRuns':[{'value':string,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'pt','color':c}}]}])})
    v['visual']['visualContainerObjects']={'background':obj(show=lit(False)),'border':obj(show=lit(False))}
    return v
def button(page,name,label,x,w,target,reset=False):
    active=target==page and not reset
    v=visual(page,name,'actionButton',x,83,w,43,objects={'text':[{'selector':{'id':'default'},'properties':{'show':lit(True),'text':lit(label),'fontColor':color('#FFFFFF' if active else '#1666C0'),'fontSize':lit(12)}}],'fill':[{'selector':{'id':'default'},'properties':{'show':lit(True),'fillColor':color('#1666C0' if active else '#FFFFFF')}}],'icon':obj(show=lit(False))})
    v['visual']['visualContainerObjects']['visualLink']=obj(show=lit(True),type=lit('Bookmark' if reset else 'PageNavigation'),**({'bookmark':lit('resetFilters')} if reset else {'navigationSection':lit(target)}))
    v['visual']['objects']['text'].append({'properties':{'show':lit(True)}})
    return v
def card(page,name,measure,label,x,y,w,h=106,c='#1666C0',size=28):
    return visual(page,name,'card',x,y,w,h,label,{'Values':[mp(measure)]},{'labels':obj(color=color(c),fontSize=lit(size),labelDisplayUnits=lit(0)),'categoryLabels':obj(show=lit(False))})
def axes():
    return {'categoryAxis':obj(showAxisTitle=lit(False),labelColor=color('#52617A'),fontSize=lit(10)),'valueAxis':obj(showAxisTitle=lit(False),labelColor=color('#52617A'),fontSize=lit(10)),'labels':obj(show=lit(True),color=color('#25334A'),fontSize=lit(10),labelPrecision=lit(1),labelDisplayUnits=lit(0)),'legend':obj(show=lit(False))}
def sort(v,t,c,m=True,descending=True): v['visual']['query']['sortDefinition']={'sort':[{'field':f(t,c,m),'direction':'Descending' if descending else 'Ascending'}]}
def network(page,x,y,w,h,title):
    o=axes(); o['dataPoint']=obj(defaultColor={'solid':{'color':{'expr':f('_Measures','Utilization Color',True)}}}); o['categoryAxis'][0]['properties']['minimumCategoryWidth']=lit(12)
    v=visual(page,'network','barChart',x,y,w,h,title,{'Category':[proj('olt_info_clean','olt_id',label='OLT')],'Y':[mp('Avg Congestion Ratio','Average utilization')],'Tooltips':[mp('Utilization Status'),mp('Capacity Gbps'),mp('Average Throughput Gbps')]},o)
    sort(v,'_Measures','Avg Congestion Ratio');return v
for page,title in pages:
    dump(REPORT/'definition'/'pages'/page/'page.json',{'$schema':S+'page/2.1.0/schema.json','name':page,'displayName':title,'displayOption':'FitToPage','width':1600,'height':900,'objects':{'background':obj(color=color('#F3F6FB'),transparency=lit(0))}})
    text(page,'title','OLT Network Intelligence',28,17,980,54,28,'#25334A')
    text(page,'tag','NETWORK HEALTH  /  EXPERIENCE  /  RETENTION',1040,31,530,32,11,'#6C4CCF')
    button(page,'navExecutive','Executive Overview',28,244,'executive')
    button(page,'navDiagnostics','Network & Churn Analysis',284,290,'diagnostics')
    button(page,'reset','Reset Filters',1402,170,page,True)
    for i,(label,t,c) in enumerate([('Date','DateTable','Date'),('Plan Tier','plans_clean','plan_tier'),('Value Segment','customers_clean','value_segment'),('OLT ID','olt_info_clean','olt_id'),('Risk Category','customer_daily_metrics','churn_risk_category')]):
        v=visual(page,'slicer'+str(i),'slicer',28+i*311,142,300,68,label,{'Values':[proj(t,c)]},{'data':obj(mode=lit('Between' if i==0 else 'Dropdown')),'header':obj(show=lit(False)),'items':obj(fontColor=color('#25334A'),background=color('#FFFFFF'),textSize=lit(11)),'date':obj(fontColor=color('#25334A'),background=color('#FFFFFF'),fontSize=lit(10))})
        v['visual']['syncGroup']={'groupName':'Shared_'+c,'fieldChanges':True,'filterChanges':True}
    kpis=[('Total Customers','Total Customers','#1666C0'),('% High Risk Customers','High Risk Customers %','#D94668'),('Avg Experience Score','Avg Experience Score','#149C8B'),('Complaint Leakage Customers','Complaint Leakage','#6C4CCF'),('Avg Congestion Ratio','Avg Utilization (24h)','#1666C0'),('High Congestion OLTs','High Utilization OLTs','#D94668')] if page=='executive' else [('Total OLTs','Total OLTs','#1666C0'),('High Congestion OLTs','High Utilization OLTs','#D94668'),('Avg Congestion Ratio','Avg Utilization (24h)','#1666C0'),('High Risk Customers','High Risk Customers','#D94668'),('Avg Downtime Minutes','Avg Downtime / min','#6C4CCF'),('Avg Latency Ms','Avg Latency / ms','#149C8B')]
    for i,(m,label,c) in enumerate(kpis): card(page,'kpi'+str(i),m,label,28+260*i,228,248,c=c)
    text(page,'limits','24h utilization estimate, not peak congestion | 10/12 OLTs observed | Assigned/logged OLT mismatch: 1,135 customers | Rule-based risk; not a churn prediction',28,866,1544,25,10,'#6A5870')
network('executive',28,352,486,443,'OLT Congestion Overview')
o=axes();o['valueAxis'][0]['properties'].update(start=lit(0),end=lit(100));o['categoryAxis'][0]['properties']['axisType']=lit('Categorical');o['dataPoint']=obj(defaultColor=color('#1666C0'))
v=visual('executive','experience','lineChart',532,352,1040,209,'Customer Experience Trend',{'Category':[proj('DateTable','Date')],'Y':[mp('Avg Experience Score')]},o);sort(v,'DateTable','Date',False,False)
o=axes();o['legend']=obj(show=lit(True),position=lit('Top'),showTitle=lit(False),labelColor=color('#52617A'),fontSize=lit(10))
visual('executive','riskSegment','columnChart',532,579,614,216,'Churn Risk by Customer Value Segment',{'Category':[proj('customers_clean','value_segment',label='Value segment')],'Series':[proj('customer_daily_metrics','churn_risk_category')],'Y':[mp('Worst Risk Customers','Customers')]},o)
visual('executive','riskDistribution','donutChart',1164,579,408,216,'Customer Risk Distribution',{'Category':[proj('customer_daily_metrics','churn_risk_category')],'Y':[mp('Worst Risk Customers','Customers')]},{'legend':obj(show=lit(True),position=lit('Right'),showTitle=lit(False),labelColor=color('#52617A'),fontSize=lit(10)),'labels':obj(show=lit(True),color=color('#25334A'),fontSize=lit(10),labelDisplayUnits=lit(0))})
card('executive','insight','Executive Insight','',28,811,1544,43,c='#25334A',size=14)
network('diagnostics',28,352,465,385,'OLT Congestion Detail')
o=axes();o['legend']=obj(show=lit(True),position=lit('Top'),showTitle=lit(False),labelColor=color('#52617A'),fontSize=lit(10));o['labels']=obj(show=lit(False));o['categoryAxis'][0]['properties'].update(start=lit(0),end=lit(100));o['valueAxis'][0]['properties'].update(start=lit(0),end=lit(100))
visual('diagnostics','scatter','scatterChart',511,352,560,257,'Experience Score vs Churn Risk',{'Category':[proj('customers_clean','customer_id')],'Series':[proj('customer_daily_metrics','churn_risk_category')],'X':[mp('Avg Experience Score')],'Y':[mp('Avg Risk Score')],'Tooltips':[mp('Avg Downtime Minutes'),mp('Avg Latency Ms')]},o)
o=axes();o['dataPoint']=obj(defaultColor=color('#6C4CCF'))
visual('diagnostics','downtime','columnChart',1089,352,483,257,'Downtime by Risk Category',{'Category':[proj('customer_daily_metrics','churn_risk_category')],'Y':[mp('Avg Downtime Minutes')],'Tooltips':[mp('Avg Latency Ms'),mp('Avg Experience Score')]},o)
v=visual('diagnostics','attention','tableEx',511,627,1061,222,'Customers Requiring Attention',{'Values':[proj('customers_clean','customer_id',label='Customer ID'),proj('customers_clean','olt_id',label='Assigned OLT'),proj('customers_clean','value_segment',label='Value segment'),mp('Avg Experience Score','Experience'),mp('Max Risk Score','Risk score'),proj('customer_daily_metrics','churn_risk_category',label='Risk category')]},{'columnHeaders':obj(fontColor=color('#25334A'),backColor=color('#EAF0FA'),fontSize=lit(11)),'values':obj(fontColor=color('#25334A'),backColor=color('#FFFFFF'),fontSize=lit(11)),'grid':obj(gridVertical=lit(False),gridHorizontal=lit(True)),'total':obj(totals=lit(False))})
v['filterConfig']={'filters':[{'name':'highRiskOnly','field':f('customer_daily_metrics','churn_risk_category'),'type':'Categorical','filter':{'Version':2,'From':[{'Name':'d','Entity':'customer_daily_metrics','Type':0}],'Where':[{'Condition':{'In':{'Expressions':[{'Column':{'Expression':{'SourceRef':{'Source':'d'}},'Property':'churn_risk_category'}}],'Values':[[{'Literal':{'Value':"'High Risk'"}}]]}}}]}}]}
sort(v,'_Measures','Max Risk Score')
card('diagnostics','leakage','Leakage Status','Complaint Leakage',28,755,465,94,c='#149C8B',size=13)
bookmark={'$schema':S+'bookmark/1.4.0/schema.json','displayName':'Reset Filters','name':'resetFilters','options':{'suppressDisplay':True,'suppressActiveSection':True},'explorationState':{'version':'1.3','activeSection':'executive','sections':{}}}
for page,_ in pages:
    bookmark['explorationState']['sections'][page]={'visualContainers':{page+'_slicer'+str(i):{'filters':{'byName':{}},'singleVisual':{'visualType':'slicer','objects':{'remove':[{'object':'general','property':'filter','selector':{}}]}}} for i in range(5)}}
dump(REPORT/'definition'/'bookmarks'/'resetFilters.bookmark.json',bookmark)
dump(REPORT/'definition'/'bookmarks'/'bookmarks.json',{'$schema':S+'bookmarksMetadata/1.0.0/schema.json','items':[{'name':'resetFilters'}]})
for name,v in V.items(): dump(REPORT/'definition'/'pages'/name.split('_')[0]/'visuals'/name/'visual.json',v)
original=ROOT/'dashboard'/'OLT_Churn_Network_Risk.pbix'
manifest={'original_pbix':str(original),'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'working_pbix':str(ROOT/'dashboard'/'OLT_Churn_Network_Risk_Professional.pbix'),'completed':['Seven approved datasets and prior validation','Typed refreshable TMDL model','Existing DAX and active single-direction relationships','One-page PBIR prototype'],'partially_completed':['Reset button and visual QA','Portfolio documentation with stale numerical claims'],'not_completed_at_discovery':['Two-page light design','Final populated PBIX','Screenshot exports'],'professional_pages':[x[1] for x in pages],'visual_count':len(V),'added_measures':list(extra)}
dump(NEW/'build_manifest.json',manifest)
print(json.dumps(manifest,indent=2))
