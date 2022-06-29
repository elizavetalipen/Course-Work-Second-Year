from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QSlider, QFileDialog, QErrorMessage, QMessageBox
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import matplotlib

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

import sys
import os.path
import regex as re
import math
import sympy

import mymodels

class App(QWidget):
    
    
    def __init__(self, fname):
        
        self.fname = fname
        self.start()
        
        
    def start(self):
        ''' Метод, вызывающий графический шаблон'''
        
        self.ui=uic.loadUi('design.ui')
        self.ui.show()
        self.set_slider()
        self.set_lineEdit()
        self.set_plot()
        self.set_initial_params()
        self.set_changing_params()
     
        
    def load_file(self,dialog=True):
        ''' Загружает файл и пересчитывает значения'''
        
        if dialog == True:
            file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                   "", "Json Files (*.json);;")
            if check:
                self.ui.lineEdit.setText(file)
                self.fname = file
                # присвоить лэйблам значения из файла
                self.set_initial_params()
                self.set_changing_params() # обновляются графики
                # обновляются вычисляемые значения
                for i in range(1,4):
                    self.set_calculated_params(i)

        else: 
            file_path = self.ui.lineEdit.text()
            if os.path.exists(file_path):
                self.fname = file_path
                # присвоить лэйблам значения из файла
                self.set_initial_params()
                self.set_changing_params() # обновляются графики
                # обновляются вычисляемые значения
                for i in range(1,4):
                    self.set_calculated_params(i)
                    
                self.ui.lineEdit.setStyleSheet("QLineEdit"
                                        "{"
                                        "background : #EBF2FC;"
                                        "}")
                
            else:
                self.ui.lineEdit.setStyleSheet("QLineEdit"
                                    "{"
                                    "background : #F3CBB4;"
                                    "}")
     

        
    def set_initial_params(self,p='file'):
        ''' Устанавливает начальные параметры, по умолчанию они считываются из файла,
        но могут задаваться через поле ввода'''
        
        parameters = mymodels.read_data(self.fname)
        self.T, self.gamma = round(parameters['T']*0.001), parameters['gamma']
        T, gamma = str(self.T),str(self.gamma)
        
        if p == 'file': 
            pass
            
        elif p == 'lineEdit':
            if self.ui.edit_gamma.text() != '': 
                gamma = self.ui.edit_gamma.text()
                try:
                    self.gamma = float(gamma)
                    
                except Exception as e:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Input must be a number')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                      
                self.ui.edit_gamma.clear()
                    
            if self.ui.edit_T.text() != '':
                T = self.ui.edit_T.text()
                
                try:
                    self.T = float(T)
                    
                except Exception as e:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Input must be a number')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    
                self.ui.edit_T.clear()
            
        text1 = self.ui.lbl_gamma1.text()
        text1 = mymodels.split_text(text1,gamma,10,'(1/h)')
        
        self.ui.lbl_gamma1.setText(text1)
        self.ui.lbl_gamma2.setText(text1)
        self.ui.lbl_gamma3.setText(text1)
        
        text2 = self.ui.lbl_T1.text()
        text2 = mymodels.split_text(text2,T,10,' (mM)')
        
        self.ui.lbl_T1.setText(text2)
        self.ui.lbl_T2.setText(text2)
        self.ui.lbl_T3.setText(text2)
        
              
    def set_changing_params(self):
        
        # установка начальных значений со слайдера
        beta1 = (self.ui.Slider11.value())/1000
        beta2 = (self.ui.Slider21.value())/1000
        nu1 = (self.ui.Slider12.value())/10000
        nu2 = (self.ui.Slider22.value())/10000
        delta2 = (self.ui.Slider23.value())/1000
        delta3 = (self.ui.Slider3.value())/1000
        
        # по умолчанию в поле ввода отображается значение со слайдера
        self.ui.edit_beta1.setText(str(beta1))
        self.ui.edit_beta2.setText(str(beta2))
        self.ui.edit_nu1.setText(str(nu1))
        self.ui.edit_nu2.setText(str(nu2))
        self.ui.edit_delta2.setText(str(delta2))
        self.ui.edit_delta3.setText(str(delta3))
        
        # строим графики по данным начальным значениям
        self.update_plot(1,[beta1,nu1])
        self.update_plot(2,[beta2, nu2, delta2])
        self.update_plot(3,[delta3])
        
        
    def set_plot(self):
        ''' Создает шаблон для графика'''
        
        self.canvas1 = Canvas(plt.Figure(figsize=(6,4)))
        self.canvas2 = Canvas(plt.Figure(figsize=(6,4)))
        self.canvas3 = Canvas(plt.Figure(figsize=(6,4)))
        self.ui.plot_layout1.addWidget(self.canvas1)
        self.ui.plot_layout2.addWidget(self.canvas2)
        self.ui.plot_layout3.addWidget(self.canvas3)
        
        # установка осей
        self.ax1 = self.canvas1.figure.subplots()
        # названия осей
        self.ax1.set(xlabel='Time(h)', ylabel='Cell concentration(%)')
        self.ax1.set_ylim([0,100])
        self.ax1.set_xlim([0,6])
        self.ax2 = self.canvas2.figure.subplots()
        self.ax2.set(xlabel='Time(h)', ylabel='Cell concentration(%)')
        self.ax2.set_ylim([0,100])
        self.ax2.set_xlim([0,6])
        self.ax3 = self.canvas3.figure.subplots()
        self.ax3.set(xlabel='Time(h)', ylabel='Cell concentration(%)')
        self.ax3.set_ylim([0,100])
        self.ax3.set_xlim([0,6])
        
        
    def update_plot(self, n:int, vals:list):
        '''' Обновляет график на основе вычисленных параметров '''
        
        hours = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]
        params = mymodels.read_data(self.fname)
        cexp = params['Cexp']
        
        if n == 1:
            results = mymodels.model1(self.T,self.gamma,vals[0],vals[1],hours)
            c = results # list
            
            self.ax1.cla()
            self.plt1 = self.ax1.plot(hours,c)
            self.ax1.scatter(hours,cexp,color = '#88c999')
            self.canvas1.draw()
            
            # вычисление ошибки
            err = mymodels.error(cexp,c)
            text = self.ui.error1.text()
            text = mymodels.split_text(text,err,1,'','=')
            self.ui.error1.setText(text)
         
            
        elif n == 2:
            results = mymodels.model2(self.T, self.gamma,vals[0],vals[1],vals[2],hours)
            c = results # list
            
            self.ax2.cla()
            self.plt2 = self.ax2.plot(hours,c)
            self.ax2.scatter(hours,cexp,color = '#88c999')
            self.canvas2.draw()
            
            # вычисление ошибки
            err = str(mymodels.error(cexp,c))
            text = self.ui.error2.text()
            text = mymodels.split_text(text,err,1,'','=')
            self.ui.error2.setText(text)
            
        
        elif n == 3:
            results = mymodels.model3(self.T,self.gamma,vals[0],hours)
            c = results # list
            
            self.ax3.cla()
            self.plt3 = self.ax3.plot(hours,c)
            self.ax3.scatter(hours,cexp,color = '#88c999')
            self.canvas3.draw()
            
            # вычисление ошибки
            err = str(mymodels.error(cexp,c))
            text = self.ui.error3.text()
            text = mymodels.split_text(text,err,1,'','=')
            self.ui.error3.setText(text)
    
                  
    def set_lineEdit(self):
        
        self.ui.lineEdit.setStyleSheet("QLineEdit"
                                "{"
                                "background : #EBF2FC;"
                                "}")
        
        
        self.ui.search_btn.clicked.connect(lambda:self.load_file())
        self.ui.lineEdit.returnPressed.connect(lambda:self.load_file(dialog=False))
        
        self.ui.edit_gamma.returnPressed.connect(lambda:self.set_initial_params(p='lineEdit'))
        self.ui.edit_T.returnPressed.connect(lambda:self.set_initial_params(p='lineEdit'))
        
        self.ui.edit_beta1.returnPressed.connect(lambda:self.lineEdit_changed(num=11))
        self.ui.edit_beta2.returnPressed.connect(lambda:self.lineEdit_changed(num=21))
        self.ui.edit_nu1.returnPressed.connect(lambda:self.lineEdit_changed(num=12))
        self.ui.edit_nu2.returnPressed.connect(lambda:self.lineEdit_changed(num=22))
        self.ui.edit_delta2.returnPressed.connect(lambda:self.lineEdit_changed(num=23))
        self.ui.edit_delta3.returnPressed.connect(lambda:self.lineEdit_changed(num=3))
        
    
    def set_slider(self):
        
        self.ui.Slider11.valueChanged.connect(lambda:self.slider_changed(num = 11))
        self.ui.Slider12.valueChanged.connect(lambda:self.slider_changed(num = 12))
        self.ui.Slider21.valueChanged.connect(lambda:self.slider_changed(num = 21))
        self.ui.Slider22.valueChanged.connect(lambda:self.slider_changed(num = 22))
        self.ui.Slider23.valueChanged.connect(lambda:self.slider_changed(num = 23))
        self.ui.Slider3.valueChanged.connect(lambda:self.slider_changed(num = 3))
    
        
    def lineEdit_changed(self,num:int):
        ''' При нажатии кнопки Enter значение из LineEdit перестраивает графики'''
        
        if num == 11:
            try:
                curr_val = float(self.ui.edit_beta1.text())
                other_val = float(self.ui.edit_nu1.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val11.setText(str(curr_val))
                self.ui.Slider11.setValue(int(curr_val*1000))
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(1)
                
                # обновляем график
                self.update_plot(1,[curr_val, other_val])
                
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()

        
        elif num == 12:
            try:
                curr_val = float(self.ui.edit_nu1.text())
                other_val = float(self.ui.edit_beta1.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val12.setText(str(curr_val))
                self.ui.Slider12.setValue(int(curr_val*10000))
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(1)
                
                # обновляем график
                self.update_plot(1,[other_val, curr_val])
            
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
       
        
        elif num == 21:
            try:
                curr_val = float(self.ui.edit_beta2.text())
                other1 = float(self.ui.edit_nu2.text())
                other2 = float(self.ui.edit_delta2.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val21.setText(str(curr_val))
                self.ui.Slider21.setValue(int(curr_val*1000))
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(2)
                
                # обновляем график
                self.update_plot(2,[curr_val,other1, other2])
            
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
            
        elif num == 22:
            try:
                curr_val = float(self.ui.edit_nu2.text())
                other1 = float(self.ui.edit_beta2.text())
                other2 = float(self.ui.edit_delta2.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val22.setText(str(curr_val))
                self.ui.Slider22.setValue(int(curr_val*10000))
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(2)
                
                # обновляем график
                self.update_plot(2,[other1, curr_val, other2])
            
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
            
        elif num == 23:
            try:
                curr_val = float(self.ui.edit_delta2.text())
                other1 = float(self.ui.edit_beta2.text())
                other2 = float(self.ui.edit_nu2.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val23.setText(str(curr_val))
                self.ui.Slider23.setValue(int(curr_val*1000))
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(2)
                
                # обновляем график
                self.update_plot(2,[other1, other2, curr_val])
            
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
            
        elif num == 3:
            try:
                curr_val = float(self.ui.edit_delta3.text())
                
                # установка соответствующего значения на слайдере
                self.ui.Val3.setText(str(curr_val))
                self.ui.Slider3.setValue(int(curr_val*1000)) #int is required
                
                # устанавливаем значения вычисленных констант
                self.set_calculated_params(3)
                
                # обновляем график
                self.update_plot(3,[curr_val])
                
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Error")
                msg.exec_()
    
        
    def slider_changed(self, num:int):
        ''' При протягивании соответствующего слайдера меняется текст в LineEdit,
        перестраиваются графики'''
        
        if num == 11:
            curr_val = (self.ui.Slider11.value())/1000
            other_val = (self.ui.Slider12.value())/10000
            
            # меняем значение цифры возле самого слайдера
            self.ui.Val11.setText(str(curr_val))
            self.ui.edit_beta1.setText(str(curr_val))
            
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(1)
            
            # обновляем график
            self.update_plot(1,[curr_val, other_val])
            
            
        elif num == 12:
            curr_val = (self.ui.Slider12.value())/10000
            other_val = (self.ui.Slider11.value())/1000
            self.ui.Val12.setText(str(curr_val))
            
            self.ui.edit_nu1.setText(str(curr_val))
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(1)
            
            # обновляем график
            self.update_plot(1,[other_val, curr_val])
            
        elif num == 21:
            curr_val = (self.ui.Slider21.value())/1000
            other1 = (self.ui.Slider22.value())/10000
            other2 = (self.ui.Slider23.value())/1000
            self.ui.Val21.setText(str(curr_val))
            
            self.ui.edit_beta2.setText(str(curr_val))
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(2)
            
            # обновляем график
            self.update_plot(2,[curr_val,other1, other2])
            
        elif num == 22:
            curr_val = (self.ui.Slider22.value())/10000
            other1 = (self.ui.Slider21.value())/1000
            other2 = (self.ui.Slider23.value())/1000
            self.ui.Val22.setText(str(curr_val))
            
            self.ui.edit_nu2.setText(str(curr_val))
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(2)
            
            # обновляем график
            self.update_plot(2,[other1, curr_val, other2])
            
        elif num == 23:
            curr_val = (self.ui.Slider23.value())/1000
            other1 = (self.ui.Slider21.value())/1000
            other2 = (self.ui.Slider22.value())/10000
            self.ui.Val23.setText(str(curr_val))

            self.ui.edit_delta2.setText(str(curr_val))
            
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(2)
            
            # обновляем график
            self.update_plot(2,[other1, other2, curr_val])
            
        elif num == 3:
            curr_val = (self.ui.Slider3.value())/1000 #delta
            self.ui.Val3.setText(str(curr_val))

            self.ui.edit_delta3.setText(str(curr_val))
            
            # устанавливаем значения вычисленных констант
            self.set_calculated_params(3)
            
            # обновляем график
            self.update_plot(3,[curr_val])
            
            
    def set_calculated_params(self, m:int):
        
        try:
            T = self.ui.lbl_T3.text()
            T = re.findall(r'\d*\.\d+|\d+', T)
            T = float(T[0])
            gamma = self.ui.lbl_gamma3.text()
            gamma = re.findall(r'\d*\.\d+|\d+', gamma)
            gamma = float(gamma[0])
            
            c = []
            t = sympy.symbols('t')
            
            # первая модель
            if m == 1:
                
                # текущие значения слайдеров
                beta = float(self.ui.edit_beta1.text())
                nu = float(self.ui.edit_nu1.text())
                
                hep_const = round(nu/beta,5)
                
                text = self.ui.lbl_const1.text()
                text = mymodels.split_text(text,hep_const,10,' (hMm)')
                self.ui.lbl_const1.setText(text)
                
                '''try:
                    # calculating median lethal time
                    expr= 100*sympy.exp(-gamma*t + ((T*nu)/(beta*beta))*(1-sympy.exp(-t*beta)-t*beta))-50
                    sol = round(sympy.nsolve(expr,t,1),5)
                except Exception as e:
                    #print(e)
                    sol = '???' '''
                sol='???'
                    
                text2 = self.ui.lbl_median1.text()
                text2 = mymodels.split_text(text2,sol,10,' (h)')
                self.ui.lbl_median1.setText(text2)
                
                
            elif m == 2:
                beta = float(self.ui.edit_beta2.text())
                nu = float(self.ui.edit_nu2.text())
                delta = float(self.ui.edit_delta2.text())
                
                # вторая модель непонятно по какой формуле вычислить
                hep_const = '???'
                text = self.ui.lbl_const2.text()
                text = mymodels.split_text(text,hep_const,10,' (hMm)')
                self.ui.lbl_const2.setText(text)
                
                '''try:
                    # calculating median lethal time
                    expr= 100*sympy.exp(-(gamma+delta)*t + ((T*nu)/(beta*beta))*(1-sympy.exp(-t*beta)-t*beta))-50
                    sol = round(sympy.nsolve(expr,t,1),5)
                except Exception as e:
                    #print(e)
                    sol = '???' '''
                sol = '???'
                    
                text2 = self.ui.lbl_median2.text()
                text2 = mymodels.split_text(text2,sol,10,' (h)')
                self.ui.lbl_median2.setText(text2)
            
            elif m == 3:
                delta = float(self.ui.edit_delta3.text())
                hep_const = round(delta*T,5)
                
                text = self.ui.lbl_const3.text()
                text = mymodels.split_text(text,hep_const,10,' (1/h)')
                self.ui.lbl_const3.setText(text)
                
                try:
                    # calculating median lethal time
                    expr= 100*sympy.exp(-(gamma*T+delta)*t)-50
                    sol = round(sympy.nsolve(expr,t,1),5)
                except Exception as e:
                    sol = '???'
                    
                text2 = self.ui.lbl_median3.text()
                text2 = mymodels.split_text(text2,sol,10,' (h)')
                self.ui.lbl_median3.setText(text2)
                
            
        except Exception as e:
            print(e)
        
            
def main():
    try:
        app=QApplication(sys.argv)
        ex=App('A5.json')
        app.exec_()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()