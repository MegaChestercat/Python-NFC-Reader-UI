import serial
import tkinter
import keyboard as kb
from beepy import beep
import customtkinter as tk
import threading
import datetime
from pymongo import MongoClient
from pprint import pprint
from tkcalendar import *
import json

file = open("env.json")
env = json.load(file)

client = MongoClient(env["mongodb_uri"])
db = client["iot"]
tk.set_appearance_mode('light')
tk.set_default_color_theme('green')


root = tk.CTk()
root.title("ID Scanner")
root.geometry("780x500")
root.resizable(False, False)

settings_options = ["Acceso", "Asistencia", "Material", "Reservar Salón", "Gimnasio", "Pago Estacionamiento"]

entradas = ["Acceso Recta", "Acceso Periférico", "Acceso 14-O", "Acceso 14-O Canchas Tenis"]
clase_estado = ["Asistencia", "Retardo", "Falta"]

curso_secciones = []

def pick_date1(event):
    global cal, date_window
    date_window = tk.CTkToplevel()
    date_window.grab_set()
    date_window.title("Elige Fecha Inicio")
    date_window.geometry('250x220+590+370')
    cal = Calendar(date_window, selectmode='day', date_pattern='y/mm/dd')
    cal.place(x=30, y=20)
    
    submitBTN= tk.CTkButton(master=date_window, text='Seleccionar', command=grab_date1)
    submitBTN.place(x=60, y=180)
    
def pick_date2(event):
    global cal2, date_window2
    date_window2 = tk.CTkToplevel()
    date_window2.grab_set()
    date_window2.title("Elige Fecha Inicio")
    date_window2.geometry('250x220+590+370')
    cal2 = Calendar(date_window2, selectmode='day', date_pattern='y/mm/dd')
    cal2.place(x=30, y=20)
    
    submitBTN= tk.CTkButton(master=date_window2, text='Seleccionar', command=grab_date2)
    submitBTN.place(x=60, y=180)
    
def grab_date1():
    datePicker_var.set("")
    datePicker_var.set(cal.get_date())
    date_window.destroy()
    
def grab_date2():
    datePicker2_var.set("")
    datePicker2_var.set(cal2.get_date())
    date_window2.destroy()
       
def switch_event():
    if switch_var.get() == "off":
        tk.set_appearance_mode('light')
        switchTextVar.set('Dark Mode Off')
        
    elif switch_var.get() == 'on':
        tk.set_appearance_mode('dark')
        switchTextVar.set('Dark Mode On')

def buscar_curso():
    curso_secciones.clear()
    res = db["cursos"].find({"claveCurso": comboboxCurso_var.get()})
    if res != None:
        for doc in res:
            curso_secciones.append(doc["seccion"])
        seccion_combobox.configure(values=curso_secciones)
    else:
        panel.insert("end", text = 'El curso escrito no existe en la base de datos.\n')

def buscar_material():
    res = db["materials"].find_one({"id": material_variable.get().upper()})
    if res != None:
        if int(res["cantidad"]) == 0:
            panel.insert("end", text = f'El material escrito "{material_variable.get()}" ya no tiene elementos en stock.\n')
            material_variable.set("")
    else:
        material_variable.set("")
        panel.insert("end", text = 'El material escrito no existe en la base de datos.\n')

def ver_disp():
    salon = salon_variable.get()
    init_time = datePicker_var.get().replace("/", "-") + " " + timePicker_var.get()
    finish_time = datePicker2_var.get().replace("/", "-") + " " + timePicker2_var.get()
    query = db["reservaciones_salones"].find_one(
        {"$and": [{"salon": salon}, 
                  {"initial_time": init_time}, 
                  {"end_time": finish_time}]})
    
    query2 = db["reservaciones_salones"].find_one(
        {"$and": [{"salon": salon}, 
                  {"initial_time": init_time}]})
    
    if query != None:
        salon_variable.set("")
        datePicker_var.set("")
        datePicker2_var.set("")
        timePicker_var.set("")
        timePicker2_var.set("")
        panel.insert("end", text = 'El salón especificado ya se encuentra apartado para ese rango de tiempo.\n')
    elif query2 != None :
        salon_variable.set("")
        datePicker_var.set("")
        datePicker2_var.set("")
        timePicker_var.set("")
        timePicker2_var.set("")
        panel.insert("end", text = 'El salón especificado ya se encuentra apartado en esa tiempo inicial.\n')
    else:
        panel.insert("end", text = 'El salón especificado se encuentra disponible en ese rango de tiempo.\n')
     
