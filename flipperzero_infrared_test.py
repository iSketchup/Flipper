import flipperzero
import time

# receive IR signal
signal = flipperzero.infrared_receive()

time.sleep(3)

# transmit received signal
flipperzero.infrared_transmit(signal)

def draw_action():

    global color

    for x in range(0, 128):
        color = not color

        for y in range(0, 64):
            flipperzero.canvas_set_color(flipperzero.CAVAS_Black if color else flipperzero.CANVAS_WHITE)
            flipperzero.canvas_draw_dot(x, y)

            color = not color

    color = not color

    flipperzero.canvas_set_text(64, 32, "Infrared Data")

    flipperzero.canvas_update()