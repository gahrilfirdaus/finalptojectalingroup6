import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Matrix Transformation WebApp", layout="wide")
st.title("✨ Matrix Transformation WebApp")
st.write("Aplikasi untuk melakukan transformasi matriks: Translation, Scaling, Rotation, Shearing, Reflection.")

# INPUT KOORDINAT
st.sidebar.markdown("### Input coordinates (x, y)")
input_x = st.sidebar.number_input("X:", value=1.0, step=0.1)
input_y = st.sidebar.number_input("Y:", value=1.0, step=0.1)
original_point = np.array([input_x, input_y])

# TRANSFORMASI
transformation_type = st.sidebar.selectbox(
    "Transformation Type", ["Translation", "Scaling", "Rotation", "Shearing", "Reflection"]
)

# MATRIX FUNCTIONS
def translation_matrix(tx, ty): return np.array([[1,0,tx],[0,1,ty],[0,0,1]])
def scaling_matrix(sx, sy): return np.array([[sx,0,0],[0,sy,0],[0,0,1]])
def rotation_matrix(theta): c,s=np.cos(theta),np.sin(theta); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def shear_matrix(shx, shy): return np.array([[1,shx,0],[shy,1,0],[0,0,1]])
def reflection_matrix(opt):
    mats={"Reflect X-axis":np.array([[1,0,0],[0,-1,0],[0,0,1]]),
          "Reflect Y-axis":np.array([[-1,0,0],[0,1,0],[0,0,1]]),
          "Reflect y=x":np.array([[0,1,0],[1,0,0],[0,0,1]]),
          "Reflect y=-x":np.array([[0,-1,0],[-1,0,0],[0,0,1]])}
    return mats.get(opt,np.eye(3))

# PARAMETER INPUT
params = {}
if transformation_type=="Translation":
    params["tx"]=st.sidebar.number_input("Translate X",2.0,step=0.1)
    params["ty"]=st.sidebar.number_input("Translate Y",2.0,step=0.1)
elif transformation_type=="Scaling":
    params["sx"]=st.sidebar.number_input("Scale X",1.5,step=0.1)
    params["sy"]=st.sidebar.number_input("Scale Y",1.5,step=0.1)
elif transformation_type=="Rotation":
    params["angle"]=np.deg2rad(st.sidebar.slider("Rotation (°)",-360,360,45))
elif transformation_type=="Shearing":
    params["shx"]=st.sidebar.number_input("Shear X",0.5,step=0.1)
    params["shy"]=st.sidebar.number_input("Shear Y",0.0,step=0.1)
elif transformation_type=="Reflection":
    params["ref"]=st.sidebar.selectbox("Reflection",["Reflect X-axis","Reflect Y-axis","Reflect y=x","Reflect y=-x"])

# BUILD MATRIX 
builders={
    "Translation":lambda p:translation_matrix(p["tx"],p["ty"]),
    "Scaling":lambda p:scaling_matrix(p["sx"],p["sy"]),
    "Rotation":lambda p:rotation_matrix(p["angle"]),
    "Shearing":lambda p:shear_matrix(p["shx"],p["shy"]),
    "Reflection":lambda p:reflection_matrix(p["ref"])
}
M = builders.get(transformation_type,lambda p:np.eye(3))(params)

# POINT RESULT
transformed_point = (M @ [*original_point,1])[:2]

# DISPLAY
st.subheader("Original Point")
st.dataframe(pd.DataFrame(original_point.reshape(-1,1),columns=["value"]),use_container_width=True)

st.subheader("Transformation Matrix")
st.dataframe(pd.DataFrame(M),use_container_width=True)

st.subheader("Result Points")
st.dataframe(pd.DataFrame({"Original Point":original_point,"Transformed Point":transformed_point}),use_container_width=True)

# PLOT
fig,ax=plt.subplots()
ax.scatter(*original_point,s=100,label="Original Point",color="blue")
ax.scatter(*transformed_point,s=100,label="Transformed Point",color="orange")
ax.axhline(0,linewidth=1.5,color="black"); ax.axvline(0,linewidth=1.5,color="black")
ax.set_xlim(-8,12); ax.set_ylim(-8,12); ax.set_aspect("equal")
ax.legend(loc="upper right",fontsize=8)
for spine in ax.spines.values(): spine.set_visible(False)
st.pyplot(fig)

st.subheader("Final Transformation Matrix (High Precision)")
st.text(np.array2string(M,precision=25,suppress_small=False,max_line_width=500))
