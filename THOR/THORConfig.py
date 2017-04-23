# thor environment setting

# size of the display
screen_width=300
screen_height=300

# size of the input image to the network
net_input_width=224
net_input_height=224

darwin_build='thor_binary/thor-cmu-201703101557-OSXIntel64.app/Contents/MacOS/thor-cmu-201703101557-OSXIntel64'
linux_build='thor_binary/thor-cmu-201703101558-Linux64'
x_display="0.0"

# supported environments and actions
supported_envs = ['FloorPlan224', 'FloorPlan225']
supported_actions = ['MoveAhead', 'MoveBack', 'RotateLeft', 'RotateRight']
# supported_actions = ['MoveAhead', 'MoveBack', 'MoveRight', 'MoveLeft', 'RotateLeft', 'RotateRight', 'LookUp', 'LookDown']

# THORTargetImgProvider configurations
target_image_diff_threshold=10

# random actions being taken when new episode is started
random_start = 30  # TODO: check the value used in paper

# maximum number of steps before the episode terminates
episode_max_steps = 10000

