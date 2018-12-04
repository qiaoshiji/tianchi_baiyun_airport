# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 14:06:59 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:29:25 2016

@author: Administrator
"""
from pandas import DataFrame
import pandas as pd
import time
import json
import numpy as np
import copy
import random
print "begin to read data"
a=pd.read_csv('./jiwei_2nd_1107.csv')
b=pd.read_csv('./schedule1.csv')
b['in_time_stamp']=''
b['out_time_stamp']=''
b['duration']=''

"""
for i in b.index:
    b.loc[i,'in_time_stamp']=time.mktime(time.strptime(b.loc[i,'in_time'],'%Y-%m-%d %H:%M:%S'))
    b.loc[i,'out_time_stamp']=time.mktime(time.strptime(b.loc[i,'out_time'],'%Y-%m-%d %H:%M:%S'))
    b.loc[i,'duration']=b.loc[i,'out_time_stamp']-b.loc[i,'in_time_stamp']
"""
for i in b.index:
    b.loc[i,'in_time_stamp']=time.mktime(time.strptime(b.loc[i,'in_time'],'%Y/%m/%d %H:%M'))
    b.loc[i,'out_time_stamp']=time.mktime(time.strptime(b.loc[i,'out_time'],'%Y/%m/%d %H:%M'))
    b.loc[i,'duration']=b.loc[i,'out_time_stamp']-b.loc[i,'in_time_stamp']

mis_write=b[b['duration']<=0]
data=b[b['duration']>0]
all_data=copy.deepcopy(data)


chushijie=pd.read_csv('./result.csv')
while True:
    t_f1=random.randint(int(all_data.out_time_stamp.min()),int(all_data.in_time_stamp.max()))
    t_f2=t_f1+600
    t_b1=t_f2+3600*15
    t_b2=t_b1+600
    data=all_data[all_data.in_time_stamp>=t_f2]
    data=data[data.out_time_stamp<=t_b1]
    none_ralated1=all_data[all_data.out_time_stamp<=t_f1]
    none_ralated2=all_data[all_data.in_time_stamp>=t_b2]
    con=all_data[~all_data.fnum.isin(list(none_ralated1.fnum))]
    con=con[~con.fnum.isin(list(none_ralated2.fnum))]
    con=con[~con.fnum.isin(list(data.fnum))]
    con=con[con.fnum.isin(list(chushijie.fnum))]
    data=pd.concat([data,con])
    data=data.reset_index()
    del data['index']             
                 
    
    #con=pd.read_csv('./result.csv')
    aircraft_count=len(data)
    population=data.members.sum()
    a=pd.read_csv('./jiwei_2nd_1107.csv')
    a['airline'][a['airline']!=a['airline']]='all'
    a['mession'][a['mession']!=a['mession']]='2,3,4,5,6,C,D,E,I,J,M,O,S,F,P,V,Y,Z'
    a['fcategory'][a['fcategory']!=a['fcategory']]='ID'
    
    N=[]
    apron=list(np.array(a['apron']))
    for i in a.index:
        if a['dis_type'][i]=='N':
            N.append(i)
    
    fenpeijieguo={}
        
    for i in range(len(apron)):
        fenpeijieguo[apron[i]]=[]
        
    for i in chushijie.index:
        if not chushijie['fnum'][i] in list(data.fnum):
            j=chushijie['apron'][i]
            if  j=='501ZJ':
                j='501J'
            elif j=='515YJ':
                j='515J'
            elif j[-2:]=='ZJ':
                j=j[:3]+'JL'
            elif j[-2:]=='YJ':
                j=j[:3]+'JU'        
            apron_index=list(all_data[all_data['fnum']==chushijie['fnum'][i]].index)[0]
            fenpeijieguo[j].append(apron_index)
    
    apron_count=len(apron)    
    
    
            
    a.index=a.apron
    del a['apron']
    b=a.T
    c=b.to_json()
    d=json.loads(c)
    for i in d:
        if d[i]['aircraft_type']==d[i]['aircraft_type']:
            d[i]['a_type']=d[i]['aircraft_type'].split(',')
        if d[i]['airline']==d[i]['airline']:
            d[i]['airline']=d[i]['airline'].split(',')
        if d[i]['mession']==d[i]['mession']:
            d[i]['f_type']=d[i]['mession'].split(',')
    
    L=[]
    for i in range(apron_count):
        if d[apron[i]]['airline']==['all']:
            L.append(i)
    
    def yifenpei(k):
        fnum=data['fnum'][k]
        for i in chushijie.index:
            if chushijie['fnum'][i]==fnum:
                j=chushijie['apron'][i]
        if  j=='501ZJ':
            j='501J'
        elif j=='515YJ':
            j='515J'
        elif j[-2:]=='ZJ':
            j=j[:3]+'JL'
        elif j[-2:]=='YJ':
            j=j[:3]+'JU'   
        return j
     
    huaxing_order=[]
    for i in apron:
        if d[i]['in_huaxing']!=None:
            huaxing_order.append(str(d[i]['in_huaxing']))
        if d[i]['out_huaxing']!=None:
            huaxing_order.append(str(d[i]['out_huaxing']))
    huaxing_order=list(set(huaxing_order))
    
    in_jiwei={}
    out_jiwei={}
    for i in huaxing_order:
        in_jiwei[i]=[]
        out_jiwei[i]=[]
    for i in apron:
        if d[i]['in_huaxing']!=None:
            in_jiwei[d[i]['in_huaxing']].append(i)
        if d[i]['out_huaxing']!=None:
            out_jiwei[d[i]['in_huaxing']].append(i)       
            
    def test_conflict(t1,t2,t3,t4):
        if int(t3)-int(t2)>=600 or int(t1)-int(t4)>=600:
            return False 
        else:
            return True
    
    
    def in_conflict(t1,t2,t3,t4):
        if int(t1)-int(t3)>-300 and int(t1)-int(t3)<300 :
            return True 
        else:
            return False
    
    def out_conflict(t1,t2,t3,t4):
        if int(t2)-int(t4)>-300 and int(t2)-int(t4)<300 :
            return True 
        else:
            return False 
    
    def in_out_conflict(t1,t2,t3,t4):
        if int(t1)-int(t4)<600 and int(t1)-int(t4)>0 :
            return True 
        else:
            return False
    
    def out_in_conflict(t1,t2,t3,t4):
        if int(t3)-int(t2)<600 and int(t3)-int(t2)>0 :
            return True 
        else:
            return False
    
    
            
    def huaxingdaochongtu(i,j):
                #print i,j 
        in_huaxingdao=d[j]['in_huaxing']
        out_huaxingdao=d[j]['out_huaxing']
        if in_huaxingdao!=None:
            jin=in_jiwei[in_huaxingdao]
                    #print jin
            for k in jin:
                if k!=j:
                    for l in fenpeijieguo[k]:
                        if in_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],all_data['in_time_stamp'][l],all_data['out_time_stamp'][l]) :
                            return True
        if out_huaxingdao!=None:
            chu=out_jiwei[out_huaxingdao]
                    #print chu
            for k in chu:
                if k!=j:
                    for l in fenpeijieguo[k]:
                        if out_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],all_data['in_time_stamp'][l],all_data['out_time_stamp'][l]) :
                            return True
        if in_huaxingdao!=None:
            jin=out_jiwei[in_huaxingdao]
                    #print jin
            for k in jin:
                if k!=j:
                    for l in fenpeijieguo[k]:
                        if in_out_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],all_data['in_time_stamp'][l],all_data['out_time_stamp'][l]):
                            return True
        if out_huaxingdao!=None:
            chu=in_jiwei[out_huaxingdao]
                    #print chu
            for k in chu:
                if k!=j:
                    for l in fenpeijieguo[k]:
                        if out_in_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],all_data['in_time_stamp'][l],all_data['out_time_stamp'][l]) :
                            return True
        return False
    
    
    con_conflict_list=[]
    for i in data.index:
        if data['fnum'][i] in list(con.fnum):
            jiwei=yifenpei(i)
            if huaxingdaochongtu(i,jiwei):
                con_conflict_list.append(i)
    
    choose_apron=[]                 
    choose_list={}                    
    for i in data.index:
        if data['fnum'][i] in list(con['fnum']):
            yifenpeijiwei=yifenpei(i)
            choose_list[i]=[yifenpeijiwei]
        else:
            apron_list=[]
            for j in apron:
                if data['mession'][i] in d[j]['f_type'] and (data['airline'][i] in d[j]['airline'] or d[j]['airline']==['all']) and data['aircraft_type'][i] in d[j]['a_type']:
                    if data['fcategory'][i]==d[j]['fcategory'] or d[j]['fcategory']=='ID' :
                        apron_list.append(j)
            apron_list.sort()
            choose_list[i]=apron_list                   
    """
    for i in data.index:
        apron_list=[]
        for j in d:
            if data['mession'][i] in d[j]['f_type'] and (data['airline'][i] in d[j]['airline'] or d[j]['airline']==['all']) and data['aircraft_type'][i] in d[j]['a_type']:
                if data['fcategory'][i]==d[j]['fcategory'] or d[j]['fcategory']=='ID' :
                    apron_list.append(j)
        apron_list.sort()
        choose_list[i]=apron_list
    """
        
    for i in choose_list:
        list_a=[]
        for j in range(len(apron)):
            if apron[j] in choose_list[i]:
                list_a.append(1)
            else:
                list_a.append(0)
        choose_apron.append(list_a)
            
    score_list=[]
    for i in range(apron_count):
        if i in N:
            score_list.append(13.0/aircraft_count)
        elif i in L:
            score_list.append(9.0/aircraft_count)
        else:
            score_list.append(10.0/aircraft_count)
            
    pop_score=[]
    for i in data.index:
        if data['members'][i]==data['members'][i]:
            pop_score.append(3.0*data['members'][i]/population)
        else:
            pop_score.append(0.0)
    
    conflict_8min=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if test_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and j>i:
                list_1.append(j)
        conflict_8min.append(list_1)
    
    conflict_in_5min=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if in_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and j!=i:
                list_1.append(j)
        conflict_in_5min.append(list_1)
    
    conflict_out_5min=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if out_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and j!=i:
                list_1.append(j)
        conflict_out_5min.append(list_1)
    
    conflict_in_out_5min=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if in_out_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and j!=i:
                list_1.append(j)
        conflict_in_out_5min.append(list_1)
    
    conflict_out_in_5min=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if out_in_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and j!=i:
                list_1.append(j)
        conflict_out_in_5min.append(list_1)
        
    apron_num=[]
    for i in range(apron_count):
        apron_num.append(i)
    
    
    
    
    in_huaxing=[]
    for i in huaxing_order:
        list_2=[]
        for j in range(apron_count):
            if d[apron[j]]['in_huaxing']==i:
                list_2.append(j)
        in_huaxing.append(list_2)
    
    out_huaxing=[]
    for i in huaxing_order:
        list_2=[]
        for j in range(apron_count):
            if d[apron[j]]['out_huaxing']==i:
                list_2.append(j)
        out_huaxing.append(list_2)
    
    huaxing_count=len(huaxing_order)
    
       
    choose_in_huaxing=[]
    for i in range(aircraft_count):
        huaxing_list=[]
        for j in range(huaxing_count):
            sum_x=0
            for k in in_huaxing[j]:
                sum_x=choose_apron[i][k]+sum_x
            if sum_x>0:
                huaxing_list.append(1)
            else:
                huaxing_list.append(0)
        choose_in_huaxing.append(huaxing_list)
    
    choose_out_huaxing=[]
    for i in range(aircraft_count):
        huaxing_list=[]
        for j in range(huaxing_count):
            sum_x=0
            for k in out_huaxing[j]:
                sum_x=choose_apron[i][k]+sum_x
            if sum_x>0:
                huaxing_list.append(1)
            else:
                huaxing_list.append(0)
        choose_out_huaxing.append(huaxing_list)
    
    apron_dict={}
    for i in range(apron_count):
        apron_dict[apron[i]]=i
       
    #import cplex
    from gurobipy import *
    
    m = Model("2nd_round")
    
    #model=cplex.Cplex()
    #model.objective.set_sense(model.objective.sense.maximize)
    
    
    print ("begin to set variables",time.ctime())
    x = m.addVars([("apron"+str(i),"fnum"+str(j)) for i in range(apron_count) for j in range(aircraft_count)],vtype = GRB.BINARY,name = "x")
    """
    for i in range(apron_count):
        for j in range(aircraft_count):
            if i in N:
                model.variables.add(
                                names = ["apron"+str(i) +"fnum"+str(j)],
                                         obj   = [score_list[i]+pop_score[j]])#score_list[i]
            else:
                model.variables.add(
                                names = ["apron"+str(i) +"fnum"+str(j)],
                                         obj   = [score_list[i]])
            model.variables.set_types("apron"+str(i) +"fnum"+str(j), model.variables.type.binary)
    """
    y = m.addVars(["fnum_conflict"+str(i) for i in range(aircraft_count)],vtype = GRB.BINARY,name = "y")
    """
    for i in range(aircraft_count):
        model.variables.add(
                                names = ["fnum_conflict"+str(i)],
                                         obj   = [-1.0/aircraft_count])#score_list[i]
        model.variables.set_types("fnum_conflict"+str(i), model.variables.type.binary)
    """
    z1 = m.addVars([("in_huaxing"+str(i) ,"fnum"+str(j)) for i in range(apron_count) for j in range(aircraft_count)],vtype = GRB.BINARY,name = "z1")
    z2 = m.addVars([("out_huaxing"+str(i) ,"fnum"+str(j)) for i in range(apron_count) for j in range(aircraft_count)],vtype = GRB.BINARY,name = "z2")
    """
    for i in range(huaxing_count):
        for j in range(aircraft_count):
            model.variables.add(
                                names = ["in_huaxing"+str(i) +"fnum"+str(j)],
                                         obj   = [0])#score_list[i]
            model.variables.set_types("in_huaxing"+str(i) +"fnum"+str(j), model.variables.type.binary)
    
    for i in range(huaxing_count):
        for j in range(aircraft_count):
            model.variables.add(
                                names = ["out_huaxing"+str(i) +"fnum"+str(j)],
                                         obj   = [0])#score_list[i]
            model.variables.set_types("out_huaxing"+str(i) +"fnum"+str(j), model.variables.type.binary)
    """
    obj = LinExpr()
    for i in range(apron_count):
        for j in range(aircraft_count):
            if i in N:
                obj += (score_list[i]+pop_score[j])* x['apron'+str(i),'fnum'+str(j)]
            else:
                obj += score_list[i]* x['apron'+str(i),'fnum'+str(j)]
                
    for i in range(aircraft_count):
        obj += -1.0/aircraft_count*y['fnum_conflict'+str(i)]
    m.setObjective(obj,GRB.MAXIMIZE)
    m.addConstrs((y["fnum_conflict"+str(i)] == 1 for i in con_conflict_list), name ='c0')
    print ("begin to set constraints_1",time.ctime())
    m.addConstrs((x['apron'+str(i),'fnum'+str(j)] <= choose_apron[j][i] for i in range(apron_count)
                                                                       for j in range(aircraft_count)),name='c1')
    
    """
    constraints_1=[]
    right_value_1=[]
    for i in range(apron_count):
        for j in range(aircraft_count):
            constraints_1.append(cplex.SparsePair(ind = ["apron"+str(i) +"fnum"+str(j)], val = [1.0] ))
            right_value_1.append(choose_apron[j][i]+0.1)
    model.linear_constraints.add(lin_expr = constraints_1 ,senses = ["L"]*len(constraints_1), rhs = right_value_1)
    """
    print ("begin to set constraints_2",time.ctime())
    
    m.addConstrs((LinExpr([1.0]*apron_count,[x['apron'+str(j),'fnum'+str(i)] 
                for j in range(apron_count)])<= 1 for i in range(aircraft_count)),name='c2')
    
    """
    constraints_2=[]
    for i in range(aircraft_count):
        constraints_2.append(cplex.SparsePair(ind = ["apron"+str(j) +"fnum"+str(i) for j in range(apron_count)],val = [1.0]*apron_count ))
    model.linear_constraints.add(lin_expr = constraints_2,senses = ["L"]*len(constraints_2), rhs = [1.1]*len(constraints_2))
    """
    print ("begin to set constraints_3",time.ctime())
    m.addConstrs((LinExpr([1.0]*len(in_huaxing[j]),[x["apron"+str(k) ,"fnum"+str(i)] for k in in_huaxing[j]])==z1["in_huaxing"+str(j) ,"fnum"+str(i)]
                    for i in range(aircraft_count) for j in range(huaxing_count)),name='c3')
    
    """
    constraints_3=[]
    for i in range(aircraft_count):
        for j in range(huaxing_count):
            constraints_3.append(cplex.SparsePair(ind=["in_huaxing"+str(j) +"fnum"+str(i)]+["apron"+str(k) +"fnum"+str(i) for k in in_huaxing[j]],
                                                                          val=[-1]+[1.0]*len(in_huaxing[j])))
    model.linear_constraints.add(lin_expr = constraints_3,senses = ["E"]*len(constraints_3), rhs = [0]*len(constraints_3))
    """
    print ("begin to set constraints_4",time.ctime())
    m.addConstrs((LinExpr([1.0]*len(out_huaxing[j]),[x["apron"+str(k) ,"fnum"+str(i)] for k in out_huaxing[j]])==z2["out_huaxing"+str(j) ,"fnum"+str(i)] 
                    for i in range(aircraft_count) for j in range(huaxing_count)),name='c4')
    """
    constraints_4=[]
    for i in range(aircraft_count):
        for j in range(huaxing_count):
            constraints_4.append(cplex.SparsePair(ind=["out_huaxing"+str(j) +"fnum"+str(i)]+["apron"+str(k) +"fnum"+str(i) for k in out_huaxing[j]],
                                                                          val=[-1]+[1.0]*len(out_huaxing[j])))
    model.linear_constraints.add(lin_expr =constraints_4,senses = ["E"]*len(constraints_4), rhs = [0]*len(constraints_4))
    """
    print ("begin to set constraints_5",time.ctime())
    m.addConstrs((LinExpr([-1.0,1.0,1.0],[y["fnum_conflict"+str(i)],z1["in_huaxing"+str(j) ,"fnum"+str(i)],z1["in_huaxing"+str(j) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count) if len(conflict_in_5min[i])!=0 for k in conflict_in_5min[i] for j in range(huaxing_count) if choose_in_huaxing[i][j]==1 and choose_in_huaxing[k][j]==1 ) ,name='c5')
    """
    constraints_5=[]
    for i in range(aircraft_count):
        if len(conflict_in_5min[i])!=0:
            for k in conflict_in_5min[i]:
                for j in range(huaxing_count):
                    if choose_in_huaxing[i][j]==1 and choose_in_huaxing[k][j]==1:
                        constraints_5.append(cplex.SparsePair(ind = ["fnum_conflict"+str(i)]+["in_huaxing"+str(j) +"fnum"+str(i),"in_huaxing"+str(j) +"fnum"+str(k)],
                                                        val = [-1]+[1.0]*2 ))
    model.linear_constraints.add(lin_expr =constraints_5,senses = ["L"]*len(constraints_5), rhs = [1.1]*len(constraints_5))
    """
    print ("begin to set constraints_6",time.ctime())
    m.addConstrs((LinExpr([-1.0,1.0,1.0],[y["fnum_conflict"+str(i)],z1["in_huaxing"+str(j) ,"fnum"+str(i)],z2["out_huaxing"+str(j) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count) if len(conflict_in_out_5min[i])!=0 for k in conflict_in_out_5min[i] for j in range(huaxing_count) if choose_in_huaxing[i][j]==1 and choose_out_huaxing[k][j]==1 ) ,name='c6')
    """
    constraints_6=[]
    for i in range(aircraft_count):
        if len(conflict_in_out_5min[i])!=0:
            for k in conflict_in_out_5min[i]:
                for j in range(huaxing_count):
                    if choose_in_huaxing[i][j]==1 and choose_out_huaxing[k][j]==1:
                        constraints_6.append(cplex.SparsePair(ind = ["fnum_conflict"+str(i)]+["in_huaxing"+str(j) +"fnum"+str(i),"out_huaxing"+str(j) +"fnum"+str(k)],
                                                        val = [-1]+[1.0]*2 ))
    model.linear_constraints.add(lin_expr =constraints_6,senses = ["L"]*len(constraints_6), rhs = [1.1]*len(constraints_6))
    """
    print ("begin to set constraints_7",time.ctime())
    m.addConstrs((LinExpr([-1.0,1.0,1.0],[y["fnum_conflict"+str(i)],z2["out_huaxing"+str(j) ,"fnum"+str(i)],z2["out_huaxing"+str(j) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count) if len(conflict_out_5min[i])!=0 for k in conflict_out_5min[i] for j in range(huaxing_count) if choose_out_huaxing[i][j]==1 and choose_out_huaxing[k][j]==1 ) ,name='c7')
    """
    constraints_7=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_7:laod',i
        if len(conflict_out_5min[i])!=0:
            for k in conflict_out_5min[i]:
                for j in range(huaxing_count):
                    if choose_out_huaxing[i][j]==1 and choose_out_huaxing[k][j]==1:
                        constraints_7.append(cplex.SparsePair(ind = ["fnum_conflict"+str(i)]+["out_huaxing"+str(j) +"fnum"+str(i),"out_huaxing"+str(j) +"fnum"+str(k)],
                                                        val = [-1]+[1.0]*2 ))
    model.linear_constraints.add(lin_expr =constraints_7,senses = ["L"]*len(constraints_7), rhs = [1.1]*len(constraints_7))
    """
    print ("begin to set constraints_8",time.ctime())
    m.addConstrs((LinExpr([-1.0,1.0,1.0],[y["fnum_conflict"+str(i)],z2["out_huaxing"+str(j) ,"fnum"+str(i)],z1["in_huaxing"+str(j) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count) if len(conflict_out_in_5min[i])!=0 for k in conflict_out_in_5min[i] for j in range(huaxing_count) if choose_out_huaxing[i][j]==1 and choose_in_huaxing[k][j]==1 ) ,name='c8')
    """
    constraints_8=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_8:laod',i
        if len(conflict_out_in_5min[i])!=0:
            for k in conflict_out_in_5min[i]:
                for j in range(huaxing_count):
                    if choose_out_huaxing[i][j]==1 and choose_in_huaxing[k][j]==1:
                        constraints_8.append(cplex.SparsePair(ind = ["fnum_conflict"+str(i)]+["out_huaxing"+str(j) +"fnum"+str(i),"in_huaxing"+str(j) +"fnum"+str(k)],
                                                        val = [-1]+[1.0]*2 ))
    model.linear_constraints.add(lin_expr =constraints_8,senses = ["L"]*len(constraints_8), rhs = [1.1]*len(constraints_8))
    """
    gongwu=[]
    for i in [413,414,416,417,418,419]:
        gongwu.append(apron_dict[str(i)])
    gongwu_b=[]
    for i in ['413A','413A','416A','416A','419A','419A']:
        gongwu_b.append(apron_dict[str(i)])
    chaifen=[]
    for i in range(apron_count):
        if apron[i][:1]=='5':
            chaifen.append(i)
    
    print ("begin to set constraints_9",time.ctime())
    m.addConstrs((LinExpr([1.0,1.0],[x["apron"+str(j) ,"fnum"+str(i)],x["apron"+str(j) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count)  for k in conflict_8min[i] for j in range(apron_count) if len(conflict_8min[i])!=0 and choose_apron[i][j]==1 and choose_apron[k][j]==1 and not j in gongwu and not j in gongwu_b and not j in chaifen ) ,name='c9')
    
    """
    constraints_9=[]   
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_9:laod',i
        #print "load",i
        if  len(conflict_8min[i])!=0:
            for k in conflict_8min[i]:
                for j in range(apron_count):
                    if choose_apron[i][j]==1 and choose_apron[k][j]==1 :
                        if not j in gongwu and not j in gongwu_b and not j in chaifen:
                            constraints_9.append(cplex.SparsePair(ind = ["apron"+str(j) +"fnum"+str(i),"apron"+str(j) +"fnum"+str(k)],
                                                        val = [1.0]*2 ))
    model.linear_constraints.add(lin_expr = constraints_9, senses = ["L"]*len(constraints_9), rhs = [1.1]*len(constraints_9))
    """
    print ("begin to set constraints_10",time.ctime())
    m.addConstrs((LinExpr([1.0,1.0,1.0,1.0],[x["apron"+str(gongwu[j]) ,"fnum"+str(i)],x["apron"+str(gongwu[j]) ,"fnum"+str(k)],x["apron"+str(gongwu_b[j]) ,"fnum"+str(i)],x["apron"+str(gongwu_b[j]) ,"fnum"+str(k)]])<= 1
                    for i in range(aircraft_count) if  len(conflict_8min[i])!=0 for k in conflict_8min[i] for j in range(len(gongwu))
                    if (choose_apron[i][gongwu[j]]==1 or choose_apron[i][gongwu_b[j]]==1) and (choose_apron[k][gongwu[j]]==1 or choose_apron[k][gongwu_b[j]]==1) ) ,name='c10')
    """
    constraints_10=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_10:laod',i
        #print "load",i
        if  len(conflict_8min[i])!=0:
            for k in conflict_8min[i]:
                 for j in range(len(gongwu)):
                    if (choose_apron[i][gongwu[j]]==1 or choose_apron[i][gongwu_b[j]]==1) and (choose_apron[k][gongwu[j]]==1 or choose_apron[k][gongwu_b[j]]==1) :
                        constraints_10.append(cplex.SparsePair(ind = ["apron"+str(gongwu[j]) +"fnum"+str(i),"apron"+str(gongwu[j]) +"fnum"+str(k),"apron"+str(gongwu_b[j]) +"fnum"+str(i),"apron"+str(gongwu_b[j]) +"fnum"+str(k)],
                                                        val = [1.0]*4 ))
    model.linear_constraints.add(lin_expr = constraints_10, senses = ["L"]*len(constraints_10), rhs = [1.1]*len(constraints_10))
    """
    def avialible(i,j,l):
        flag_1=0
        flag_2=0
        for k in l:
            if choose_apron[i][k]==1:
                flag_1=1
        for k in l:
            if choose_apron[j][k]==1:
                flag_2=1
        if flag_1==1 and flag_2==1:
            return True
        else:
            return False
    
    chaifen_group=[]
    for i in range(501,515):
        chaifen_group.append([apron_dict[str(i)],apron_dict[str(i)+'L']])
        chaifen_group.append([apron_dict[str(i+1)],apron_dict[str(i)+'L']])
    for i in range(502,515):
        chaifen_group.append([apron_dict[str(i)],apron_dict[str(i)+'JU'],apron_dict[str(i)+'JL']])
        chaifen_group.append([apron_dict[str(i)+'JL'],apron_dict[str(i-1)+'L']])
        chaifen_group.append([apron_dict[str(i)+'JU'],apron_dict[str(i)+'L']])
    
    chaifen_group.append([apron_dict['501'],apron_dict['501J']])  
    chaifen_group.append([apron_dict['515'],apron_dict['515J']]) 
    chaifen_group_count=len(chaifen_group)
    print ("begin to set constraints_11",time.ctime())
    m.addConstrs((LinExpr([1.0]*2*len(chaifen_group[j]),[x["apron"+str(l) ,"fnum"+str(i)] for l in chaifen_group[j]]+[x["apron"+str(l),"fnum"+str(k)] for l in chaifen_group[j]])<= 1
                    for i in range(aircraft_count) if  len(conflict_8min[i])!=0 for k in conflict_8min[i] for j in range(chaifen_group_count)
                    if avialible(i,k,chaifen_group[j]))  ,name='c11')
    """
    constraints_11=[]    
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_11:laod',i
        #print "load",i
        if  len(conflict_8min[i])!=0:
            for k in conflict_8min[i]:
                 for j in range(chaifen_group_count):
                    if avialible(i,k,chaifen_group[j]):
                        constraints_11.append(cplex.SparsePair(ind = ["apron"+str(l) +"fnum"+str(i) for l in chaifen_group[j]]+["apron"+str(l) +"fnum"+str(k) for l in chaifen_group[j]],
                                                        val = [1.0]*2*len(chaifen_group[j]) ))
    model.linear_constraints.add(lin_expr = constraints_11, senses = ["L"]*len(constraints_11), rhs = [1.1]*len(constraints_11))
     """                   
    def gongwu_conflict(t1,t2,t3):
        if t3>t1-300 and t3<t2+300:
            return True
        else:
            return False
        
    gongwu_zhanyong=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if i!=j and choose_apron[i][apron_dict['413A']]==1 and gongwu_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j]) :
                list_1.append(j)
        gongwu_zhanyong.append(list_1)
    """
    gongwu_group=[]
    for i in range(415,430):
        gongwu_group.append([apron_dict['413A'],apron_dict[str(i)]])
    for i in range(418,430):
        gongwu_group.append([apron_dict['416A'],apron_dict[str(i)]])
    for i in range(420,430):
        gongwu_group.append([apron_dict['419A'],apron_dict[str(i)]])
    gongwu_group.append([apron_dict['413A'],apron_dict['416A']])
    gongwu_group.append([apron_dict['413A'],apron_dict['419A']])
    gongwu_group.append([apron_dict['416A'],apron_dict['419A']])
    print ("begin to set constraints_12",time.ctime())
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_12:laod',i
        if  len(gongwu_zhanyong[i])!=0:
            for k in gongwu_zhanyong[i]:
                for j in gongwu_group:
                    if choose_apron[k][j[1]]==1 and choose_apron[i][j[0]]:
                        m.addConstr(LinExpr([1.0]*2,[x["apron"+str(j[0]),"fnum"+str(i)],x["apron"+str(j[1]),"fnum"+str(k) ]])<= 1,
                'c12'+str(i)+str(k)+str(j[0])+str(j[1]))
    """
    gongwu_group=[]
    gongwu_group_inner=[apron_dict['413A'],apron_dict['416A'],apron_dict['419A']]
    for i in range(415,430):
        gongwu_group_inner.append(apron_dict[str(i)])
    gongwu_group.append(gongwu_group_inner)
    gongwu_group_inner=[apron_dict['416A'],apron_dict['419A']]
    for i in range(418,430):
        gongwu_group_inner.append(apron_dict[str(i)])
    gongwu_group.append(gongwu_group_inner)
    gongwu_group_inner=[apron_dict['419A']]
    for i in range(420,430):
        gongwu_group_inner.append(apron_dict[str(i)])
    gongwu_group.append(gongwu_group_inner)
    print "begin to set constraints_12",time.ctime()
    constraints_12=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_12:laod',i
        if  len(gongwu_zhanyong[i])!=0:
            for k in gongwu_zhanyong[i]:
                for j in gongwu_group:
                    if sum(choose_apron[k][j[l]] for l in range(len(j)) if l!=0)>=1 and choose_apron[i][j[0]]==1:
                        m.addConstr(LinExpr([1.0]*len(j),[x["apron"+str(j[0]),"fnum"+str(i)]]+[x["apron"+str(j[l]),"fnum"+str(k) ] for l in range(len(j)) if l!=0])<= 1,
                'c12'+str(i)+str(k)+str(j[0]))
    """
    print ("begin to set constraints_12",time.ctime())
    m.addConstrs((LinExpr([1.0]*4,[x["apron"+str(j[0]),"fnum"+str(i)],x["apron"+str(j[0]),"fnum"+str(k)],x["apron"+str(j[1]),"fnum"+str(i)],x["apron"+str(j[1]),"fnum"+str(k) ]])<= 1
                    for i in range(aircraft_count)   if  len(gongwu_zhanyong[i])!=0 for k in gongwu_zhanyong[i] for j in gongwu_group
                    if choose_apron[k][j[1]]==1)  ,name='c12')
    
    constraints_12=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_12:laod',i
        if  len(gongwu_zhanyong[i])!=0:
            for k in gongwu_zhanyong[i]:
                for j in gongwu_group:
                    if choose_apron[k][j[1]]==1:
                        constraints_12.append(cplex.SparsePair(ind = ["apron"+str(j[0]) +"fnum"+str(i),"apron"+str(j[0]) +"fnum"+str(k),"apron"+str(j[1]) +"fnum"+str(i),"apron"+str(j[1]) +"fnum"+str(k) ],
                                                        val = [1.0]*4 ))
    model.linear_constraints.add(lin_expr = constraints_12, senses = ["L"]*len(constraints_12), rhs = [1.1]*len(constraints_12))
    """
                                    
    def linshi_conflict(t1,t2,t3,t4):
        if t3>t1-300 and t3<t2+300:
            return True
        elif t4>t1-300 and t4<t2+300:
            return True
        else:
            return False
        
    linshi_zhanyong=[]
    for i in data.index:
        list_1=[]
        for j in data.index:
            if  linshi_conflict(data['in_time_stamp'][i],data['out_time_stamp'][i],data['in_time_stamp'][j],data['out_time_stamp'][j]) and i!=j:
                list_1.append(j)
        linshi_zhanyong.append(list_1)
    
    linshi_group=[]
    for i in [101,102,103,104]:
        linshi_group.append([apron_dict['L101'],apron_dict[str(i)]])
    for i in [101,102,103,104]:
        linshi_group.append([apron_dict['L103'],apron_dict[str(i)]])
    for i in [108,109,110]:
        linshi_group.append([apron_dict['L110'],apron_dict[str(i)]])
    for i in [110,111,112,113,114]:
        linshi_group.append([apron_dict['L113'],apron_dict[str(i)]])
    for i in [110,111,112,113,114,115,116,'L113']:
        linshi_group.append([apron_dict['L115'],apron_dict[str(i)]])
    for i in [119,120,121]:
        linshi_group.append([apron_dict['L121'],apron_dict[str(i)]])
    for i in [121,122,123,124,125,126]:
        linshi_group.append([apron_dict['L124'],apron_dict[str(i)]])
    for i in [122,123,124,125,126,127,'L124']:
        linshi_group.append([apron_dict['L126'],apron_dict[str(i)]])
    for i in [131,132,133,135,136,137,138]:
        linshi_group.append([apron_dict['L135'],apron_dict[str(i)]])
    for i in [130,131,132,133,135,136,137,138,139,'L135']:
        linshi_group.append([apron_dict['L138'],apron_dict[str(i)]])
    linshi_group.append([apron_dict['L140'],apron_dict[str(140)]])
    for i in [201,202,203,401,402]:
        linshi_group.append([apron_dict['L201'],apron_dict[str(i)]])
    for i in [201,202,203,204,401,402,403,'L201']:
        linshi_group.append([apron_dict['L203'],apron_dict[str(i)]])
    for i in [212,213,214,215,216]:
        linshi_group.append([apron_dict['L214'],apron_dict[str(i)]])
    for i in [211,212,213,214,215,216,217,'L214']:
        linshi_group.append([apron_dict['L216'],apron_dict[str(i)]])
    for i in [221,222,223,224,225,226,227,228,'L224']:
        linshi_group.append([apron_dict['L222'],apron_dict[str(i)]])
    for i in [222,223,224,225,226]:
        linshi_group.append([apron_dict['L224'],apron_dict[str(i)]])
    for i in [227,228]:
        linshi_group.append([apron_dict['L227'],apron_dict[str(i)]])
    for i in [233,234,235,236,237]:
        linshi_group.append([apron_dict['L235'],apron_dict[str(i)]])
    for i in [232,233,234,235,236,237,238,239,'L235']:
        linshi_group.append([apron_dict['L238'],apron_dict[str(i)]])
    for i in [301,302,303,304]:
        linshi_group.append([apron_dict['L301'],apron_dict[str(i)]])
    for i in [301,302,303,304,305,'L301']:
        linshi_group.append([apron_dict['L303'],apron_dict[str(i)]])
    for i in [513,514,515,'513L','514L','513JU','513JL','514JU','514JL','515J']:
        linshi_group.append([apron_dict['L515'],apron_dict[str(i)]])
    for i in ['GY01','GY02','GY03','GY04','GY05','GY06','LGY06']:
        linshi_group.append([apron_dict['LGY03'],apron_dict[str(i)]])
    for i in ['GY04','GY05','GY06']:
        linshi_group.append([apron_dict['LGY06'],apron_dict[str(i)]])
    for i in ['GY07','GY08','GY09']:
        linshi_group.append([apron_dict['LGY07'],apron_dict[str(i)]])
    for i in ['GY07','GY08','GY09','GY10','GY11','GY12','LGY07']:
        linshi_group.append([apron_dict['LGY10'],apron_dict[str(i)]])
    print ("begin to set constraints_13",time.ctime())
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_13:laod',i
        if  len(linshi_zhanyong[i])!=0:
            for k in linshi_zhanyong[i]:
                for j in linshi_group:
                    if choose_apron[k][j[1]]==1 and choose_apron[i][j[0]]==1:
                        m.addConstr(LinExpr([1.0]*2,[x["apron"+str(j[0]),"fnum"+str(i)],x["apron"+str(j[1]),"fnum"+str(k) ]])<= 1,'c13'+str(i)+str(k)+str(j[0])+str(j[1]))
    """
    constraints_13=[]
    for i in range(aircraft_count):
        #if i%50==0:
        #    print 'constraints_13:laod',i
        if  len(linshi_zhanyong[i])!=0:
            for k in linshi_zhanyong[i]:
                for j in linshi_group:
                    if choose_apron[k][j[1]]==1 and choose_apron[k][j[0]]==1:
                        constraints_13.append(cplex.SparsePair(ind = ["apron"+str(j[0]) +"fnum"+str(i),"apron"+str(j[0]) +"fnum"+str(k),"apron"+str(j[1]) +"fnum"+str(i),"apron"+str(j[1]) +"fnum"+str(k) ],
                                                        val = [1.0]*4 ))
    model.linear_constraints.add(lin_expr = constraints_13, senses = ["L"]*len(constraints_13), rhs = [1.1]*len(constraints_13))
    
    model.solve()
    model.solution.write('d:/cplex_result')
    
    score=0
    for i in range(apron_count):
        for j in range(aircraft_count):
            #if i in N:
                score=score+model.solution.get_values("apron"+str(i) +"fnum"+str(j))
    print score
    
    conflict=0
    for i in range(aircraft_count):
        conflict=conflict+model.solution.get_values("fnum_conflict"+str(i))
    print conflict
    """
    apron_new=[]
    for i in apron:
        if i[-2:]=='JL':
            apron_new.append(i[:3]+'ZJ')
        elif i[-2:]=='JU':
            apron_new.append(i[:3]+'YJ')
        elif i=='501J':
            apron_new.append('501ZJ')
        elif i=='515J':
            apron_new.append('515YJ')
        else:
            apron_new.append(i)
    """
    def mycallback(model,where):
        if where == GRB.Callback.MIPSOL:
            # MIP solution callback
            nodecnt = model.cbGet(GRB.Callback.MIPSOL_NODCNT)
            obj = model.cbGet(GRB.Callback.MIPSOL_OBJ)
            solcnt = model.cbGet(GRB.Callback.MIPSOL_SOLCNT)
            x1 = model.cbGetSolution(x)
            #y1 = model.cbGetSolution(y)
            #z1 = model.cbGetSolution(z)
            print('**** New solution at node %d, obj %g, sol %d, ' % (nodecnt, obj, solcnt))
            result_list=[]
            for i in range(apron_count):
                for j in range(aircraft_count):
                    if x1['apron'+str(i),'fnum'+str(j)]==1:
                        result_list.append([data.loc[j,'fnum'],apron_new[i]])
            result=DataFrame(result_list)
            result.to_csv('./result_callback.csv')
    """
    print (time.ctime())
    m.setParam(GRB.Param.Threads,4)
    #m.setParam('mipgap',0.001)
    m.setParam('Method',0)
    m.optimize() 
    
    
    
    result_list=[]
    for j in range(aircraft_count):        
        for i in range(apron_count):
                if x['apron'+str(i),'fnum'+str(j)].x==1:
                    result_list.append([data['fnum'][j],apron_new[i]])
    
    for i in chushijie.index:
        if not chushijie['fnum'][i] in list(data['fnum']) and not chushijie['fnum'][i] in list(con['fnum']):
            result_list.append([chushijie['fnum'][i],chushijie['apron'][i]])
                    
    result=DataFrame(result_list,columns=['fnum','apron'])
    result.to_csv('./new_result.csv',index=False)
    chushijie=copy.deepcopy(result)  