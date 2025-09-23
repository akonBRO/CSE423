from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random, time




WIN_W, WIN_H = 1000, 800
ASPECT = WIN_W / float(WIN_H)
FOVY = 70.0




plane_pos = [0.0, 0.0, 120.0]
yaw_deg = 0.0
pitch_deg = 0.0
roll_deg = 0.0
speed = 1.2
prop_angle = 0.0
previous_speed = 1.2




weapons = []
WEAPON_SPEED = 20.0
WEAPON_LIFETIME = 2500




game_state = {
    'adventure_level': 'Obstacle Run',
    'health': 100,
    'score': 0,
    'start_time': None,
    'power_mode': False,
    'ghost_mode': False,
    'game_over': False,
    'current_level': 1,
    'level_timer': 60,
    'rapid_rewards_active': False,
    'rapid_rewards_end_time': 0,
}




cam_follow_dist = 120.0
cam_height = 35.0
cam_side_offset = 0.0
cam_offset_x = 0.0
cam_offset_y = 0.0
cam_offset_z = 0.0




is_first_person = False




N_CLOUDS = 60
CLOUD_AHEAD_RANGE = 4000.0
CLOUD_SIDE_RANGE = 2000.0
CLOUD_MIN_Z, CLOUD_MAX_Z = -200.0, 350.0
clouds = []




N_OBSTACLES = 50
N_COLLECTIBLES = 100
SPAWN_AHEAD_RANGE = 2500.0
SPAWN_SIDE_RANGE = 1500.0
SPAWN_MIN_Z, SPAWN_MAX_Z = -200.0, 200.0
obstacles = []
collectibles = []




SPECIAL_COLLECTIBLE_PROB = 0.1
special_collectible_exists = False
yellow_spawned_count = 0
NORMAL_PLANE_SPEED = 5
MAX_SPEED = 50.0
MIN_SPEED = 0.5
SPEED_INCREMENT = 0.01




rain_drops = []
RAIN_ACTIVE = False
RAIN_START_TIME = time.time() + 10
RAIN_INTERVAL = 30
RAIN_DURATION = 10
N_RAIN = 1000
RAIN_RADIUS = 2000
RAIN_HEIGHT = 4000
RAIN_SPEED = 50
RAIN_LENGTH = 30




is_transitioning = False
transition_start_time = 0.0
transition_duration = 1.0




normal_sky_color = (0.5, 0.7, 1.0)
rainy_sky_color = (0.4, 0.45, 0.5)
current_sky_color = list(normal_sky_color)




special_point = [random.uniform(-15, 15), random.uniform(-15, 15), random.uniform(-15, -5)]
special_angle = 0




_quad = None




mouse_state = {
    GLUT_LEFT_BUTTON: False,
    GLUT_RIGHT_BUTTON: False
}




def reset_game():
    global plane_pos, yaw_deg, pitch_deg, roll_deg, speed, prop_angle, previous_speed
    global weapons, game_state, cam_offset_x, cam_offset_y, cam_offset_z
    global clouds, obstacles, collectibles, special_collectible_exists, yellow_spawned_count
    global rain_drops, RAIN_ACTIVE, RAIN_START_TIME, is_transitioning, current_sky_color, is_first_person
   
    plane_pos = [0.0, 0.0, 120.0]
    yaw_deg = 0.0
    pitch_deg = 0.0
    roll_deg = 0.0
    speed = 1.2
    prop_angle = 0.0
    previous_speed = 1.2
   
    weapons = []
   
    game_state['adventure_level'] = 'Obstacle Run'
    game_state['health'] = 100
    game_state['score'] = 0
    game_state['start_time'] = time.time()
    game_state['power_mode'] = False
    game_state['ghost_mode'] = False
    game_state['game_over'] = False
    game_state['current_level'] = 1
    game_state['level_timer'] = 60
    game_state['rapid_rewards_active'] = False
    game_state['rapid_rewards_end_time'] = 0
   
    cam_offset_x = 0.0
    cam_offset_y = 0.0
    cam_offset_z = 0.0
    is_first_person = False
   
    clouds = []
    obstacles = []
    collectibles = []
    special_collectible_exists = False
    yellow_spawned_count = 0
   
    rain_drops = []
    RAIN_ACTIVE = False
    RAIN_START_TIME = time.time() + 10
    is_transitioning = False
    current_sky_color = list(normal_sky_color)




    init_clouds()
    init_obstacles_and_collectibles()
    print("Game has been restarted.")
    glutPostRedisplay()




