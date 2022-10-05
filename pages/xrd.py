import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import re
st.title("XRD数据分析")
# 上传对应个数的文件
uploaded_files = st.file_uploader("1.上传txt文件", type="txt",accept_multiple_files=True)
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
def draw_xrd(x,y,file_name,line_color):
  fig,ax = plt.subplots()
  my_x_ticks = np.arange(10,90,10)
  plt.plot(x,y,linewidth=1,color=line_color,label=file_name)
  plt.xlabel('2 Theta',fontdict={'family':'Times New Roman','size':16})
  plt.ylabel('Intensity(a.u)',fontdict={'family':'Times New Roman','size':16})
  plt.xlim(10,80)
  plt.xticks(my_x_ticks,fontproperties='Times New Roman',size=14)
  plt.yticks([])
  ax.legend(loc='upper right')
  st.pyplot(fig)
# 根据上传文件数量生成对应个数的配置
for uploaded_file in uploaded_files:
    file_name_origin = uploaded_file.name
    file_name = re.sub(r'\.txt','',file_name_origin)
    st.write(file_name,"的XRD图例")
    array= pd.read_table(uploaded_file,sep="\t", header=None)
    tempx,tempy = transform_txt(array)
    # 生成配置文件
    st.sidebar.write(file_name,"的配置文件")
    # 颜色
    line_color = st.sidebar.color_picker('选择颜色', '#FF0000',key=file_name)
    # 绘图
    draw_xrd(tempx,tempy,file_name,line_color)
  
