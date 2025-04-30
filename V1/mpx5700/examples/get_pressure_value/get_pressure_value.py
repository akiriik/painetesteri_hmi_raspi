import sys
import os
import time

# Lisää polku josta moduuli löytyy
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Importtaa moduuli
from DFROBOT_MPX5700 import DFRobot_MPX5700_I2C

# Luo oikea instanssi
mpx5700 = DFRobot_MPX5700_I2C(1, 0x16)

def setup():
  mpx5700.set_mean_sample_size(5)
  
def loop():
  press = mpx5700.get_pressure_value_kpa(1)
  print ("Pressure : " + str(press) + " kPA")
  time.sleep(1)  
  
if __name__ == "__main__":
  setup()
  while True:
    loop()