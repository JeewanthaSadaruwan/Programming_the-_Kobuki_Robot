import movement
from kobukidriversample import Kobuki
import rotating
import navigation




color_sequence = ['red', 'blue', 'green', 'yellow']

kobuki = Kobuki()


# x=colordetectionwhilerotatng.find_color_boxes_between_lines(kobuki,color_sequence,100)


navigation.robot_navigation(
    kobuki=kobuki,
    color="white",
    y_center=300,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

rotating.find_color_box(kobuki,"red",100,0.9)



navigation.robot_navigation(
    kobuki=kobuki,
    color="red",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max

)

rotating.find_color_box(kobuki,"red",100,0.7)


navigation.robot_navigation(
    kobuki=kobuki,
    color="red",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

movement.move_backward(kobuki,100)

rotating.find_color_box(kobuki,"white",100,0.9)

navigation.robot_navigation(
    kobuki=kobuki,
    color="green",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

rotating.find_color_box(kobuki,"green",100,0.7)

navigation.robot_navigation(
    kobuki=kobuki,
    color="green",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

movement.move_backward(kobuki,100)

rotating.find_color_box(kobuki,"white",100,0.9)
navigation.robot_navigation(
    kobuki=kobuki,
    color="yellow",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)           

rotating.find_color_box(kobuki,"yellow",100,0.7)

navigation.robot_navigation(
    kobuki=kobuki,
    color="yellow",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)
movement.move_backward(kobuki,100)

rotating.find_color_box(kobuki,"white",100,0.9)

navigation.robot_navigation(
    kobuki=kobuki,
    color="blue",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

rotating.find_color_box(kobuki,"blue",100,0.7)

navigation.robot_navigation(
    kobuki=kobuki,
    color="blue",
    y_center=400,
    gap=50,
    forward_speed=100,
    timeout=60  # Will terminate after 60 seconds max
)

movement.move_backward(kobuki,100)


