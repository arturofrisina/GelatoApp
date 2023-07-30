import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import io


st.set_page_config(
     page_title="Gelato Balance",
     page_icon='🍨',
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'About': "Creato da Arturo Frisina"})




st.markdown("<h2 style='text-align: center'>G E L A T O &nbsp  🍨 &nbsp B A L A N C E</h2>", unsafe_allow_html=True)

cola,colb=st.columns([1,3.5])
with colb:
     #st.header('G E L A T O  🍨  B A L A N C E')
     st.title('')
     st.title('')
     st.title('')
     st.title('')

nome_ricetta = st.text_input('Inserisci il nome della ricetta','Nuova ricetta')     
     
col0,col00,col000=st.columns([0.5,0.5,1])

with col0:    
    conta_ingredienti = st.number_input('Quanti Ingredienti?',value=1,min_value=1)
with col00:
     conta_gelato = st.number_input('Quanto gelato? (kg)', value=1.0, min_value=0.0, step=0.5)



col1,col2=st.columns([2,1])

@st.cache(allow_output_mutation=True)
def datab():
     db=pd.read_excel('database_free.xlsx')
     db=db.set_index('INGREDIENTI')
     db=db.replace(',','.',regex=True)
     return db

db=datab()     
     
st.sidebar.image('gelato_drop.png', width=60) 

with col1:
    st.markdown('#### Ingredienti')
with col2:
    st.markdown('#### Quantità (g)')   
    

#---------------------------------  
   

d = {'Ingredienti': [], 'Quantità': [], 'Zuccheri': [],'SLNG':[], 'Grassi':[], 'Proteine':[], 'PAC':[], 'POD':[],  'Solidi':[], 'kcal':[]}

i=0.0

     
while(i<conta_ingredienti):

 with col1:
     ingrediente=st.selectbox('',db,index=0,key=i)
     d['Ingredienti'].append(ingrediente)

 with col2:
     quantità=st.number_input('',value=0.0,key=i, step=10.0)
     d['Quantità'].append(quantità)


 sugar=float((db.loc[ingrediente,'ZUCCHERI']))
 sugar_prc=sugar*quantità
 d['Zuccheri'].append(sugar_prc)

 pod=float((db.loc[ingrediente,'POD']))
 pod_prc=pod*quantità
 d['POD'].append(pod_prc)

 pac=float((db.loc[ingrediente,'PAC']))
 pac_prc=pac*quantità
 d['PAC'].append(pac_prc)

 slng=float((db.loc[ingrediente,'SLNG']))
 slng_prc=slng*quantità 
 d['SLNG'].append(slng_prc)

 Grassi=float((db.loc[ingrediente,'GRASSI']))
 Grassi_prc=Grassi*quantità 
 d['Grassi'].append(Grassi_prc)


 prot=float((db.loc[ingrediente,'PROTEINE']))
 prot_prc=prot*quantità 
 d['Proteine'].append(prot_prc)

 Solidi=float((db.loc[ingrediente,'SOLIDI TOTALI']))
 Solidi_prc=Solidi*quantità 
 d['Solidi'].append(Solidi_prc)  

 kcal = float((db.loc[ingrediente,'CALORIE']))  
 d['kcal'].append(kcal*quantità)



 i=i+1
 



df1 = pd.DataFrame(d)
df1=df1.set_index('Ingredienti')
df = df1/df1['Quantità'].sum()*1000*conta_gelato
prc_calc=(df['Quantità'] / df['Quantità'].sum()) * 100
df.insert(1, '%', prc_calc)
df=df.fillna(0.0)


df_prc = df/df.sum()
df_prc=df_prc.fillna(0.0)


d_tot = {}
for colonna in df:
    d_tot[colonna] = df[colonna].sum()

df_tot = pd.DataFrame(d_tot, index=['Totals']).drop(['%'],axis=1)

df_prc = df_tot/df_tot['Quantità'].sum()*100
df_prc = df_prc.rename(index={'Totals':'Percentage'})



df=df.iloc[:,0:8]

with col2:
    somma = df1['Quantità'].sum()
    st.subheader(' %s g' %somma)

st.table(df.style.format({'%' : '{:1,.2f} %','Quantità': '{:1,.2f} g','Zuccheri': '{:1,.2f} g','SLNG':'{:1,.2f} g',
                            'Grassi': '{:1,.2f} g','PAC': '{:1,.2f}', 'POD': '{:1,.2f}', 'Proteine': '{:1,.2f} g', 
                            'Solidi': '{:1,.2f} g','kcal': '{:1,.2f}'}))
st.title('')

st.table(df_tot.style.format({'Quantità': '{:1,.2f} g','Zuccheri': '{:1,.2f} g','SLNG':'{:1,.2f} g',
                            'Grassi': '{:1,.2f} g','PAC': '{:1,.2f}','POD': '{:1,.2f}','Proteine': '{:1,.2f} g', 
                            'Solidi': '{:1,.2f} g','kcal': '{:1,.2f}'}).set_properties(**{'background-color': 'green','color': 'white'}))
st.subheader('')
st.table(df_prc.style.format({'Quantità': '{:2,.2f} %','Zuccheri': '{:1,.2f} %','SLNG':'{:1,.2f} %',
                            'Grassi': '{:1,.2f} %','PAC': '{:1,.2f} %','POD': '{:1,.2f} %','Proteine': '{:1,.2f} %','Solidi': '{:1,.2f} %','kcal': '{:1,.2f}'}).set_properties(**{'background-color': '#36a5ff','color': 'white'}))

     




#------------CALCOLO ACQUA-------------------------------------------------------

wt=df_tot['Quantità']-df_tot['Solidi']

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

     
st.sidebar.subheader('La mia ricetta')


#---------------EXCEL-------------------------------------------


df=df.append(pd.Series(name=''))
df=df.append(df.sum().rename('Total'))
df['%']=df['%']/100
df_prc=df_prc.div(100)
df=df.append(df_prc)

buffer = io.BytesIO()
tot_row=i+3

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='New recipe')

    workbook  = writer.book
    worksheet = writer.sheets['New recipe']
    format1 = workbook.add_format({'num_format': '0.00%','bold':True})
    format2 = workbook.add_format({'num_format': '0.00%','bold':True,'font_color':'#8290FA'})
    format3 = workbook.add_format({'bold': True, 'font_color':'green'})

    worksheet.set_column(0, 0, 35)
    worksheet.set_column(2, 2, 15, format1 )
    worksheet.set_column(3, 8, 15 )
    worksheet.set_row(tot_row-1,15,format3)
    worksheet.set_row(tot_row,15,format2)


    writer.save()

    st.sidebar.download_button(
        label="Scarica ricetta",
        data=buffer,
        file_name=nome_ricetta+".xlsx",
        mime="application/vnd.ms-excel")
  
database=pd.DataFrame(db)

#st.sidebar.subheader('Database')

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    database.to_excel(writer, sheet_name='Database')

    workbook  = writer.book
    worksheet = writer.sheets['Database']

    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 5,None, {'hidden': True})
    worksheet.set_column(2,15,12)

    writer.save()
     
    #st.sidebar.download_button(
     #   label="Download database",
     #   data=buffer,
      #  file_name="Database.xlsx",
       # mime="application/vnd.ms-excel")     

    
col0,col00,col000=st.columns([3,4,1])

with col00:
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     st.title('')
     #st.image('DSI_logo.png', width=200)
 



    