def deg2rad(a):
    return a * math.pi / 180.0




def forward_vec():
    yaw = deg2rad(yaw_deg)
    pitch = deg2rad(pitch_deg)
    fx = math.sin(yaw) * math.cos(pitch)
    fy = math.cos(yaw) * math.cos(pitch)
    fz = math.sin(pitch)
    return (fx, fy, fz)
def up_vec(fwd, rgt):
    ux = rgt[1] * fwd[2] - rgt[2] * fwd[1]
    uy = rgt[2] * fwd[0] - rgt[0] * fwd[2]
    uz = rgt[0] * fwd[1] - rgt[1] * fwd[0]
    return (ux, uy, uz)


def right_vec(fwd):
    up = (0.0, 0.0, 1.0)
    rx = fwd[1] * up[2] - fwd[2] * up[1]
    ry = fwd[2] * up[0] - fwd[0] * up[2]
    rz = fwd[0] * up[1] - fwd[1] * up[0]
    l = math.sqrt(rx * rx + ry * ry + rz * rz) or 1.0
    return (rx / l, ry / l, rz / l)




def add(a, b, s=1.0):
    return [a[0] + s * b[0], a[1] + s * b[1], a[2] + s * b[2]]




def draw_sky_gradient():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(current_sky_color[0], current_sky_color[1], current_sky_color[2])
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glColor3f(current_sky_color[0] + 0.3, current_sky_color[1] + 0.2, current_sky_color[2] + 0.1)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)




def draw_cloud():
    glColor3f(0.8039, 0.9411, 1.0)
    glPushMatrix()
    glScalef(1.0, 0.8, 0.8)
    glutSolidSphere(18, 20, 16)
    glTranslatef(12, 5, 2); glutSolidSphere(14, 18, 14)
    glTranslatef(-20, -10, 3); glutSolidSphere(15, 18, 14)
    glTranslatef(10, 10, 10); glutSolidSphere(12, 18, 14)
    glTranslatef(8, -4, -12); glutSolidSphere(10, 16, 12)
    glPopMatrix()




def draw_clouds():
    for c in clouds:
        glPushMatrix()
        glTranslatef(c['pos'][0], c['pos'][1], c['pos'][2])
        glScalef(c['scale'], c['scale'], c['scale'])
        draw_cloud()
        glPopMatrix()




def draw_obstacle():
    glColor3f(0.443, 0.224, 0.118)
    glPushMatrix()
    glScalef(1.0, 1.0, 3.0)
    glutSolidCube(20)
    glPopMatrix()




def draw_target():
    glColor3f(0.8, 0.8, 0.1)
    glutSolidTorus(5, 12, 12, 24)




def draw_collectible(is_special=False):
    if is_special:
        global special_angle
        scale = 1.2 + 0.4 * math.sin(special_angle * math.pi / 180)
       
        glPushMatrix()
        glRotatef(90, 1, 0, 0)  
        glColor3f(1, 0.5, 0)  
        glutWireTorus(0.2, scale + 0.3, 16, 32)
        glPopMatrix()




        special_angle = (special_angle + 2) % 360
    else:
        glColor3f(0.85, 0.85, 0.1)
        glPushMatrix()
        glutSolidSphere(8, 16, 16)
        glPopMatrix()
   
def draw_weapon():
    # Save the current lighting attributes (which includes the shade model)
    glPushAttrib(GL_LIGHTING_BIT)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)


    # Set smooth shading for the weapon's gradient colors
    glShadeModel(GL_SMOOTH)


    slices = 24
    radius = 8.0
    height = 20.0


    # Draw the cone part of the bullet
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.8, 0.7, 0.0) # Tip color
    glVertex3f(0.0, 0.0, height)


    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glColor3f(1.0, 0.5, 0.0) # Base color
        glVertex3f(x, y, 0.0)
    glEnd()


    # Draw the base of the bullet
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.5, 0.0) # Center of base color
    glVertex3f(0.0, 0.0, 0.0)


    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, 0.0)
    glEnd()


    glPopMatrix()
    # Restore the saved attributes, including the original shade model.
    # This prevents this function from affecting how the sky is drawn.
    glPopAttrib()




