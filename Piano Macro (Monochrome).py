import time
import keyboard
import win32api, win32con
import mss
import subprocess
subprocess.run("cls", shell=True)
#basic_offset_y = int(input("Enter Base Offset: "))
basic_offset_y = 40
print(basic_offset_y)
print('Running')

def click(x, y, offset_y=0):
    win32api.SetCursorPos((x, y + int(offset_y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#x1, x2, x3, x4 = 141, 150, 429, 435
x1, x2, x3, x4 = 143, 151, 434, 443
tile_positions = [x1, x2, x3, x4]

left, top = x1, 210
width, height = x4 - x1 + 1, 30

paused = False


pixel_indices = []
for x in tile_positions:
    x_rel = x - left
    y_rel = 220 - top
    index = (y_rel * width + x_rel) * 3 + 1
    pixel_indices.append(index)

def toggle_pause():
    global paused
    paused = not paused
    print("Paused" if paused else "Running")

keyboard.add_hotkey('p', toggle_pause)

def increase_basic_offset():
    global basic_offset_y
    basic_offset_y += 10
    print(f"basic offset increased to {basic_offset_y}")

def decrease_basic_offset():
    global basic_offset_y
    basic_offset_y -= 10
    print(f"basic offset decreased to {basic_offset_y}")

keyboard.add_hotkey('up', increase_basic_offset)
keyboard.add_hotkey('down', decrease_basic_offset)

with mss.mss() as sct:
    monitor = {"top": top, "left": left, "width": width, "height": height}
    while not keyboard.is_pressed('q'):
        if paused:
            time.sleep(0.01)
            continue

        img = sct.grab(monitor)
        pixel_data = img.rgb

        for idx, green_index in enumerate(pixel_indices):
            if 40 <= pixel_data[green_index] < 55:
                click(tile_positions[idx], 220, offset_y=basic_offset_y)
        time.sleep(0.001)
