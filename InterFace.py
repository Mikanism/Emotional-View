import streamlit as st
import pandas as pd
import datetime as dt
import os
import csv

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
    
    upload = st.form_submit_button("Загрузить")

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
    df1 = pd.read_csv('ans1.csv', encoding='utf-8-sig', sep=';')
    st.write(df1)
 