def draw_pilot():
    glPushMatrix()




    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 5)
    glScalef(1.2, 1.2, 1.4)
    glutSolidSphere(4, 16, 16)
    glPopMatrix()




    glColor3f(0.4, 0.4, 0.4)
    glPushMatrix()
    glTranslatef(0, 0, 6)
    glScalef(1.0, 1.0, 1.0)
    glutSolidSphere(3, 16, 16)
    glPopMatrix()




    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glColor4f(0.5, 0.8, 1.0, 0.5)
    glPushMatrix()
    glTranslatef(0, 0, 5.5)
    glRotatef(90, 1, 0, 0)
    gluPartialDisk(_quad, 0, 3.5, 16, 1, 0, 180)
    glPopMatrix()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)




    glColor3f(0.1, 0.1, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, -3)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(_quad, 5, 3, 8, 16, 1)
    glPopMatrix()
    glColor3f(0.1, 0.1, 0.8)




    for x_offset in [-5.5, 5.5]:
        glPushMatrix()
        glTranslatef(x_offset, 0, -3)
        glRotatef(90, 0, 1, 0)
        glRotatef(15, 1, 0, 0)
        gluCylinder(_quad, 1.5, 1.5, 4, 12, 1)




        glTranslatef(0, 0, 4)
        gluCylinder(_quad, 1.3, 1.3, 3, 12, 1)




        glTranslatef(0, 0, 3)
        glColor3f(1.0, 0.8, 0.6)
        glutSolidSphere(1.5, 8, 8)




        glPopMatrix()




    glPopMatrix()




def draw_plane():
    glPushMatrix()
    glTranslatef(plane_pos[0], plane_pos[1], plane_pos[2])
    glRotatef(yaw_deg, 0, 0, 1)
    glRotatef(pitch_deg, 1, 0, 0)
    glRotatef(roll_deg, 0, 1, 0)




    FUSELAGE_COLOR = (1.0, 0.0, 0.0)
    FUSELAGE_STRIPE = (1.0, 1.0, 1.0)
    WING_COLOR = (0.3, 0.3, 0.3)
    TAIL_COLOR = (1.0, 0.0, 0.0)
    COCKPIT_COLOR = (0.5, 0.3, 0.8, 0.5)
    WHEEL_COLOR = (0.1, 0.1, 0.1)
    STRUT_COLOR = (0.5, 0.5, 0.5)




    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glColor3f(*FUSELAGE_COLOR)
    body_len = 80.0
    body_r = 12.0
    gluCylinder(_quad, body_r, body_r, body_len, 24, 2)
    glColor3f(*FUSELAGE_STRIPE)
    glBegin(GL_QUADS)
    glVertex3f(-body_r, 0, 10); glVertex3f(body_r, 0, 10)
    glVertex3f(body_r, 0, 6); glVertex3f(-body_r, 0, 6)
    glEnd()
    glPushMatrix()
    glTranslatef(0, 0, body_len)
    gluDisk(_quad, 0, body_r, 24, 1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, -5.0)
    gluCylinder(_quad, body_r, body_r*0.6, 5.0, 24, 2)
    glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 25, 0)
    glRotatef(90, 0, 1, 0)
    glBegin(GL_QUADS)
    glColor3f(*WING_COLOR)
    glVertex3f(-25, 0, -2); glVertex3f(-5, 0, -2)
    glVertex3f(-5, -50, 2); glVertex3f(-25, -50, 2)
    glVertex3f(25, 0, -2); glVertex3f(5, 0, -2)
    glVertex3f(5, -50, 2); glVertex3f(25, -50, 2)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -50, 0)
    glBegin(GL_QUADS)
    glColor3f(*TAIL_COLOR)
    glVertex3f(-2, 0, 0); glVertex3f(2, 0, 0)
    glVertex3f(2, 0, 20); glVertex3f(-2, 0, 20)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -45, 10)
    glBegin(GL_QUADS)
    glColor3f(*WING_COLOR)
    glVertex3f(-15, 0, 1); glVertex3f(-15, 0, -1)
    glVertex3f(-5, 0, -1); glVertex3f(-5, 0, 1)
    glVertex3f(15, 0, 1); glVertex3f(15, 0, -1)
    glVertex3f(5, 0, -1); glVertex3f(5, 0, 1)
    glEnd()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 70, -15)
    glColor3f(*STRUT_COLOR)
    glLineWidth(5.0)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0); glVertex3f(0, 0, -15)
    glEnd()
    glColor3f(*WHEEL_COLOR)
    glTranslatef(0, 0, -15)
    glutSolidTorus(2.0, 5.0, 10, 12)
    glPopMatrix()




    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 20, 15, -10)
        glColor3f(*STRUT_COLOR)
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0); glVertex3f(0, 0, -10)
        glEnd()
        glColor3f(*WHEEL_COLOR)
        glTranslatef(0, 0, -10)
        glutSolidTorus(2.0, 5.0, 10, 12)
        glPopMatrix()




    glPushMatrix()
    glTranslatef(0, 30, 10)
    glScalef(0.8, 0.8, 0.8)
    draw_pilot()
    glPopMatrix()




    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glTranslatef(0, 30, 10)
    glColor4f(*COCKPIT_COLOR)
    glutSolidSphere(18, 20, 16)
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glPopMatrix()
    glPopMatrix()




