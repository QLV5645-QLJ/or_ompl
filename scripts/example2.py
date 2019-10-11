#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009-2011 Rosen Diankov (rosen.diankov@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shows how to use the grasping.GraspingModel to compute valid grasps for manipulation.

.. examplepre-block:: simplegrasping

Description
-----------

This type of example is suited for object geometries that are dynamically created from sensor data.

.. examplepost-block:: simplegrasping
"""

from __future__ import with_statement # for python 2.5
__author__ = 'Rosen Diankov'

from itertools import izip
import openravepy
if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

def main(env,options):
    "Main example code."
    # env.Load(options.scene)
    # robot = env.GetRobots()[0]
    # if options.manipname is not None:
        # robot.SetActiveManipulator(options.manipname)

    start_config = [  0.80487864,  0.42326865, -0.54016693,  2.28895761,
                     -0.34930645, -1.19702164,  1.95971213 ]
    goal_config  = [  2.41349473, -1.43062044, -2.69016693,  2.12681216,
                     -0.75643783, -1.52392537,  1.01239878 ]

    # Setup the environment.
    env = Environment()
    env.SetViewer('qtcoin')
    env.Load('data/wamtest1.env.xml')
    robot = env.GetRobot('BarrettWAM')
    manipulator = robot.GetManipulator('arm')

    planner = RaveCreatePlanner(env, 'OMPL_RRTConnect')
    simplifier = RaveCreatePlanner(env, 'OMPL_Simplifier')

    with env:
        robot.SetActiveDOFs(manipulator.GetArmIndices())
        robot.SetActiveDOFValues(start_config)
        robot.SetActiveManipulator(manipulator)

    # Setup the planning instance.
    params = Planner.PlannerParameters()
    params.SetRobotActiveJoints(robot)
    params.SetGoalConfig(goal_config)

    # Set the timeout and planner-specific parameters. You can view a list of
    # supported parameters by calling: planner.SendCommand('GetParameters')
    if (planner is None):
        print "planner is none"
    else:
        print "planner is not None"
    print 'Parameters:'
    # print planner.SendCommand('GetParameters')

    params.SetExtraParameters('<range>0.02</range>')
    print params

    with env:
        with robot:
            # Invoke the planner.
            print 'Calling the OMPL_RRTConnect planner.'
            traj = RaveCreateTrajectory(env, '')
            planner.InitPlan(robot, params)
            result = planner.PlanPath(traj)
            print ("result:",result)
            print ( PlannerStatus.HasSolution)
            assert result == PlannerStatus.HasSolution

            # Shortcut the path.
            print 'Calling the OMPL_Simplifier for shortcutting.'
            simplifier.InitPlan(robot, Planner.PlannerParameters())
            result = simplifier.PlanPath(traj)
            assert result == PlannerStatus.HasSolution

            # Time the trajectory.
            print 'Timing trajectory'
            result = planningutils.RetimeTrajectory(traj)
            assert result == PlannerStatus.HasSolution

    # Execute the trajectory.
    raw_input('Press <ENTER> to execute trajectory.')
    robot.GetController().SetPath(traj)
    robot.WaitForController(0)


from optparse import OptionParser
from openravepy.misc import OpenRAVEGlobalArguments

@openravepy.with_destroy
def run(args=None):
    """Command-line execution of the example.

    :param args: arguments for script to parse, if not specified will use sys.argv
    """
    parser = OptionParser(description='Shows how to use the grasping.GraspingModel to compute valid grasps for manipulation.')
    OpenRAVEGlobalArguments.addOptions(parser)
    parser.add_option('--scene', action="store",type='string',dest='scene',default='data/wamtest1.env.xml',
                      help='Scene file to load (default=%default)')
    parser.add_option('--manipname', action="store",type='string',dest='manipname',default=None,
                      help='Choose the manipulator to perform the grasping for')
    (options, leftargs) = parser.parse_args(args=args)
    OpenRAVEGlobalArguments.parseAndCreateThreadedUser(options,main,defaultviewer=True)

if __name__ == "__main__":
    run()
