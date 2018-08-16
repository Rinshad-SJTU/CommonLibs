import numpy as np
def gen_feature_from_file(file_path):
    try:
        loaded=np.load(file_path)
        data=loaded['x']
        label=loaded['y']
        return data,label
    except Exception as exp:
        print('Exception:',file_path)
        return None,None
    
