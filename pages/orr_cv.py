import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import streamlit as st
import pandas as pd
import re
st.title("ORR_CV数据分析")
color_arr=[]
fig,ax = plt.subplots()
# 因为是氧气和氩气的对比，所以只传两条曲线，因此可以精简。
def transform_txt(data):
  tempx = np.array(data[0])+0.8663
  tempy = np.array(data[1])/0.237
  return tempx,tempy
def draw_orr_cv(x,y,name,index):
  ax.plot(x,y,linewidth=1,color=color_arr[index],label=name)
  plt.legend(loc='upper right')
  plt.xlabel('E (V vs.RHE)',fontsize=16,family='Times New Roman',fontweight='bold')
  plt.ylabel('J (mA cm-2)',fontsize=16,family='Times New Roman',fontweight='bold')
  plt.xticks(fontsize=14,family='Times New Roman',fontweight='bold')
  plt.yticks(fontsize=14,family='Times New Roman',fontweight='bold')
  return plt
# 上传文件
uploaded_files = st.file_uploader("上传txt文件", type="txt",accept_multiple_files=True,key='basic')
# 文件上传完毕，推送到数组中
if uploaded_files:
  for index,file in enumerate(uploaded_files):
    # 去掉后缀
    file_name = re.sub(r'\.txt','',file.name)
    # 读取文件
    array= pd.read_table(file,sep="\t", header=None)
    # 拿到转换后的数据
    tempx,tempy = transform_txt(array)
    # 生成颜色的配置文件
    st.sidebar.write(file_name,"的配置文件")
    line_color = st.sidebar.color_picker('选择颜色', '#FF0000',key=file_name)
    color_arr.append(line_color)
    # 绘图
    draw_orr_cv(tempx,tempy,file_name,index)
fig