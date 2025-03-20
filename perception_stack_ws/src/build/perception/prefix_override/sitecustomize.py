import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/hunter/Robot_Perception_System/perception_stack_ws/src/install/perception'
