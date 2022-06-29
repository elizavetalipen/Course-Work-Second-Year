# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 20:48:25 2022

@author: User

Вспомогательные функции
"""

import math
import json
import sympy


def read_data(fname:str)->dict:
    ''' Параметры Т и Гамма читаются из json файла'''
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            data = json.load(f) #загрузить данные в словарь 
        return data
            
    except Exception as e:
        print(e)


def split_text(text:str,val,spacings:int,measure:str, sep=':'):
    ''' text - строка с лэйбла, val - численное значение которое нужно установить
    spacings - число пробелов measure - единица измерения'''
        
    ind = text.find(sep)+1
    text = text[:ind]+' '*spacings + str(val) + measure
    return text.rjust(3)


def model1(T, gamma, b, mu,hours:list)->list:
    ''' parameters  '''
    
    '''T = params['T']*0.001
    gamma = params['gamma']'''
    c = []
        
    for t in hours:
        res = -gamma*t + ((T*mu)/math.pow(b,2))*(1-math.exp(-t*b)-t*b)
        res = 100*math.exp(res)
        c.append(res)
             
    return c


def model2(T, gamma, b,mu, delta,hours:list):
    ''' parameters'''
    
    '''T = params['T']*0.001
    gamma = params['gamma']'''
    c = []
    
    for t in hours:
        res = -(gamma+delta)*t + ((T*mu)/math.pow(b,2))*(1-math.exp(-t*b)-t*b)
        res = math.exp(res)
        c.append(res*100)
         
    return c


def model3(T,gamma, delta, hours:list):
    ''' parameters  '''
    
    '''T = params['T']*0.001
    gamma = params['gamma']'''
    c = []
    
    for t in hours:
        # res = -(gamma+delta)*t + delta*tau*(1-math.exp(-t/tau))
        res = -(gamma*T+delta)*t
        res = math.exp(res)
        c.append(res*100)
        
    return c


def error(experimental:list,evaluated:list):
    res = math.dist(experimental,evaluated)
    return round(res/100,3)



