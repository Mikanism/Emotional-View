from email import header
from fileinput import filename
import streamlit as st
import pandas as pd
import datetime as dt
import os
import csv
import io

def timme(a):
    if a == 1:
        start = "00:00:00"
        end = "23:59:59"
        times = []
        start = now = dt.datetime.strptime(start, "%H:%M:%S")
        end = dt.datetime.strptime(end, "%H:%M:%S")
        while now != end:
            times.append(str(now.strftime("%H:%M:%S")))
            now += dt.timedelta(seconds = 1)
        times.append(end.strftime("%H:%M:%S"))
        return(times)
    else:
        start = "00:00"
        end = "59:59"
        times = []
        start = now = dt.datetime.strptime(start, "%M:%S")
        end = dt.datetime.strptime(end, "%M:%S")
        while now != end:
            times.append(str(now.strftime("%M:%S")))
            now += dt.timedelta(seconds = 1)
        times.append(end.strftime("%M:%S"))
        return(times)

#-------------------------------------------#

head = ['date','ans1','ans2','ans3','ans4','ans5','ans6','time','weight','opinion']
df = pd.DataFrame(columns=head)
if os.path.isfile('ans1.csv') == False:
    df.to_csv('ans1.csv', encoding='utf-8-sig', header = head, index = False, sep = ';')



st.title('Emotional View')

with st.form("my_form", clear_on_submit = True):
    k1, k2 = st.columns(2)
    with k1:
        date = st.date_input(
            "1. Дата обращения за услугой:",
            dt.datetime.now())
        time = st.selectbox('2. Время предоставления услуги:',timme(2))

    with k2:
        time_2 = st.selectbox('Время обращения за услугой:',timme(1)) 

    dttime =  str(date).split('-')
    dttime = dttime[2]+'.'+dttime[1]+'.'+dttime[0]+' '+time_2    
    

    q3 = st.radio(
        "3. Сколько времени Вы затратили на ожидание в очереди при обращении в МФЦ за получением услуги:",
        ('Не ждал', 'Ждал, но не долго (Менее 15 минут)', 'Долго ждал (Более 15 минут)'))

    q4 = st.radio(
        "4. Оцените вежливость и компетентность сотрудника, взаимодействующего с Вами при предоставлении услуг:",
        ('Удовлетворён', 'Скорее удовлетворён, чем не удовлетворён', 'Не удовлетворён'))

    q5 = st.radio(
        "5. В случае обращения за консультацией к сотруднику МФЦ, были Вы удовлетворены качеством и полнотой полученной информации:",
        ('Удовлетворён', 'Скорее удовлетворён, чем не удовлетворён', 'Не удовлетворён','За консультацией не обращался'))

    q6 = st.radio(
        "6. Оцените комфортность условий в помещении, в котором предоставлены Вам услуги:",
        ('Удовлетворён', 'Скорее удовлетворён, чем не удовлетворён', 'Не удовлетворён'))

    q7 = st.radio(
        "7. Оцените доступность информации о порядке предоставления Вам услуги:",
        ('Удовлетворён', 'Скорее удовлетворён, чем не удовлетворён', 'Не удовлетворён'))

    q8 = st.radio(
        "8. Была ли на Вас маска?",
        ('Да','Нет'))

    q9 = st.text_input('9. Вопрос для оператора: Какие эмоции клиент испытывал во время приёма?','')


    ans1, ans2, ans3, ans4, ans5, ans6 = q3, q4, q5, q6, q7, q8
    ans7 = q9
    
    upload = st.form_submit_button("Cохранить")

if upload:
    weight = 0
    weight_mass = [ans1, ans2, ans3, ans4, ans5]
    for i in range(len(weight_mass)):
        if weight_mass[i] == "Не ждал" or \
            weight_mass[i] == "Удовлетворён":
            weight += 1
        elif weight_mass[i] == "Долго ждал (Более 15 минут)" or \
            weight_mass[i] == "Не удовлетворён":
            weight -= 1
        else:
            weight += 0
    
    df.loc[len(df.index)] = [dttime, ans1, ans2, ans3, ans4, ans5, ans6, time, weight/5, ans7]
    df.dropna(axis=0, inplace=True)

    #df.to_csv('ans.csv',encoding='utf-8-sig', header = head, index = False, sep = ';')
    
    with open('ans1.csv','a', newline='', encoding='utf-8-sig',) as csvfile:
        writer = csv.writer(csvfile, delimiter = ';')
        writer.writerow([dttime, ans1, ans2, ans3, ans4, ans5, ans6, time, weight/5, ans7])
    