def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(0, 0, 0)):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)




def setupCamera():
    global cam_offset_x, cam_offset_y, cam_offset_z, is_first_person
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, ASPECT, 0.1, 6000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


   
    fwd = forward_vec()
    rgt = right_vec(fwd)
    up = up_vec(fwd, rgt)


    if is_first_person:
       
        cam_pos = add(plane_pos, fwd, 30.0)
        look_at = add(cam_pos, fwd, 100.0)
       
       
        gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                  look_at[0], look_at[1], look_at[2],
                  up[0], up[1], up[2])
    else:
       
        cam = add(plane_pos, fwd, -cam_follow_dist)
        cam = add(cam, up, cam_height)
        cam = add(cam, rgt, cam_side_offset)
        cam[0] += cam_offset_x
        cam[1] += cam_offset_y
        cam[2] += cam_offset_z


        look = add(plane_pos, fwd, 80.0)
       
       
        gluLookAt(cam[0], cam[1], cam[2],
                  look[0], look[1], look[2],
                  up[0], up[1], up[2])




def keyboardListener(key, x, y):
    global cam_offset_x, cam_offset_y, cam_offset_z, game_state, weapons, RAIN_ACTIVE, is_first_person




    key_str = key.decode("utf-8").lower()




    if key_str in ['u', 'U']:
        cam_offset_z += 5.0
    if key_str in ['d', 'D']:


        cam_offset_z -= 5.0
    if key_str in ['l', 'L']:


        cam_offset_x -= 5.0
    if key_str in ['r', 'R']:


        cam_offset_x += 5.0
   
    if key_str in ['s', 'S']:


        if game_state['game_over']:
            reset_game()
            return




    if key_str == 'f':
        is_first_person = not is_first_person
        print("First person perspective ON." if is_first_person else "Third person perspective ON.")




    if key_str == 'p':
        game_state['power_mode'] = not game_state['power_mode']
        print("Power mode ON: Press SPACE to fire weapons." if game_state['power_mode'] else "Power mode OFF.")




    if key_str == 'g':
        if RAIN_ACTIVE:
            game_state['ghost_mode'] = not game_state['ghost_mode']
            print("Ghost mode ON: Plane is invulnerable to rain." if game_state['ghost_mode'] else "Ghost mode OFF.")
        else:
            print("Ghost Mode can only be activated during rain.")




    if key_str == ' ':
      if game_state['power_mode'] and not game_state['game_over']:
        weapon_pos = list(plane_pos)
        fwd = forward_vec()
        weapon_pos = add(weapon_pos, fwd, 80.0)
        weapons.append({
            'pos': weapon_pos,
            'dir': fwd,
            'spawn_time': time.time() * 1000
        })
        game_state['health'] -= 5.0 / 100
   
    if plane_pos[2] < -300:
        plane_pos[2] = -300




    if key_str == '\x1b':
        glutLeaveMainLoop()




    glutPostRedisplay()




