import os
import glob

# #현재 파일 이름
# print(__file__)

# #현재 파일 실제 경로
# file = os.path.realpath(__file__)
# print(file)

# #현재 파일 절대 경로
# print(os.path.abspath(__file__))

# #현재 폴더 경로; 작업 폴더 기준
# print(os.getcwd())

# #현재 파일의 폴더 경로; 작업 파일 기준
# print(os.path.dirname(os.path.realpath(__file__)))

# #3.현재 디렉토리의 파일 리스트
# hole = os.listdir(os.getcwd())
# for i in range(0,8): 
#         print(hole[i])

root_dir = "./verticle/"
for (root, dirs, files) in os.walk(root_dir):
   
    if len(dirs) > 0:
        for i in range(0,2): 
            print(dirs[i])

    # if len(files) > 0:
    #     print(files)
