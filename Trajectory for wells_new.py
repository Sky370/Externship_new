import numpy as np
import pandas as pd
import pickle
import plotly.express as px
import os
# import warnings
# warnings.filterwarnings("ignore")

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'Directional Survey Data_6.15.2022.xlsx')

new = pd.read_excel(my_file)
tvd = [-x for x in new["TVDCalc"].tolist()]
sortedwells = list(set(new["WELL NAME"]))
# sortedwells.pop(0)
sortedwells.sort()

Build_rad = []
for i in range(len(sortedwells)):
    df = new[new["WELL NAME"] == sortedwells[i]]
    Md = df["MD"].to_list()
    TVD = df["TVDCalc"].to_list()
    INC = df["Inclination"].to_list()
    AZ = df["Azimuth"].to_list()
    DLS = df["DLSCalc"].to_list()
    crv_start = [i for i in range(len(TVD)-1, 0, -1) if TVD[i] - TVD[i-1] > 10 and INC[i] < 4]
    crv_end = [i-1 for i in range(1, len(TVD)) if TVD[i] - TVD[i-1] < 10 and INC[i] > 80]
    LL = Md[-1] - Md[crv_end[0]]
    Rad = 1/((np.deg2rad(INC[crv_end[0]])-np.deg2rad(INC[crv_start[0]]))/(Md[crv_end[0]]-Md[crv_start[0]]))
    Build_rad.append(Rad)
    print("Well name: {}, MD: {}, TVD: {}, Lateral Length: {}".format(sortedwells[i], Md[-1], max(TVD), LL))
    print("The Kick off point parameters are: MD is {}, TVD is {}, Incl is {}, Azim is {}".format(Md[crv_start[0]], TVD[crv_start[0]], INC[crv_start[0]], AZ[crv_start[0]]))
    print("The LAT point parameters are: MD is {}, TVD is {}, Incl is {}, Azim is {} \n".format(Md[crv_end[0]], TVD[crv_end[0]], INC[crv_end[0]], AZ[crv_end[0]]))
    

fig = px.line_3d(new, x="NSCalc", y="EWCalc", z=tvd, color="WELL NAME", labels={
    "NSCalc":"North-South", 
    "EWCalc":"East-West", 
    "z":"TVD",
    "WELL NAME":"WELL NAMES"
    })

fig1 = px.line(new, x= "NSCalc", y="DLSCalc", color="WELL NAME", labels={
    "NSCalc":"North-South",
    "DLSCalc":"DLS"
})
fig.update_traces(line_width=2.5)

fig2 = px.line(new, x="MD", y="3D_Tortuosity_Index", color="WELL NAME")
fig3 = px.line(new, x="NSCalc", y=tvd, color="WELL NAME", labels={
    "NSCalc":"North-South",
    "y":"TVD"
})

fig.show()
fig1.show()
fig2.show()
fig3.show()