def specialKeyListener(key, x, y):
    global pitch_deg, plane_pos




    if key == GLUT_KEY_UP:
        pitch_deg = min(35.0, pitch_deg + 1.8)
    if key == GLUT_KEY_DOWN:
        pitch_deg = max(-35.0, pitch_deg - 1.8)
    if key == GLUT_KEY_LEFT:
        plane_pos[0] -= 15.0
    if key == GLUT_KEY_RIGHT:
        plane_pos[0] += 15.0




    glutPostRedisplay()




def mouseListener(button, state, x, y):
    global mouse_state
    if button == GLUT_LEFT_BUTTON or button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            mouse_state[button] = True
        elif state == GLUT_UP:
            mouse_state[button] = False




    glutPostRedisplay()




def check_collisions():
    global weapons, obstacles, collectibles




    if game_state['game_over']:
        return




    plane_radius = 40.0
    current_time = time.time() * 1000




    if game_state['power_mode']:
        hit_weapons = []
        hit_obstacles = []
        for i, weapon in enumerate(weapons):
            weapon_pos = weapon['pos']
            for j, obs in enumerate(obstacles):
                obs_pos = obs['pos']
                dist_sq = sum((weapon_pos[k] - obs_pos[k]) ** 2 for k in range(3))
                obs_radius = obs['scale'] * 15.0
                if dist_sq < (10.0 + obs_radius) ** 2:
                    hit_weapons.append(i)
                    hit_obstacles.append(j)
                    game_state['score'] += 20
       
        for i in sorted(set(hit_weapons), reverse=True):
            del weapons[i]
        for j in sorted(set(hit_obstacles), reverse=True):
            del obstacles[j]




    if not game_state['rapid_rewards_active']:
        collided_obstacles = []
        for i, obs in enumerate(obstacles):
            obs_pos = obs['pos']
            obs_radius = obs['scale'] * 15.0
            dist_sq = sum((plane_pos[k] - obs_pos[k]) ** 2 for k in range(3))
           
            if dist_sq < (plane_radius + obs_radius) ** 2:
                if not game_state['ghost_mode']:
                    game_state['health'] -= 5 if game_state['power_mode'] else 10
                collided_obstacles.append(i)
       
        for i in sorted(collided_obstacles, reverse=True):
            del obstacles[i]




    collided_collectibles = []
    for i, col in enumerate(collectibles):
        col_pos = col['pos']
       
        if col['type'] == 'special':
            col_radius = col['scale']
            dist_sq = sum((plane_pos[k] - col_pos[k]) ** 2 for k in range(3))
           
            if dist_sq < (plane_radius + col_radius) ** 2:
                global previous_speed
                previous_speed = speed
                game_state['adventure_level'] = 'Rapid Rewards'
                game_state['rapid_rewards_active'] = True
                game_state['rapid_rewards_end_time'] = time.time() + 5
                global special_collectible_exists
                special_collectible_exists = False
                print("RAPID REWARDS ACTIVATED!")
                collided_collectibles.append(i)
        else:
            col_radius = col['scale'] * 8.0
            dist_sq = sum((plane_pos[k] - col_pos[k]) ** 2 for k in range(3))
            if dist_sq < (plane_radius + col_radius) ** 2:
                game_state['score'] += 10
                collided_collectibles.append(i)




    for i in sorted(collided_collectibles, reverse=True):
        del collectibles[i]




    weapons = [w for w in weapons if current_time - w['spawn_time'] < WEAPON_LIFETIME]