def mode_callback(choice):
    if choice == "Acceso":
        curso_title.place_forget()
        curso_entry.place_forget()
        buscarCursoBtn.place_forget()
        seccion_title.place_forget()
        seccion_combobox.place_forget()
        material_title.place_forget()
        nombre_material_entry.place_forget()
        salon_title.place_forget()
        salon_entry.place_forget()
        diaInicio_title.place_forget()
        datePicker_btn1.place_forget()
        tiempoInicio_title.place_forget()
        timeEntry_btn1.place_forget()
        diaFinal_title.place_forget()
        datePicker_btn2.place_forget()
        tiempoFinal_title.place_forget()
        timeEntry_btn2.place_forget()
        materialbtn.place_forget()
        reservacionDispBtn.place_forget()
        
        acceso_title.place(relx=0.04, rely=0.20)
        entrada_entry.place(relx=0.04, rely=0.27)
            
    elif choice == "Asistencia":
        acceso_title.place_forget()
        entrada_entry.place_forget()
        material_title.place_forget()
        nombre_material_entry.place_forget()
        salon_title.place_forget()
        salon_entry.place_forget()
        diaInicio_title.place_forget()
        datePicker_btn1.place_forget()
        tiempoInicio_title.place_forget()
        timeEntry_btn1.place_forget()
        diaFinal_title.place_forget()
        datePicker_btn2.place_forget()
        tiempoFinal_title.place_forget()
        timeEntry_btn2.place_forget()
        materialbtn.place_forget()
        reservacionDispBtn.place_forget()
        
        
        curso_title.place(relx=0.04, rely=0.21)
        curso_entry.place(relx=0.04, rely=0.28)
        buscarCursoBtn.place(relx=0.04, rely=0.35)
        seccion_title.place(relx=0.04, rely=0.42)
        seccion_combobox.place(relx=0.04, rely=0.49)
    elif choice == "Material":
        acceso_title.place_forget()
        entrada_entry.place_forget()
        curso_title.place_forget()
        curso_entry.place_forget()
        buscarCursoBtn.place_forget()
        seccion_title.place_forget()
        seccion_combobox.place_forget()
        salon_title.place_forget()
        salon_entry.place_forget()
        diaInicio_title.place_forget()
        datePicker_btn1.place_forget()
        tiempoInicio_title.place_forget()
        timeEntry_btn1.place_forget()
        diaFinal_title.place_forget()
        datePicker_btn2.place_forget()
        tiempoFinal_title.place_forget()
        timeEntry_btn2.place_forget()
        reservacionDispBtn.place_forget()
        
        material_title.place(relx=0.04, rely=0.2)
        nombre_material_entry.place(relx=0.04, rely=0.27)
        materialbtn.place(relx=0.04, rely=0.35)
    elif choice == "Reservar Salón":
        acceso_title.place_forget()
        entrada_entry.place_forget()
        curso_title.place_forget()
        curso_entry.place_forget()
        buscarCursoBtn.place_forget()
        seccion_title.place_forget()
        seccion_combobox.place_forget()
        material_title.place_forget()
        nombre_material_entry.place_forget()
        materialbtn.place_forget()
        
        salon_title.place(relx=0.04, rely=0.2)
        salon_entry.place(relx=0.04, rely=0.27)
        diaInicio_title.place(relx=0.04, rely=0.34)
        datePicker_btn1.place(relx=0.04, rely=0.41)
        tiempoInicio_title.place(relx=0.04, rely=0.47)
        timeEntry_btn1.place(relx=0.04, rely=0.53)
        diaFinal_title.place(relx=0.04, rely=0.59)
        datePicker_btn2.place(relx=0.04, rely=0.65)
        tiempoFinal_title.place(relx=0.04, rely=0.71)
        timeEntry_btn2.place(relx=0.04, rely=0.77)
        
        reservacionDispBtn.place(relx=0.04, rely=0.85)
        
    elif choice == "Gimnasio":
        acceso_title.place_forget()
        entrada_entry.place_forget()
        curso_title.place_forget()
        curso_entry.place_forget()
        buscarCursoBtn.place_forget()
        seccion_title.place_forget()
        seccion_combobox.place_forget()
        material_title.place_forget()
        nombre_material_entry.place_forget()
        salon_title.place_forget()
        salon_entry.place_forget()
        diaInicio_title.place_forget()
        datePicker_btn1.place_forget()
        tiempoInicio_title.place_forget()
        timeEntry_btn1.place_forget()
        diaFinal_title.place_forget()
        datePicker_btn2.place_forget()
        tiempoFinal_title.place_forget()
        timeEntry_btn2.place_forget()
        materialbtn.place_forget()
        reservacionDispBtn.place_forget()
    elif choice == "Pago Estacionamiento":
        acceso_title.place_forget()
        entrada_entry.place_forget()
        curso_title.place_forget()
        curso_entry.place_forget()
        buscarCursoBtn.place_forget()
        seccion_title.place_forget()
        seccion_combobox.place_forget()
        material_title.place_forget()
        nombre_material_entry.place_forget()
        salon_title.place_forget()
        salon_entry.place_forget()
        diaInicio_title.place_forget()
        datePicker_btn1.place_forget()
        tiempoInicio_title.place_forget()
        timeEntry_btn1.place_forget()
        diaFinal_title.place_forget()
        datePicker_btn2.place_forget()
        tiempoFinal_title.place_forget()
        timeEntry_btn2.place_forget()
        materialbtn.place_forget()
        reservacionDispBtn.place_forget()
        


