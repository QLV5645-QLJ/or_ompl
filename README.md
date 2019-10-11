in the ompl_ws set up ompl:  
```bash  
mkdir ompl_ws
wget https://bitbucket.org/ompl/ompl/downloads/ompl-1.4.2-Source.zip
unzip ompl-1.4.2-Source.zip
mv ompl-1.4.2-Source ompl
cd ompl
mkdir -p build/Release
cd build/Release
cmake ../..
make -j 4 # replace 4 by the cores of the cpu
cd ../..
mkdir ../include
mkdir ../lib
cp -r src/* ../include/
cp build/Release/lib/* ../lib/
```  

in the openrave_ws set up openRave and follow the README :  
```bash
mkdir openrave_ws
git clone https://github.com/QLV5645-QLJ/openrave-installation.git
```

in the or_ompl_ws set up or_ompl:
```bash 
mkdir -p or_ompl_ws/src
cd or_ompl_ws/src
git clone https://github.com/QLV5645-QLJ/or_ompl.git
catkin_make #set ompl_DIR and openRave in the cmakeList before this
copy two built libraries to /usr/local/lib/openrave0.9-plugins/  
python src/tests/test_planners.py # for testing
``` 

[README by personalRobotics](README_origin.md)  