def manage_game_entities():
    global clouds, obstacles, collectibles, weapons, yellow_spawned_count, speed


    if game_state['rapid_rewards_active']:
        speed = 50
    else:
        speed = max(MIN_SPEED, min(MAX_SPEED, speed))


   
    clouds_to_keep = [c for c in clouds if c['pos'][1] > plane_pos[1] - 500]
    clouds = clouds_to_keep
   
    while len(clouds) < N_CLOUDS:
       
        x = plane_pos[0] + random.uniform(-CLOUD_SIDE_RANGE, CLOUD_SIDE_RANGE)
        y = plane_pos[1] + CLOUD_AHEAD_RANGE
       
        z = plane_pos[2] + random.uniform(CLOUD_MIN_Z, CLOUD_MAX_Z)
        s = random.uniform(0.5, 2.5)
        clouds.append({'pos': [x, y, z], 'scale': s})


    obstacles = [o for o in obstacles if o['pos'][1] > plane_pos[1] - 50]
    collectibles = [c for c in collectibles if c['pos'][1] > plane_pos[1] - 50]


    num_collectibles_to_spawn = N_COLLECTIBLES
    if game_state['rapid_rewards_active']:
        num_collectibles_to_spawn = N_COLLECTIBLES + 1000
        obstacles = []
   
   
    while len(collectibles) < num_collectibles_to_spawn:
       
        x = plane_pos[0] + random.uniform(-SPAWN_SIDE_RANGE, SPAWN_SIDE_RANGE)
        y = plane_pos[1] + random.uniform(100, SPAWN_AHEAD_RANGE)
       
        z = plane_pos[2] + random.uniform(SPAWN_MIN_Z, SPAWN_MAX_Z)
        s = random.uniform(0.5, 1.5)


        if not game_state['rapid_rewards_active'] and random.random() < 0.005:  
            collectibles.append({'pos': [x, y, z], 'scale': s * 30, 'type': 'special'})
            yellow_spawned_count = 0
            print("A special collectible has appeared!")
        else:
            collectibles.append({'pos': [x, y, z], 'scale': s, 'type': 'normal'})
            if not game_state['rapid_rewards_active']:
                yellow_spawned_count += 1
   
   
    if not game_state['rapid_rewards_active']:
        while len(obstacles) < N_OBSTACLES:
           
            x = plane_pos[0] + random.uniform(-SPAWN_SIDE_RANGE, SPAWN_SIDE_RANGE)
            y = plane_pos[1] + random.uniform(100, SPAWN_AHEAD_RANGE)
           
            z = plane_pos[2] + random.uniform(SPAWN_MIN_Z, SPAWN_MAX_Z)
            s = random.uniform(0.5, 2.0)
            obstacles.append({'pos': [x, y, z], 'scale': s})


    current_time = time.time() * 1000
    weapons = [w for w in weapons if current_time - w['spawn_time'] < WEAPON_LIFETIME]




