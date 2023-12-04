import pybullet as p
import time
import math
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetSimulation()
p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)


#PlayerSetting#############################################################
playerStartPos = [0, 0, 1] 
playerPos = playerStartPos

playerStartOrientation = p.getQuaternionFromEuler([0, 0, 90])

playerId = p.loadURDF("r2d2.urdf", playerStartPos, playerStartOrientation)

m_forward = 0
m_back = 0
m_left = 0
m_right = 0

######################################################################################


#CameraSetting###########################################################
p.resetDebugVisualizerCamera(5, 90, -30, playerPos)
#########################################################################

p.setGravity(0, 0, -10)
p.setRealTimeSimulation(0)

boxHalfLength = 0.5
boxHalfWidth = 2.5
boxHalfHeight = 0.1
segmentLength = 5

#발판들의 충돌 크기 설정
colBoxId = p.createCollisionShape(p.GEOM_BOX,
                                  halfExtents=[boxHalfLength, boxHalfWidth, boxHalfHeight])

mass = 1
visualShapeId = -1

################# 맵 생성######################
segmentStart = 0

# 발판 5개 생성
for i in range(segmentLength):
  p.createMultiBody(baseMass=0,
                    baseCollisionShapeIndex=colBoxId,
                    basePosition=[segmentStart, 0, -0.1])
  segmentStart = segmentStart - 1

# 높이를 다르게 하여 발판 생성
for i in range(segmentLength):
  height = 0
  if (i % 2):
    height = 0.5
  p.createMultiBody(baseMass=0,
                    baseCollisionShapeIndex=colBoxId,
                    basePosition=[segmentStart, 0, -0.1 + height])
  segmentStart = segmentStart - 1

baseOrientation = p.getQuaternionFromEuler([math.pi / 2., 0, math.pi / 2.])

# 수직 벽 생성
for i in range(segmentLength):
  p.createMultiBody(baseMass=0,
                    baseCollisionShapeIndex=colBoxId,
                    basePosition=[segmentStart, 0, -0.1])
  segmentStart = segmentStart - 1
  if (i % 2):
    p.createMultiBody(baseMass=0,
                      baseCollisionShapeIndex=colBoxId,
                      basePosition=[segmentStart, i % 3, -0.1 + height + boxHalfWidth],
                      baseOrientation=baseOrientation)

# 볼록 벽 생성
stoneId = p.createCollisionShape(p.GEOM_MESH, fileName="stone.obj")

for i in range(segmentLength):
  p.createMultiBody(baseMass=0,
                    baseCollisionShapeIndex=colBoxId,
                    basePosition=[segmentStart, 0, -0.1])
  width = 4
  for j in range(width):
    p.createMultiBody(baseMass=0,
                      baseCollisionShapeIndex=stoneId,
                      basePosition=[segmentStart, 0.5 * (i % 2) + j - width / 2., 0])
  segmentStart = segmentStart - 1

link_Masses = [1]
linkCollisionShapeIndices = [colBoxId]
linkVisualShapeIndices = [-1]
linkPositions = [[0, 0, 0]]
linkOrientations = [[0, 0, 0, 1]]
linkInertialFramePositions = [[0, 0, 0]]
linkInertialFrameOrientations = [[0, 0, 0, 1]]
indices = [0]
jointTypes = [p.JOINT_REVOLUTE]
axis = [[1, 0, 0]]


baseOrientation = [0, 0, 0, 1]
sphereRadius = 0.05
colSphereId = p.createCollisionShape(p.GEOM_SPHERE, radius=sphereRadius)

for i in range(segmentLength):
  boxId = p.createMultiBody(0,
                            colSphereId,
                            -1, 
                            [segmentStart, 0, -0.1],
                            baseOrientation,
                            linkMasses=link_Masses,
                            linkCollisionShapeIndices=linkCollisionShapeIndices,
                            linkVisualShapeIndices=linkVisualShapeIndices,
                            linkPositions=linkPositions,
                            linkOrientations=linkOrientations,
                            linkInertialFramePositions=linkInertialFramePositions,
                            linkInertialFrameOrientations=linkInertialFrameOrientations,
                            linkParentIndices=indices,
                            linkJointTypes=jointTypes,
                            linkJointAxis=axis)
  p.changeDynamics(boxId, -1, spinningFriction=0.001, rollingFriction=0.001, linearDamping=0.0)
  print(p.getNumJoints(boxId))
  for joint in range(p.getNumJoints(boxId)):
    targetVelocity = 5
    if (i % 2):
      targetVelocity = -5
    p.setJointMotorControl2(boxId,
                            joint,
                            p.VELOCITY_CONTROL,
                            targetVelocity=targetVelocity,
                            force=50)
  segmentStart = segmentStart - 1.1

p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)

###################################################################################################
while (p.isConnected()):
  camData = p.getDebugVisualizerCamera()
  viewMat = camData[2]
  projMat = camData[3]
  p.getCameraImage(256,
                   256,
                   viewMatrix=viewMat,
                   projectionMatrix=projMat,
                   renderer=p.ER_BULLET_HARDWARE_OPENGL)
  keys = p.getKeyboardEvents()
  for k, v in keys.items():

    if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
      m_right = -.2
    if (k == p.B3G_RIGHT_ARROW and (v & p.KEY_WAS_RELEASED)):
      m_right = 0
    if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_TRIGGERED)):
      m_left = .2
    if (k == p.B3G_LEFT_ARROW and (v & p.KEY_WAS_RELEASED)):
      m_left = 0
    if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_TRIGGERED)):
      m_forward= -.2
    if (k == p.B3G_UP_ARROW and (v & p.KEY_WAS_RELEASED)):
      m_forward = 0
    if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_TRIGGERED)):
      m_back = .2
    if (k == p.B3G_DOWN_ARROW and (v & p.KEY_WAS_RELEASED)):
      m_back = 0
  
  playerPos += [m_left + m_right, m_forward+m_back, 1]

  # p.setJointMotorControl2(playerId,
  #                         0,
  #                         p.POSITION_CONTROL,
  #                         targetPosition= playerPos,
  #                         force=30)
  p.stepSimulation()
  #print(keys)
  p.resetDebugVisualizerCamera(5, 90, -30, playerPos)
  time.sleep(0.01)