frame = tk.CTkFrame(master=root, width=725, height=460)
frame.place(relx = 0.04, rely=0.04)

cal = Calendar(master=frame, selectmode="day", year=2024, month=4, day=1)

panelTitle = tk.CTkLabel(master=frame, text="Console Information:", font=("Arial", 14))
panelTitle.place(relx= 0.70, rely=0.65)

panel = tk.CTkTextbox(master=frame, width= 200, height=120)
panel.place(relx=0.70, rely=0.70)

button = tk.CTkButton(master=frame, text="Empezar Escaneo")
button.place(relx = 0.4, rely= 0.15)

textTitle = tk.CTkLabel(master=frame, text="ID Scanner", font=("Arial", 25))
textTitle.place(relx=0.42, rely=0.03)

idTitle = tk.CTkLabel(master=frame, text="ID:", font=("Arial", 25))
idTitle.place(relx=0.40, rely=0.3)

varID = tk.StringVar()
idText = tk.CTkLabel(master=frame, font=("Arial", 20))
idText.configure(textvariable=varID)
varID.set("")
idText.place(relx=0.45, rely=0.3)

nameTitle = tk.CTkLabel(master=frame, text="Nombre:", font=("Arial", 25))
nameTitle.place(relx=0.25, rely=0.4)

varName = tk.StringVar()
nameText = tk.CTkLabel(master=frame, font=("Arial", 18))
nameText.configure(textvariable=varName)
varName.set("")
nameText.place(relx=0.38, rely=0.4)

varStarted = tk.StringVar()
started = tk.CTkLabel(master=frame, font=("Arial", 30), text_color='#F04848')
started.configure(textvariable=varStarted)
varStarted.set("Scanning Off")
started.place(relx=0.38, rely=0.5)


#app colorMode variables

switch_var = tk.StringVar(value="off")
switchTextVar = tk.StringVar()


