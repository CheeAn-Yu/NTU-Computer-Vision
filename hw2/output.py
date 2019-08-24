import numpy as np
import pandas as pd
res=np.array([[1,2,3],[1,2,4],[3,3,3]])
np.savetxt("IO.txt",res,delimiter=",")
df=pd.DataFrame(res)
df.to_csv("IO.csv")