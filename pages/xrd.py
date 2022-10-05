from turtle import color
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import streamlit as st
import pandas as pd
import re
st.title("XRD数据分析")
datax=[]
datay=[]
file_name_arr=[]
color_arr=[]
def transform_txt(data):
  tempx = []
  tempy = []
  for i in range(len(data)):
    temp = data[0][i].split()
    tempx.append(float(temp[0]))
    if temp[1]!= 'LTN':
      tempy.append(int(temp[1]))
    else:
      tempy.append(temp[1])
  del tempx[0]
  del tempy[0]
  return tempx,tempy
def draw_xrd():
  my_x_ticks = np.arange(10,90,10)
  fig, axs = plt.subplots(len(datax),1,sharex=True)
  st.write(len(datax))
  # 移除垂直方向的空白
  fig.subplots_adjust(hspace=0)
  # 绘制
  for i in range(len(datax)):
    # 设置坐标轴名字
    axs[i].plot(datax[i],datay[i],linewidth=1,color=color_arr[i],label=file_name_arr[i])
    # axs[i].set_xlabel('2 Theta',fontdict={'family':'Times New Roman','size':16})
    # axs[i].set_ylabel('Intensity(a.u)',fontdict={'family':'Times New Roman','size':16})
    # 设置横坐标范围
    axs[i].set_xlim(10,80)
    # 设置横纵坐标刻度
    axs[i].set_xticks(my_x_ticks)
    axs[i].set_xticklabels(my_x_ticks,family='Times New Roman',fontsize=14,fontweight='bold')
    axs[i].set_yticks([])
    # 设置图例
    # 字体
    font = font_manager.FontProperties(family='Times New Roman',weight='bold',style='normal',size=12)
    axs[i].legend(loc='upper right',prop=font,labelcolor=color_arr[i],edgecolor='white')
    
  # 绘图
  fig.supxlabel(t='2 Theta',x=0.5,y=0.01,fontsize=16,family='Times New Roman',fontweight='bold')
  fig.supylabel(t='Intensity(a.u)',x=0.08,y=0.5,fontsize=16,family='Times New Roman',fontweight='bold')
  
  return fig
def draw ():
  if uploaded_files:
    f = draw_xrd()
    st.pyplot(f)
# 上传文件
uploaded_files = st.file_uploader("上传txt文件", type="txt",accept_multiple_files=True)
# 文件上传完毕，推送到数组中
if uploaded_files:
  for file in uploaded_files:
    # 去掉后缀
    file_name = re.sub(r'\.txt','',file.name)
    # 读取文件
    array= pd.read_table(file,sep="\t", header=None)
    # 拿到x,y轴的数据放入数组中
    tempx,tempy = transform_txt(array)
    datax.append(tempx)
    datay.append(tempy)
    file_name_arr.append(file_name)
    # 配置
    st.sidebar.write(file_name,"的配置文件")
    line_color = st.sidebar.color_picker('选择颜色', '#FF0000',key=file_name)
    color_arr.append(line_color)
st.button("绘图",on_click=draw)