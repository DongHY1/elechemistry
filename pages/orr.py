import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import streamlit as st
import pandas as pd
import re
st.title("ORR-CV&LSV数据分析")
option = st.sidebar.selectbox('选择绘图类型：CV或LSV',('CV','LSV'))
file_name_arr=[]
color_arr=[]
density_arr=[]
start_voltage=[]
half_voltage=[]
fig,ax = plt.subplots()
# 因为是氧气和氩气的对比，所以只传两条曲线，因此可以精简。
def transform_txt(data):
  tempx = np.array(data[0])+0.8663
  tempy = np.array(data[1])/0.237
  return tempx,tempy
def draw_orr(x,y,name,index):
    get_orr_lsv_info(x,y)
    # 生成一个曲线图
    ax.plot(x,y,linewidth=3,color=color_arr[index],label=name)
    plt.xlabel('E (V vs.RHE)',fontsize=16,family='Arial',fontweight='bold')
    plt.ylabel('J (mA $\mathregular{cm^{-2}}$)',fontsize=16,family='Arial',fontweight='bold')
    plt.xticks(fontsize=14,family='Arial',fontweight='bold')
    plt.yticks(fontsize=14,family='Arial',fontweight='bold')
    if option == 'LSV':
      ax.set_xlim(0.2,1.0)
      ax.set_ylim(-6.5,0)

    return plt
def get_orr_lsv_info(x,y):
  # 极限电流密度
  for i in range(len(x)):
    if round(x[i],1) == 0.2:
      density_arr.append(round(y[i],2))
      # 半波电位
      # 得到极限电流密度的一半
      half_density = y[i]/2
      # 遍历y，找到对应的横坐标
      for i1 in range(len(y)):
        if round(y[i1],1) == round(half_density,1):
          half_voltage.append(round(x[i1],2))
          break
      break
  # 起始电位
  for j in range(len(y)):
    if(round(y[j],1) == -0.1):
      start_voltage.append(round(x[j],2))
      break
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
    plt = draw_orr(tempx,tempy,file_name,index)
    font = font_manager.FontProperties(family='Arial',weight='bold',style='normal',size=12)
    ax = plt.gca()
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    plt.legend(loc='lower right',prop=font,edgecolor='white',labelcolor='linecolor')
" ## 图例 🎉"
fig
if option == 'LSV':
  " ## 极限电流密度表"
  def draw_density_bar(data):
    fig,ax = plt.subplots()
    for index,file in enumerate(data):
      ax.bar(file_name_arr[index],file*(-1),color=color_arr[index])
    plt.xticks(fontsize=10,family='Arial',fontweight='bold',rotation=45)
    plt.yticks(fontsize=14,family='Arial',fontweight='bold')
    plt.ylabel('J (mA $\mathregular{cm^{-2}}$)',fontsize=16,family='Arial',fontweight='bold')
    for a,b in zip(file_name_arr,data):
      plt.text(a,b*(-1),b*(-1),ha='center',va='bottom',fontsize=13,family='Arial',fontweight='bold')
    return fig
  density_fig= draw_density_bar(density_arr)
  density_fig
  " ## 起始电位表"
  def draw_voltage_bar(data,xlim,ylim):
    fig,ax = plt.subplots()
    for index,file in enumerate(data):
      ax.bar(file_name_arr[index],file,color=color_arr[index])
      ax.set_ylim(xlim,ylim)
    plt.xticks(fontsize=10,family='Arial',fontweight='bold',rotation=45)
    plt.yticks(fontsize=14,family='Arial',fontweight='bold')
    plt.ylabel('E (V vs.RHE)',fontsize=16,family='Arial',fontweight='bold')
    for a,b in zip(file_name_arr,data):
      plt.text(a,b,b,ha='center',va='bottom',fontsize=13,family='Arial',fontweight='bold')
    return fig
  start_fig = draw_voltage_bar(start_voltage,0.8,1.1)
  start_fig
  " ## 半波电位表"
  half_fig = draw_voltage_bar(half_voltage,0.6,0.9)
  half_fig

