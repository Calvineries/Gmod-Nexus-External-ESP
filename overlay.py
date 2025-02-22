from helper import ScreenSize, Vector3, get_random_string
from win32gui import *
from win32con import *
import OpenGL.GLUT as glut
import OpenGL.GL as gl
import glfw, ctypes

class Overlay():
    def __init__(self) -> None:
        self.overlay_state = False
        self.random_string = get_random_string()
        if not glfw.init() or not glut.glutInit():
            return

        glfw.window_hint(glfw.FLOATING, True)
        glfw.window_hint(glfw.DECORATED, False)
        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
        glfw.window_hint(glfw.SAMPLES, 2)

        self.window = glfw.create_window(1920-1, 1080-1, title:=f'{self.random_string}', None, None)
        if not self.window:
            return
        self.handle = FindWindow(None, title)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)
        
        gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, ScreenSize.x, 0, ScreenSize.y, -1, 1)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        exstyle = GetWindowLong(self.handle, GWL_EXSTYLE)
        exstyle |= WS_EX_LAYERED
        exstyle |= WS_EX_TRANSPARENT
        SetWindowLong(self.handle, GWL_EXSTYLE, exstyle)

        self.overlay_state = True

    def close(self) -> None:
        glfw.set_window_should_close(self.window, True)
        if glfw.window_should_close(self.window) == 1:
            self.overlay_state = False
            ctypes.WinDLL('kernel32.dll').CloseHandle(self.handle)
            glfw.destroy_window(self.window)

    def refresh(self) -> None:
        glfw.swap_buffers(self.window)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glfw.poll_events()

    def draw_line(self, start_point_x: float, start_point_y: float, end_point_x: float, end_point_y: float, line_width: float, color: Vector3) -> None:
        gl.glLineWidth(line_width)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color, 0.7)
        gl.glVertex2f(start_point_x, start_point_y)
        gl.glVertex2f(end_point_x, end_point_y)
        gl.glEnd()

    def draw_full_box(self, start_point_x: float, start_point_y: float, width, height, line_width: float, color: Vector3) -> None:
        gl.glLineWidth(line_width)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color, 1.0)
        gl.glVertex2f(start_point_x, start_point_y)
        gl.glVertex2f(start_point_x + width, start_point_y)
        gl.glVertex2f(start_point_x + width, start_point_y + height)
        gl.glVertex2f(start_point_x, start_point_y + height)
        gl.glEnd()

    def draw_text(self, text: str, x: int | float, y: int | float, color: Vector3, alpha: float, font=glut.GLUT_BITMAP_HELVETICA_18) -> None:
        gl.glColor4f(*color, alpha)
        gl.glRasterPos2i(int(x), int(y))
        lines = text.split("\n")
        line_height = 24

        for i, line in enumerate(lines):
            y = y - i * line_height / 1.2

            for c in line:
                glut.glutBitmapCharacter(font, ord(c))

    def w2s(self, pos: Vector3, matrix):
        z = pos.x * matrix[12] + pos.y * matrix[13] + pos.z * matrix[14] + matrix[15]
        if z < 0.01:
            return None

        x = pos.x * matrix[0] + pos.y * matrix[1] + pos.z * matrix[2] + matrix[3]
        y = pos.x * matrix[4] + pos.y * matrix[5] + pos.z * matrix[6] + matrix[7]

        xx = x / z
        yy = y / z
        _x = (ScreenSize.x / 2 * xx) + (xx + ScreenSize.x / 2)
        _y = (ScreenSize.y / 2 * yy) + (yy + ScreenSize.y / 2)
        return [_x, _y]