with st.expander(""):   
    st.write(pd.read_csv('ans1.csv', encoding='utf-8-sig', sep=';'))

@st.cache
def convert_df(df):
    return df.to_csv(header = head, index = False, sep = ';').encode('utf-8-sig')

@st.cache
def opros(data_ans, data):
    for i in range(len(data_ans['date'])):
        time_start = data_ans['date'][i][11:].split(':')
        time_start = dt.timedelta(hours=int(time_start[0]), minutes=int(time_start[1]), seconds=int(time_start[2]))
        time_end = data_ans['time'][i].split(':')
        time_end = dt.timedelta(minutes=int(time_end[0]), seconds=int(time_end[1]))
        ttime = time_start + time_end
        if len(str(ttime)) == 7:
                ttime = '0' + str(ttime) 
        data_ans.loc[i,'time'] = data_ans['date'][i][:11] + ttime

    data_ans.rename(columns={'time': 'date_end'}, inplace=True) 
    #print(data_ans)

    data.columns = ['TIME','Path']
    for i in range(6):
        data.insert(i+2,f'ans{i+1}','')
    data.insert(8,'weight','')
    data.insert(9,'opinion','')

    sup_time = dt.timedelta(minutes = 0, seconds = 1)
    for j in range(len(data_ans['date'])):
        
        while data_ans['date'][j] not in list(data['TIME']):
            sp_time = data_ans['date'][j][11:].split(':')
            sp_time = dt.timedelta(hours=int(sp_time[0]), minutes=int(sp_time[1]), seconds=int(sp_time[2]))
            sp_time += sup_time

            if len(str(sp_time)) == 7:
                sp_time = '0' + str(sp_time) 
                
            data_ans.loc[j,'date'] = data_ans['date'][j][:11] + sp_time

        for i in range(len(data['TIME'])):
            try:
                if data['TIME'][i] == data_ans['date'][j] and data['TIME'][i] != data['TIME'][i-1]:
                    for m in range(6):
                        data[f'ans{m+1}'][i] = data_ans[f'ans{m+1}'][j]
                        data['weight'][i] = data_ans['weight'][j]
                        data['opinion'][i] = data_ans['opinion'][j]
                if data['TIME'][i] == data_ans['date_end'][j] and data['TIME'][i] != data['TIME'][i+1]:
                    data['ans1'][i] = "END"
            except KeyError:
                if data['TIME'][i] == data_ans['date'][j]:
                    for m in range(6):
                        data[f'ans{m+1}'][i] = data_ans[f'ans{m+1}'][j]
                        data['weight'][i] = data_ans['weight'][j]
                        data['opinion'][i] = data_ans['opinion'][j]

    #print(data)
    head = data.columns
    data.to_csv('file2.csv',encoding='utf-8-sig', header = head, index = False, sep = ';')
    return data

data1 = convert_df(pd.read_csv('ans1.csv',sep=';'))

with st.sidebar:
    tab1, tab2 = st.tabs(["1", "2"])
    with tab1:
        st.header('Для скачивания файла нажмите на кнопку')
        st.download_button(
            'Скачать',
            data = data1,
            file_name='ans1.csv',
            on_click= df.to_csv('ans1.csv', encoding='utf-8-sig', header = head, index = False, sep = ';'))
    
    with tab2:
        st.header('Для совмещения файлов выберите 2 файла')
        uploaded_file = st.file_uploader("Выберите файл c результатами анкеты")
        if uploaded_file is not None:

            # Can be used wherever a "file-like" object is accepted:
            data_ans = pd.read_csv(uploaded_file, sep = ";")
            #st.write(data_ans)
        
        uploaded_file1 = st.file_uploader("Выберите файл с результатами нейросети")
        if uploaded_file1 is not None:

            # Can be used wherever a "file-like" object is accepted:
            data = pd.read_csv(uploaded_file1, sep = ";", header = None)
            #st.write(data)
        
        if uploaded_file is not None and uploaded_file1 is not None:
            data2 = convert_df(opros(data_ans, data))
            st.download_button(
                'Совместить',
                data = data2,
                file_name = 'file2.csv')
