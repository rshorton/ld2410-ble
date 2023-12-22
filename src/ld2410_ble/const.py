CHARACTERISTIC_NOTIFY = "0000fff1-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_WRITE = "0000fff2-0000-1000-8000-00805f9b34fb"

CMD_COMMON_POST = b"\x04\x03\x02\x01"
CMD_BT_PASS_PRE = b"\xfd\xfc\xfb\xfa\x08\x00\xa8\x00"
CMD_BT_PASS_DEFAULT = b"HiLink"
CMD_BT_PASS_POST = CMD_COMMON_POST
CMD_ENABLE_CONFIG = b"\xfd\xfc\xfb\xfa\x04\x00\xff\x00\x01\x00\x04\x03\x02\x01"
CMD_ENABLE_ENGINEERING_MODE = b"\xfd\xfc\xfb\xfa\x02\x00b\x00\x04\x03\x02\x01"
CMD_DISABLE_CONFIG = b"\xfd\xfc\xfb\xfa\x02\x00\xfe\x00\x04\x03\x02\x01"
CMD_READ_CONFIG = b"\xfd\xfc\xfb\xfa\x02\x00\x61\x00\x04\x03\x02\x01"
CMD_SET_RANGE_SENSITIVITY_PRE = b"\xfd\xfc\xfb\xfa\x14\x00\x64\x00"
CMD_SET_RANGE_SENSITIVITY_POST = CMD_COMMON_POST
CMD_SET_MAX_GATE_AND_UNMANNED_TIMEOUT_PRE = b"\xfd\xfc\xfb\xfa\x14\x00\x60\x00"
CMD_SET_MAX_GATE_AND_UNMANNED_TIMEOUT_POST = CMD_COMMON_POST


PARAM_GATE = b"\x00\x00"
PARAM_MOTION_SENSITIVITY = b"\x01\x00"
PARAM_STATIC_SENSITIVITY = b"\x02\x00"

PARAM_MAX_MOVING_DIST_GATE = b"\x00\x00"
PARAM_MAX_STATIC_DIST_GATE = b"\x01\x00"
PARAM_UNMANNED_TIMEOUT = b"\x02\x00"

MOVING_TARGET = 1
STATIC_TARGET = 2

frame_start = b"\xf4\xf3\xf2\xf1"
frame_length = b"(?P<length>..)"
frame_engineering_mode = b"(?P<engineering>\x01|\x02)"
frame_head = b"\xaa"
frame_target_state = b"(?P<target_state>\x00|\x01|\x02|\x03)"
frame_moving_target_distance = b"(?P<moving_target_distance>..)"
frame_moving_target_energy = b"(?P<moving_target_energy>.)"
frame_static_target_distance = b"(?P<static_target_distance>..)"
frame_static_target_energy = b"(?P<static_target_energy>.)"
frame_detection_distance = b"(?P<detection_distance>..)"
frame_engineering_data = b"(?P<engineering_data>.+?)?"
frame_tail = b"\x55"
frame_check = b"\x00"
frame_end = b"\xf8\xf7\xf6\xf5"

frame_parameter_read_start = b"\xfd\xfc\xfb\xfa"
frame_parameter_read_ack = b"\x61\x01\x00\x00\xaa"
frame_parameter_read_end = b"\x04\x03\x02\x01"

frame_maximum_distance_gates = b"(?P<maximum_distance_gates>.)"
frame_maximum_motion_gates = b"(?P<maximum_motion_gates>.)"
frame_maximum_static_gates = b"(?P<maximum_static_gates>.)"
frame_motion_energy_gates = b"(?P<motion_energy_gates>.{9})"
frame_static_energy_gates = b"(?P<static_energy_gates>.{9})"
frame_additional_information = b"(?P<additional_information>.*)"
frame_unmanned_timeout = b"(?P<unmanned_timeout>..)"

frame_regex = (
    frame_start
    + frame_length
    + frame_engineering_mode
    + frame_head
    + frame_target_state
    + frame_moving_target_distance
    + frame_moving_target_energy
    + frame_static_target_distance
    + frame_static_target_energy
    + frame_detection_distance
    + frame_engineering_data
    + frame_tail
    + frame_check
    + frame_end
)

engineering_frame_regex = (
    frame_maximum_motion_gates
    + frame_maximum_static_gates
    + frame_motion_energy_gates
    + frame_static_energy_gates
    + frame_additional_information
)

read_param_frame_regex = (
    frame_parameter_read_start
    + frame_length
    + frame_parameter_read_ack
    + frame_maximum_distance_gates
    + frame_maximum_motion_gates
    + frame_maximum_static_gates
    + frame_motion_energy_gates
    + frame_static_energy_gates
    + frame_unmanned_timeout
    + frame_parameter_read_end
)

