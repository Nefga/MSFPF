
"""
Práctica Cinco: Sistema cardiovascular-arterioesclerosis

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Neltzon Farid Garcia Altamirano
Número de control: 23212194
Correo institucional: l23212194@tijuana.tecnm.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
#Librerías
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

#Datos Generales de la Simulacion
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt)+1
t = np.linspace(t0,tend,N)
u = np.zeros(N)
u[round(1/dt):round(2/dt)] = 1

#Componentes Circuito
R1,R2,R3,L,C1 = 1E3,2.2E3,10E3,100E-3,1000E-6
R2caso,C1caso = 22E3,100E-6
sys = ctrl.tf([R3],[L*C1*(R2+R3),L+R1*C1*(R2+R3),R1+R2+R3])
sysCaso = ctrl.tf([R3],[L*C1caso*(R2caso+R3),L+R1*C1caso*(R2caso+R3),R1+R2caso+R3])

#Componentes del controlador
kP,kI,kD = 10,103.23,0
PID = ctrl.tf([kD,kP,kI],[1,0])

#Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,sysCaso),1,sign=-1)

#Respuestas
_,VsX = ctrl.forced_response(sys,t,u,x0)
_,VsY = ctrl.forced_response(sysCaso,t,u,x0)
_,PIDu = ctrl.forced_response(sysPID,t,VsX,x0)

#Colores
ctrl1 = np.array([0,125,204])/255
ctrl2 = np.array([235,185,0])/255
ctrl3 = np.array([209,0,86])/255
ctrl4 = np.array([80,0,113])/255

fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'
plt.plot(t,u,'-',color=ctrl1,label='Ve(t)')
plt.plot(t,VsX,'-',color=ctrl2,label='Vs(t): Control')
plt.plot(t,VsY,'--',color=ctrl3,label='Vs(t): Caso')
plt.plot(t,PIDu,':',linewidth=2.5,color=ctrl4,label='PID: Transferencia')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.3,0.1))
plt.xlabel('t [s]')
plt.ylabel('Vs(t) [V]')
plt.legend(bbox_to_anchor=(0.5,1.12),loc='center',ncol=4)
fg.savefig('practica5_python.pdf',bbox_inches='tight')
fg.savefig('practica5_python.png',dpi=200,bbox_inches='tight')
plt.show()