def update_game_state():
    global plane_pos, prop_angle, speed, weapons
    global RAIN_ACTIVE, rain_drops, is_transitioning, transition_start_time, current_sky_color, RAIN_START_TIME, collectibles
    global mouse_state, previous_speed




    if game_state['game_over']:
        return
    if mouse_state[GLUT_LEFT_BUTTON]:
        speed += SPEED_INCREMENT
    if mouse_state[GLUT_RIGHT_BUTTON]:
        speed -= SPEED_INCREMENT




    was_rapid_rewards_active = game_state['rapid_rewards_active']




    if game_state['rapid_rewards_active'] and time.time() > game_state['rapid_rewards_end_time']:
        game_state['adventure_level'] = 'Obstacle Run'
        game_state['rapid_rewards_active'] = False
        speed = previous_speed
        print("RAPID REWARDS EXPIRED. Returning to Obstacle Run.")




    is_rapid_rewards_active_now = game_state['rapid_rewards_active']




    if was_rapid_rewards_active and not is_rapid_rewards_active_now:
        collectibles = []




    if RAIN_ACTIVE and not game_state['ghost_mode']:
        game_state['health'] -= 0.02




    if game_state['health'] <= 0:
        game_state['game_over'] = True
        print("Game Over! You crashed.")
        print(f"Final Score: {game_state['score']}")




    if game_state['adventure_level'] == 'Time Trial':
        time_elapsed = time.time() - game_state['start_time']
        if time_elapsed > game_state['level_timer']:
            game_state['game_over'] = True
            print("Game Over! Time's up.")
            print(f"Final Score: {game_state['score']}")




    fwd = forward_vec()
    plane_pos = add(plane_pos, fwd, speed)




    for weapon in weapons:
        weapon['pos'] = add(weapon['pos'], weapon['dir'], WEAPON_SPEED)




    check_collisions()
    manage_game_entities()
    prop_angle = (prop_angle + 30) % 360
    now = time.time()
    new_rain_active = (now - RAIN_START_TIME) % (RAIN_INTERVAL + RAIN_DURATION) < RAIN_DURATION




    if new_rain_active != RAIN_ACTIVE:
        is_transitioning = True
        transition_start_time = now
        RAIN_ACTIVE = new_rain_active




    if is_transitioning:
        t = (now - transition_start_time) / transition_duration
        t = min(t, 1.0)




        start_color = rainy_sky_color if not RAIN_ACTIVE else normal_sky_color
        end_color = normal_sky_color if not RAIN_ACTIVE else rainy_sky_color




        current_sky_color = [
            start_color[i] * (1 - t) + end_color[i] * t for i in range(3)
        ]




        if t >= 1.0:
            is_transitioning = False
            if not RAIN_ACTIVE:
                game_state['ghost_mode'] = False
                print("Ghost Mode automatically disabled as the rain has stopped.")




    if RAIN_ACTIVE and not rain_drops:
        rain_drops = []
        for _ in range(N_RAIN):
            angle = random.uniform(0, 2 * math.pi)
            x = plane_pos[0] + RAIN_RADIUS * math.cos(angle)
            y = plane_pos[1] + RAIN_RADIUS * math.sin(angle)
            z = random.uniform(plane_pos[2] + RAIN_HEIGHT / 2, plane_pos[2] - RAIN_HEIGHT / 2)
            rain_drops.append([x, y, z])




    if RAIN_ACTIVE:
        for drop in rain_drops:
            drop[2] -= RAIN_SPEED
            if drop[2] < plane_pos[2] - RAIN_HEIGHT / 2:
                angle = random.uniform(0, 2 * math.pi)
                drop[0] = plane_pos[0] + RAIN_RADIUS * math.cos(angle)
                drop[1] = plane_pos[1] + RAIN_RADIUS * math.sin(angle)
                drop[2] = plane_pos[2] + RAIN_HEIGHT / 2




def idle_func():
    update_game_state()
    glutPostRedisplay()




