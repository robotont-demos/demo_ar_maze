# ar_maze
**Package ar_maze aimed to provide robot navigation through the maze with ar tags. In the beginning robot is given by a list of ar tags. Reaching them one by one, robot successfully completes the maze.**

**Package consists of**:
- `main_project` node
- `nav_if_walls` node
- `ar_maze.launch` launch file</br>
However, for package functioning there are two default packages required: `ar_track_alvar` and `robotont_laserscan_to_distance`.

### Nodes
The main logic in algorithm that is enclosed in nodes `main_project` and `nav_if_walls` is looking for and approaching the ar tags one by one to complete the maze. In case of not finding the tag, robot starts rotation and motion avoiding obstacles in order to find the (next) ar tag. </br>
`main_project` node subscribes to the topic "/ar_pose_marker" and starts receiving information about ar tags. When it receives the tag with right id, it publishes robot's velocity under the topic "/cmd_vel" to approach this tag. If there is no ar tag present or it is present, but with wrong index, robot starts rotation. When completed one full rotation and still did not find the tag, `nav_if_walls` node takes action. Communication between nodes proceeds via ROS parameter "ar_present" that is set up in `main_project` node. `nav_if_walls` node subscribes to the "/scan_to_distance" topic. Once it receives that not "ar_present", it publishes messages under the topic "cmd_vel" in such a way: robot does one full rotation and then moving forward a bit. If there is an obstacle robot rotates while not avoid it and continue motion. This appears constantly while not receiving parameter "ar_present"  as True from the `main_project` node. Algorithm in action is shown here: https://youtu.be/iQvUA5Hv8zk </br>
These nodes can be used also separately. `nav_if_walls.py` node can be used for simple motion with obstacle avoidance. `main_project.py` can be used for simple finding and approaching ar tags as shown here: https://youtu.be/dXcZbo1J8K8</br>

### Launch file 
Launch file `ar_maze.launch` includes:
- list of ar tags' ids setted up as parameter
- `individualMarkersNoKinect` node from the `ar_track_alvar` package with appropriate parameters
- `distance_from_depth_image` launch file from the `robotont_laserscan_to_distance` package
- `main_project` node with ar tags list parameter 
- `nav_if_walls` node</br>

### How to run the algorithm on Robotont robot
1.Build the package and source the catkin workspace:</br>
    
    catkin build
    source devel/setup.bash
2.Modify the list of ar tags for maze navigation in 8th line of `ar_maze.launch` (/launch/ar_maze.launch)</br>

3.Launch the `ar_maze.launch` file:

    roslaunch ar_maze ar_maze.launch