colorMode = tk.CTkSwitch(master=frame, command= switch_event, variable=switch_var, onvalue="on", offvalue="off")
colorMode.configure(textvariable=switchTextVar)
switchTextVar.set('Dark Mode Off')
colorMode.place(relx=0.04, rely= 0.01)

#Mode variables
combobox_var = tk.StringVar()
combobox = tk.CTkComboBox(master=frame, values= settings_options, command= mode_callback, variable=combobox_var)
combobox.place(relx=0.04, rely=0.14)
combobox_title = tk.CTkLabel(master=frame, text="Scan Mode:", font=("Arial", 14), text_color='black')
combobox_title.place(relx=0.04, rely=0.08)

comboboxAcesso_var = tk.StringVar()
entrada_entry= tk.CTkComboBox(master=frame, values=entradas, variable=comboboxAcesso_var)
material_variable = tk.StringVar()
nombre_material_entry= tk.CTkEntry(master=frame, placeholder_text="Nombre Material", textvariable= material_variable)
salon_variable = tk.StringVar()
salon_entry= tk.CTkEntry(master=frame, placeholder_text="CN-103", textvariable= salon_variable)


comboboxCurso_var = tk.StringVar()
curso_entry= tk.CTkEntry(master=frame, placeholder_text="e.g. Álgebra Lineal", textvariable=comboboxCurso_var)

buscarCursoBtn = tk.CTkButton(master=frame, text="Buscar Curso", command=buscar_curso)

comboboxSeccion_var = tk.StringVar()
seccion_combobox= tk.CTkComboBox(master=frame, variable=comboboxSeccion_var)

datePicker_var = tk.StringVar()
timePicker_var = tk.StringVar()
datePicker_btn1 = tk.CTkEntry(master=frame, placeholder_text="YYY/MM/DD", textvariable=datePicker_var)
datePicker_btn1.bind("<1>", pick_date1)
timeEntry_btn1 = tk.CTkEntry(master=frame, placeholder_text="e.g. 14:00", textvariable=timePicker_var)

datePicker2_var = tk.StringVar()
timePicker2_var = tk.StringVar()
datePicker_btn2 =tk.CTkEntry(master=frame, placeholder_text="YYY/MM/DD", textvariable=datePicker2_var)
datePicker_btn2.bind("<1>", pick_date2)
timeEntry_btn2 = tk.CTkEntry(master=frame, placeholder_text="e.g. 09:35", textvariable=timePicker2_var)

materialbtn = tk.CTkButton(master=frame, text="Buscar Material", command=buscar_material)

reservacionDispBtn = tk.CTkButton(master=frame, text="Ver Disponibilidad", command=ver_disp)


#Mode Titles
acceso_title = tk.CTkLabel(master=frame, text="Acceso Universidad:", font=("Arial", 14), text_color='black')
curso_title = tk.CTkLabel(master=frame, text="ID Curso:", font=("Arial", 14), text_color='black')
seccion_title = tk.CTkLabel(master=frame, text="Sección:", font=("Arial", 14), text_color='black')
material_title = tk.CTkLabel(master=frame, text="Nombre Material:", font=("Arial", 14), text_color='black')
salon_title = tk.CTkLabel(master=frame, text="Salón (e.g. CN-103):", font=("Arial", 14), text_color='black')

