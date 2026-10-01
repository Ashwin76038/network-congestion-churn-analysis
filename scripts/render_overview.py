"""Render a Python figure of the frozen synthetic usage scenario."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False})
n=pd.read_csv(ROOT/'data/clean/olt_daily_metrics.csv');rates=n.groupby('olt_id').congestion_ratio.mean().sort_values()
fig,(a,b)=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1.3,1]})
bars=a.barh([f'OLT {i:02d}' for i in rates.index],rates.values*100,color='#2463a0');a.bar_label(bars,labels=[f'{x:.1%}' for x in rates],padding=5,fontsize=10);a.set_xlim(0,max(rates)*125);a.set_xlabel('Simulated daily-average utilization (%)');a.set_title('Ten simulated OLT IDs | daily average',loc='left',pad=15,fontweight='bold')
b.axis('off');b.text(0,.90,'5 simulated dates',fontsize=23,fontweight='bold');b.text(0,.79,'14 consecutive days required for the rule',fontsize=12);b.text(0,.59,'Full score: unavailable',fontsize=21,fontweight='bold',color='#986921');b.text(0,.48,'No account has two complete seven-day windows.',fontsize=11);b.text(0,.29,'Ten chosen usage IDs',fontsize=20,fontweight='bold');b.text(0,.18,'1,135 source/simulation assignments differ.\nThis is a join-compatibility check.',fontsize=11,linespacing=1.6)
fig.suptitle('Simulated network metrics and rule readiness',x=.06,ha='left',fontsize=23,fontweight='bold');fig.text(.06,.89,'1,280 row-labeled accounts  |  6,400 synthetic account-days  |  1-5 August 2026',fontsize=12,color='#475569')
fig.text(.06,.065,'Source: frozen Excel-generated usage CSVs; complaints are synthetic. Capacity inputs are scenario assumptions.',fontsize=10,color='#475569');fig.text(.06,.035,'Python simulation figure; Power BI Desktop validation pending. No measured churn or network outcome is established.',fontsize=10,color='#475569')
fig.subplots_adjust(left=.09,right=.96,top=.78,bottom=.18,wspace=.3)
(ROOT/'images').mkdir(exist_ok=True);fig.savefig(ROOT/'images/01-network-overview.png',dpi=150,facecolor='white')
