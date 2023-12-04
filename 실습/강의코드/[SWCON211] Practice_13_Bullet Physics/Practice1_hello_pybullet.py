import pybullet as p
from time import sleep
import pybullet_data


physicsClient = p.connect(p.GUI) #pyBullet의 GUI를 사용할 수 있도록 설정

p.setAdditionalSearchPath(pybullet_data.getDataPath()) # 물리 실험에 필요한 Object들의 데이터가 들어간 data_path 가져오기

p.setGravity(0, 0, -10) # 중력을 10으로 설정 pyBullet에서는 y축의 역할을 z축이 대신한다.
planeId = p.loadURDF("plane.urdf") # plane Object를 불러옴

cubeStartPos = [0, 0, 1] 
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0]) #물체의 생성 위치와 각도를 설정

boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)



#실행부 = main()
while 1:
  
  p.stepSimulation()