diaInicio_title = tk.CTkLabel(master=frame, text="Día Inicio (YYY/MM/DD):", font=("Arial", 14), text_color='black')
diaFinal_title = tk.CTkLabel(master=frame, text="Día Final (YYY/MM/DD):", font=("Arial", 14), text_color='black')
tiempoInicio_title = tk.CTkLabel(master=frame, text="Tiempo Inicio (e.g. 14:00):", font=("Arial", 14), text_color='black')
tiempoFinal_title = tk.CTkLabel(master=frame, text="Tiempo Final (e.g. 09:35):", font=("Arial", 14), text_color='black')

    
def scan():
    if combobox_var.get() == "":
        combobox_var.set("Acceso")
        mode_callback("Acceso")
        comboboxAcesso_var.set("Acceso Recta")
    button.configure(state='disabled')
    combobox.configure(state="disabled")
    
    if combobox_var.get() == "Acceso":
        entrada_entry.configure(state="disabled")
    elif combobox_var.get() == "Asistencia":
        curso_entry.configure(state="disabled")
        buscarCursoBtn.configure(state="disabled")
        seccion_combobox.configure(state="disabled")
    elif combobox_var.get() == "Material":
        nombre_material_entry.configure(state="disabled")
        materialbtn.configure(state="disabled")
    elif combobox_var.get() == "Reservar Salón":
        salon_entry.configure(state="disabled")
        timeEntry_btn1.configure(state="disabled")
        datePicker_btn1.configure(state="disabled")
        timeEntry_btn2.configure(state="disabled")
        datePicker_btn2.configure(state="disabled")
        reservacionDispBtn.configure(state="disabled")
    
    
    started.configure(text_color="#5EE151")
    varStarted.set("Scanning On")
    nfc = serial.Serial("COM9", 115200)
    
    
    while not(kb.is_pressed('esc')): 
        if not nfc.is_open:
            nfc.open()
        if nfc.in_waiting > 0:
            data = nfc.readline().decode().strip()
            if "IDMessage" in data:
                for i in range(1, 2):
                    beep(1)
                idMessage = ""
                idMessage = data.split(':')
                idMessage = idMessage[1].split('\x00')
                id = idMessage[1]
                search = db["users"].find_one({"id": id})
                if search != None:
                    varID.set(id)
                    varName.set(search["nombre"]) 
                    print(id)
                    panel.insert("end", text = id + '\n')
                    if combobox_var.get() == "Acceso":
                        db["accesos"].insert_one(
                            {"id_usuario": id,
                             "acceso": comboboxAcesso_var.get(),
                             "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    elif combobox_var.get() == "Asistencia":
                        idCurso = comboboxCurso_var.get()
                        seccion = comboboxSeccion_var.get()
                        status = ""
                        hora_inicio = datetime.datetime.strptime(db["cursos"].find_one({"$and":[{"id_curso": idCurso}, {"seccion": seccion}]})["hora_inicio"], "%H:%M")
                        hora_actual= datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M"), "%H:%M")
                        
                        c = (hora_actual - hora_inicio)
                        diferencia = c.total_seconds() / 60
                        if diferencia < 10:
                            status = clase_estado[0]
                        elif 10 >= diferencia < 19:
                            status= clase_estado[1]
                        elif diferencia >= 20:
                            status = clase_estado[2]
                        db["asistencia_cursos"].insert_one(
                            {"id_usuario": id,
                             "id_curso": comboboxCurso_var.get(),
                             "seccion": comboboxSeccion_var.get(),
                             "estado": status,
                             "time": hora_actual})
                    elif combobox_var.get() == "Material":
                         db["prestamo_materiales"].insert_one(
                            {"id_usuario": id,
                             "id_material": material_variable.get().upper(),
                             "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    elif combobox_var.get() == "Reservar Salón":
                        db["reservacion_salones"].insert_one(
                            {"id_usuario": id,
                             "salon": salon_variable.get(),
                             "initial_time": datePicker_var.get().replace("/", "-") + " " + timePicker_var.get(),
                             "end_time": datePicker2_var.get().replace("/", "-") + " " + timePicker2_var.get()})
                    elif combobox_var.get() == "Gimnasio":
                        db["gym_accesos"].insert_one(
                            {"id_usuario": id,
                             "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    elif combobox_var.get() == "Pago Estacionamiento":
                        db["estacionamiento_pagos"].insert_one(
                            {"id_usuario": id,
                             "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    
                else:
                    panel.insert("end", text = 'El ID escaneado no fue encontrado en la base de datos.\n')
            else:
                panel.insert("end",text = data + "\n")
                print(data)
                
            
    print("Thanks. Exit")

    if nfc.is_open:
        nfc.close()


thread =threading.Thread(target=scan)
thread.daemon = True

button.configure(command= lambda: thread.start())

root.mainloop()

