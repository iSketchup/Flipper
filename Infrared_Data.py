import time
import flipperzero


def get_data():

    if flipperzero.infrared_is_busy() == False:
        data = flipperzero.infrared_receive()
        print(data)


        return  data

    else:
        print("Infrared is Busy")



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

transmit = True
data = get_data()



