from glob import glob
import os
import queue
import numpy as np
import re
def exist(file_path):
    return os.path.exists(file_path)

def getfiles(folder,abs_path=True):
    result=[]
    if folder[-1]=='/':
        folder+='*'
        
    if folder[-1] is not '*':
        folder+='/*'
        
    if len(folder) <2:
        return result   
    paths=queue.Queue()
    paths.put(folder)
    while not paths.empty():
        files=glob(paths.get())
        for num,path in enumerate(files):
            if os.path.isdir(path):
                paths.put(path+'/*')
            else:
                if not abs_path:
                    path=result.append(os.path.relpath(path,start=folder))
                
                result.append(path)
    return result

def filtbyext(files,filtstr):
    result=[]
    filters=filtstr.split('|')
    filters=set(filters)
    for file in files:
        ext=os.path.splitext(file)[1]
        if ext in filters:
            result.append(file)
            
    return result

def getfilesbyext(folder,ext,abs_path=True):
    files=getfiles(folder)
    files=filtbyext(files,ext)
    return files

def getfiledicbyext(folder,ext,abs_path=True):
    files=getfilesbyext(folder,ext)
    file_dic={}
    for _,f in enumerate(files):
        id=os.path.split(f)[-1]
        id=os.path.splitext(id)[0]
        id=id.lower()
        file_dic[id]=f
    return file_dic

def getfiledetails(file_path):
    (file_dir,tempfilename) = os.path.split(file_path)
    (file_name,file_ext) = os.path.splitext(tempfilename)
    return (file_dir,file_name,file_ext)

def path_match(path_str,path_pattern):
    match_obj=re.match(path_pattern,path_str,re.I)
    if match_obj:
        # print(match_obj)
        return match_obj.groups()
    else:
        return None


def path_search(path_str,path_pattern):
    search_obj=re.search(path_pattern,path_str,re.I)
    if search_obj:
        # print(match_obj)
        return search_obj.groups()
    else:
        return None

# if __name__=='__main__':
#     x,y,z=path_match('123left_write_45','123(left|right)_(read|write)_(45|135)')
#     print(x,y,z)
#     x,y,z=path_match('123right_read_135','123(left|right)_(read|write)_(45|135)')
#     print(x,y,z)