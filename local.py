from helper import *
import offsets, struct

class LocalPlayer():
    def __init__(self, mem) -> None:
        self.mem = mem

    def local_player(self) -> int:
        return self.mem.game_handle.read_longlong(self.mem.client_dll + offsets.dwLocalPlayer)
    
    def attack_state(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwForceAttack)

    def force_attack(self, value: int) -> None:
        self.mem.game_handle.write_uint(self.mem.client_dll + offsets.dwForceAttack, value)

    def force_jump(self, value: int) -> None:
        self.mem.game_handle.write_uint(self.mem.client_dll + offsets.dwForceJump, value)

    def mat_fullbright(self) -> None:
        if hex(self.mem.game_handle.read_short(self.mem.materialsystem_dll + offsets.mat_fullbright)) == "0x5060":
            self.mem.game_handle.write_short(self.mem.materialsystem_dll + offsets.mat_fullbright, 0x5061)
        else:
            self.mem.game_handle.write_short(self.mem.materialsystem_dll + offsets.mat_fullbright, 0x5060)

    def view_matrix(self) -> Vector3:
        view_matrix_base = self.mem.game_handle.read_longlong(self.mem.engine_dll + offsets.dwViewMatrix) + 0x2D4
        view_matrix = self.mem.game_handle.read_bytes(view_matrix_base, 64)
        return struct.unpack("16f", view_matrix)
    
    def set_view_angle1(self, angle: float) -> None:
        self.mem.game_handle.write_float(self.mem.engine_dll + offsets.m_angRotation + 4, angle)

    def get_view_angle1(self) -> float:
        return self.mem.game_handle.read_float(self.mem.engine_dll + offsets.m_angRotation + 4)

    def set_view_angle2(self, angle: float) -> None:
        self.mem.game_handle.write_float(self.mem.engine_dll + offsets.m_angRotation, angle)
        
    def get_view_angle2(self) -> float:
        return self.mem.game_handle.read_float(self.mem.engine_dll + offsets.m_angRotation)