import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
st.write("""
# XRD数据分析
需要上传两个txt文件:标准卡片和测试结果
""")
def transform_txt(location):
  tempx = []
  tempy = []
  data = pd.read_table(location, sep="\t", header=None)
  for i in range(len(data)):
    temp = data[0][i].split()
    tempx.append(float(temp[0]))
    if temp[1]!= 'LTN':
      tempy.append(int(temp[1]))
    else:
      tempy.append(temp[1])
  del tempx[0]
  del tempy[0]
  return tempx, tempy
tempx,tempy = transform_txt('./XRD.txt')
fig,ax = plt.subplots()
my_x_ticks = np.arange(10,90,10)
plt.plot(tempx,tempy,linewidth=1,color='r',label='LIC-ZIF-67-M10')
plt.xlabel('2 Theta',fontdict={'family':'Times New Roman','size':16})
plt.ylabel('Intensity(a.u)',fontdict={'family':'Times New Roman','size':16})
plt.xlim(10,80)
plt.xticks(my_x_ticks,fontproperties='Arial',size=14)
plt.yticks([])
ax.legend(loc='upper right')
st.pyplot(fig)
