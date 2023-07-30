import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import io


st.set_page_config(
     page_title="Gelato Balancer",
     page_icon='🍨',
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'About': "### Visit us: https://www.illva.com/"})




st.markdown("<h2 style='text-align: center'>G E L A T O &nbsp  🍨 &nbsp B A L A N C E</h2>", unsafe_allow_html=True)

cola,colb=st.columns([1,3.5])
with colb:
     #st.header('G E L A T O  🍨  B A L A N C E')
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     
col0,col00,col000=st.columns([0.5,0.5,1])

with col0:
    conta_ingredienti = st.number_input('How many ingredients?',value=1,min_value=1)
with col00:
     conta_gelato = st.number_input('How much gelato? (kg)', value=1.0, min_value=0.0, step=0.5)

          


col1,col2=st.columns([2,1])

#st.cache(allow_output_mutation=True)
def datab():
     db=pd.read_excel('database2.xlsx')
     db=db.set_index('INGREDIENTI')
     db=db.replace(',','.',regex=True)
     return db

db=datab()     
     
st.sidebar.image('gelato_drop.png', width=60) 


with col1:
    st.markdown('#### Ingredient')
with col2:
    st.markdown('#### Quantity (g)')   
    

#---------------------------------  
    


d = {'Ingredients': [], 'Quantity': [], 'Sugars': [], 'Fats':[], 'Proteins':[], 'PAC':[], 'POD':[],  'Solids':[], 'kcal':[]}

i = 0.0
j = 100

if st.button('clear'):
     conta_ingredienti = 1
     
while(i < conta_ingredienti and j < conta_ingredienti+100):



 with col1:
     ingrediente=st.selectbox('',db,index=0,key=i)
     d['Ingredients'].append(ingrediente)

 with col2:
     quantità=st.number_input('',value=0.0,key=j, step=10.0)
     d['Quantity'].append(quantità)


 sugar=float((db.loc[ingrediente,'ZUCCHERI']))
 sugar_prc=sugar*quantità
 d['Sugars'].append(sugar_prc)

 pod=float((db.loc[ingrediente,'POD']))
 pod_prc=pod*quantità
 d['POD'].append(pod_prc)

 pac=float((db.loc[ingrediente,'PAC']))
 pac_prc=pac*quantità
 d['PAC'].append(pac_prc)

 fats=float((db.loc[ingrediente,'GRASSI']))
 fats_prc=fats*quantità 
 d['Fats'].append(fats_prc)


 prot=float((db.loc[ingrediente,'PROTEINE']))
 prot_prc=prot*quantità 
 d['Proteins'].append(prot_prc)

 solids=float((db.loc[ingrediente,'SOLIDI TOTALI']))
 solids_prc=solids*quantità 
 d['Solids'].append(solids_prc)  

 kcal = float((db.loc[ingrediente,'CALORIE']))  
 d['kcal'].append(kcal*quantità)

 i += 1
 j += 1
 

df1 = pd.DataFrame(d)
df1=df1.set_index('Ingredients')
df = df1/df1['Quantity'].sum()*1000*conta_gelato
prc_calc=(df['Quantity'] / df['Quantity'].sum()) * 100
df.insert(1, '%', prc_calc)
df=df.fillna(0.0)


df_prc = df/df.sum()
df_prc=df_prc.fillna(0.0)


d_tot = {}
for colonna in df:
    d_tot[colonna] = df[colonna].sum()

df_tot = pd.DataFrame(d_tot, index=['Totals']).drop(['%'],axis=1)

df_prc = df_tot/df_tot['Quantity'].sum()*100
df_prc = df_prc.rename(index={'Totals':'Percentage'})
df_prc=df_prc.fillna(0.0)



df=df.iloc[:,0:8]

with col2:
    somma = df1['Quantity'].sum()
    st.subheader(' %s g' %somma)

st.table(df.style.format({'%' : '{:1,.2f} %','Quantity': '{:1,.2f} g','Sugars': '{:1,.2f} g',
                            'Fats': '{:1,.2f} g','PAC': '{:1,.2f}', 'POD': '{:1,.2f}', 'Proteins': '{:1,.2f} g', 
                            'Solids': '{:1,.2f} g','kcal': '{:1,.2f}'}))
st.title('')

st.table(df_tot.style.format({'Quantity': '{:1,.2f} g','Sugars': '{:1,.2f} g',
                            'Fats': '{:1,.2f} g','PAC': '{:1,.2f}','POD': '{:1,.2f}','Proteins': '{:1,.2f} g', 
                            'Solids': '{:1,.2f} g','kcal': '{:1,.2f}'}).set_properties(**{'background-color': 'green','color': 'white'}))
st.subheader('')
st.table(df_prc.style.format({'Quantity': '{:2,.2f} %','Sugars': '{:1,.2f} %',
                            'Fats': '{:1,.2f} %','PAC': '{:1,.2f} %','POD': '{:1,.2f} %','Proteins': '{:1,.2f} %','Solids': '{:1,.2f} %','kcal': '{:1,.2f}'}).set_properties(**{'background-color': '#36a5ff','color': 'white'}))

     




#------------CALCOLO ACQUA-------------------------------------------------------

wt=df_tot['Quantity']-df_tot['Solids']

#Moli di acqua
wt_mol=wt/18+0.00000001

#Moli SE
se_mol=df_tot['PAC']/342

#Calcolo attività dell'acqua
aw=wt_mol/(se_mol+wt_mol)

#Calcolo FPD
ln_aw=np.log(aw)
fpd=103.22*ln_aw

st.header('')

col1_s,col2_s,col3_s=st.columns([3,3,2])

with col2_s:
    st.header('')
    #st.metric(label='Water activity',value='%.3f'%aw)
    
with col3_s:
    st.header('')
    st.metric('Freezing Point', value='%.2f °C'%fpd,delta='')

     
st.sidebar.subheader('My recipe')



 



    