def display():
    global current_sky_color, is_transitioning, RAIN_ACTIVE
   
    glClearColor(current_sky_color[0], current_sky_color[1], current_sky_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCamera()
    draw_sky_gradient()




    if RAIN_ACTIVE or is_transitioning:
        glPushMatrix()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        glColor4f(0.7, 0.8, 1.0, 0.6)
        glLineWidth(2.0)
       
        glBegin(GL_LINES)
        for drop in rain_drops:
            glVertex3f(drop[0], drop[1], drop[2])
            glVertex3f(drop[0], drop[1], drop[2] - 100)
        glEnd()
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)
        glPopMatrix()




    for weapon in weapons:
        glPushMatrix()
        glTranslatef(*weapon['pos'])
        draw_weapon()
        glPopMatrix()




    for obs in obstacles:
        glPushMatrix()
        glTranslatef(*obs['pos'])
        glScalef(obs['scale'], obs['scale'], obs['scale'])
        draw_obstacle()
        glPopMatrix()




    for col in collectibles:
        glPushMatrix()
        glTranslatef(*col['pos'])
        glScalef(col['scale'], col['scale'], col['scale'])
        draw_collectible(is_special=(col['type'] == 'special'))
        glPopMatrix()




    if not (RAIN_ACTIVE or is_transitioning):
      draw_clouds()
   
    if not is_first_person:
        draw_plane()




    glColor3f(0.0, 0.0, 0.0)
    draw_text(10, 780, f"Adventure Level: {game_state['adventure_level']}")
    draw_text(10, 750, f"Speed: {speed:.1f}")
    draw_text(10, 720, f"Health: {game_state['health']:.1f} HP",
                    color=(1, 0, 0) if game_state['health'] < 30 else (0, 0, 0))
    draw_text(10, 690, f"Score: {game_state['score']}")




    if game_state['adventure_level'] == 'Time Trial':
        time_elapsed = time.time() - game_state['start_time']
        if time_elapsed > game_state['level_timer']:
            game_state['game_over'] = True
            print("Game Over! Time's up.")
            print(f"Final Score: {game_state['score']}")




    if game_state['power_mode']:
        draw_text(10, 630, "POWER MODE ON",
            font=GLUT_BITMAP_TIMES_ROMAN_24, color=(1, 0, 0))

    if game_state['ghost_mode']:
        draw_text(10, 600, "GHOST MODE ON",
            font=GLUT_BITMAP_TIMES_ROMAN_24, color=(0, 1, 0))




    if game_state['rapid_rewards_active']:
        time_left = max(0, game_state['rapid_rewards_end_time'] - time.time())
        draw_text(WIN_W/2 - 120, WIN_H/2, f"RAPID REWARDS: {time_left:.1f}s", font=GLUT_BITMAP_TIMES_ROMAN_24, color=(0, 0.8, 0.0))




    if is_first_person:
        draw_text(10, 660, "FIRST PERSON MODE", color=(0.5, 0.5, 0.5))
    else:
        draw_text(10, 660, "THIRD PERSON MODE", color=(0.5, 0.5, 0.5))




    if game_state['game_over']:
        draw_text(WIN_W / 2 - 100, WIN_H / 2, "GAME OVER",
                    font=GLUT_BITMAP_TIMES_ROMAN_24, color=(0, 0, 0))
        draw_text(WIN_W / 2 - 100, WIN_H / 2 - 50, f"FINAL SCORE: {game_state['score']}",
                    font=GLUT_BITMAP_TIMES_ROMAN_24, color=(0, 0, 0))
        draw_text(WIN_W / 2 - 200, WIN_H / 2 - 100, "Press 'S' or 's' to restart the game",
                    font=GLUT_BITMAP_TIMES_ROMAN_24, color=(0, 0, 0))




    glutSwapBuffers()




def init_clouds():
    global clouds
    clouds = []
    for _ in range(N_CLOUDS):
        x = random.uniform(-CLOUD_SIDE_RANGE, CLOUD_SIDE_RANGE)
        y = random.uniform(0, CLOUD_AHEAD_RANGE)
        z = random.uniform(CLOUD_MIN_Z, CLOUD_MAX_Z)
        s = random.uniform(0.5, 2.5)
        clouds.append({'pos': [x, y, z], 'scale': s})




def init_obstacles_and_collectibles():
    global obstacles, collectibles, special_collectible_exists
    special_collectible_exists = False
    obstacles = []
    collectibles = []
    for _ in range(N_OBSTACLES):
        x = random.uniform(-SPAWN_SIDE_RANGE, SPAWN_SIDE_RANGE)
        y = random.uniform(0, SPAWN_AHEAD_RANGE)
        z = random.uniform(SPAWN_MIN_Z, SPAWN_MAX_Z)
        s = random.uniform(0.5, 2.0)
        obstacles.append({'pos': [x, y, z], 'scale': s})
    for _ in range(N_COLLECTIBLES):
        x = random.uniform(-SPAWN_SIDE_RANGE, SPAWN_SIDE_RANGE)
        y = random.uniform(0, SPAWN_AHEAD_RANGE)
        z = random.uniform(SPAWN_MIN_Z, SPAWN_MAX_Z)
        s = random.uniform(0.5, 1.5)
        is_special = random.random() < SPECIAL_COLLECTIBLE_PROB and not special_collectible_exists
        if is_special:
            special_collectible_exists = True
        collectibles.append({'pos': [x, y, z], 'scale': s, 'type': 'special' if is_special else 'normal'})




def main():
    global _quad, game_state




    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Sky Adventure")




    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.5, 0.7, 1.0, 1.0)




    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)




    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)




    glShadeModel(GL_SMOOTH)




    _quad = gluNewQuadric()




    init_clouds()
    init_obstacles_and_collectibles()
    game_state['start_time'] = time.time()




    glutDisplayFunc(display)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle_func)
    glutMainLoop()




if __name__ == "__main__":
    main()


