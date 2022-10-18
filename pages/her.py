import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import streamlit as st
import pandas as pd
import re
st.title("HER_LSV数据分析")
file_name_arr=[]
color_arr=[]
over_voltage=[]
fig,ax = plt.subplots()
# 横坐标
def transform_txt(data):
  tempx = (np.array(data[0])+0.8663)*1000
  tempy = np.array(data[1])/0.237
  return tempx,tempy
def get_her_lsv_info(x,y):
  # 起始电位
  for j in range(len(y)):
    if(round(y[j],0) == -10):
      over_voltage.append(round(x[j],2))
      break
def draw_her(x,y,name,index):
    get_her_lsv_info(x,y)
    # 生成一个曲线图
    ax.plot(x,y,linewidth=3,color=color_arr[index],label=name)
    plt.xlabel('Potential (mV vs.RHE)',fontsize=16,family='Arial',fontweight='bold')
    plt.ylabel('Current density (mA cm-2)',fontsize=16,family='Arial',fontweight='bold')
    plt.xticks(fontsize=14,family='Arial',fontweight='bold')
    plt.yticks(fontsize=14,family='Arial',fontweight='bold')
    plt.axhline(-10,c="grey",lw=2,ls="--")
    ax.set_xlim(-300,0)
    ax.set_ylim(-20,5)
    return plt
# 上传文件
uploaded_files = st.file_uploader("上传txt文件", type="txt",accept_multiple_files=True,key='basic')
# 文件上传完毕，推送到数组中
if uploaded_files:
  for index,file in enumerate(uploaded_files):
    # 去掉后缀
    file_name = re.sub(r'\.txt','',file.name)
    file_name_arr.append(file_name)
    # 读取文件
    array= pd.read_table(file,sep="\t", header=None)
    # 拿到转换后的数据
    tempx,tempy = transform_txt(array)
    # 生成颜色的配置文件
    st.sidebar.write(file_name,"的配置文件")
    line_color = st.sidebar.color_picker('选择颜色', '#FF0000',key=file_name)
    color_arr.append(line_color)
    # 绘图
    plt = draw_her(tempx,tempy,file_name,index)
    font = font_manager.FontProperties(family='Arial',weight='bold',style='normal',size=12)
    plt.legend(loc='upper left',prop=font,edgecolor='white')
" ## 图例 🎉"
fig
" ## 过电位表"
def draw_voltage_bar(data):
    fig,ax = plt.subplots()
    newdata = np.array(data)*-1
    for index,file in enumerate(newdata):
      ax.bar(file_name_arr[index],file,color=color_arr[index])
      ax.set_ylim(50,100)
    plt.xticks(fontsize=10,family='Arial',fontweight='bold',rotation=45)
    plt.yticks(fontsize=14,family='Arial',fontweight='bold')
    plt.ylabel('Potential (mV vs.RHE)',fontsize=16,family='Arial',fontweight='bold')
    for a,b in zip(file_name_arr,newdata):
      plt.text(a,b,b,ha='center',va='bottom',fontsize=13,family='Arial',fontweight='bold')
    return fig
start_fig = draw_voltage_bar(over_voltage)
start_fig