# BURL Tnw

   it is module inside of lab robotics for create application
created by tanawat thuamthet

## Install
```
pip install burltnw
```

## Import
```
import burltnw
```

## Method of use

### status
```
robot = burltnw.apollo()
print(robot.get_status())
```

### battery
```
robot = burltnw.apollo()
print(robot.get_battery())
```

### move
```
robot = burltnw.apollo()
print(robot.walk(1,1)) # position x and position y
```

### rotate
```
robot = burltnw.apollo()
print(robot.rotate(1)) # degree
```

### home
```
robot = burltnw.apollo()
print(robot.home())
```