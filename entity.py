import offsets, struct
from helper import *
from gui import *

class Entity():
    def __init__(self, mem) -> None:
        self.mem = mem
        self.entity_list = []

    def entity_loop(self) -> list:
        try:
            self.entity_list.clear()
            for i in range(0, self.get_server_slots()):
                entity = self.mem.game_handle.read_longlong(self.mem.client_dll + offsets.dwEntityList + i * 0x20)
                if entity != 0:
                    self.entity_list.append([i+1, entity])
        except Exception as err:
            pass

    def get_server_slots(self) -> int:
        return self.mem.game_handle.read_int(self.mem.engine_dll + offsets.MaxOnlinePlayers)

    def get_health(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iHealth)

    def get_team(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iTeamNum)

    def is_dormant(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_nRenderMode)

    def is_invisible(self, entity: int) -> int:
        return hex(self.mem.game_handle.read_longlong(entity + offsets.m_clrRender))

    def is_noclipping(self, entity: int) -> int:
        return hex(self.mem.game_handle.read_int(entity + offsets.m_nRenderFX))

    def is_spectating(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iObserverMode)
    
    def spectating_target(self, entity: int) -> int:
        return self.mem.game_handle.read_uint(entity + offsets.m_hObserverTarget) & 0xFFF

    def get_position(self, entity: int) -> Vector3:
        try:
            position_bytes = self.mem.game_handle.read_bytes(entity + offsets.m_vecOrigin, 0xC)
            var = struct.unpack("3f", position_bytes)
            return Vector3(*var)
        except Exception as err:
            pass