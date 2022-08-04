import windows


class ThreadStackFinder:

    @staticmethod
    def get_ce_thread_stack(process_name: str):
        target_process = None
        stack_base_list = []
        pointer_size = None
        stack_size = None
        base_thread_init_thunk_address = None
        cheat_engine_thread_stack_list = []
        process_list = windows.system.enumerate_processes()
        for process in process_list:
            # print("process name:", process.name)
            if process.name == process_name:
                target_process = process

        if target_process.bitness == 64:
            pointer_size = 8
            stack_size = 4096 * 2
        else:
            pointer_size = 4
            stack_size = 4096

        thread_list = target_process.threads

        for thread in thread_list:
            # print("startAddress:", hex(thread.start_address))
            teb = thread.teb_base
            # There is something wrong when process run in wow64, get teb from lib must add 0x2000.
            # 第三方库作者的bug,如果是64位系统运行32位程序 ,这里相差了0x2000
            if target_process.is_wow_64:
                teb = teb + 0x2000
            print("teb:", hex(teb), "id:", hex(thread.tid))
            stack_base_address = teb + pointer_size
            stack_base = target_process.read_ptr(stack_base_address)
            stack_base_list.append(stack_base)
            # print("stack_base:", hex(stack_base))

        modules_list = target_process.peb.modules
        for module in modules_list:
            print("module:", module.pe.export_name)
            if module.pe.export_name == "KERNEL32.dll":
                # kernel32baseAddress = module.pe.baseaddr
                base_thread_init_thunk_address = module.pe.exports['BaseThreadInitThunk']

        for stack_top in stack_base_list:
            print("stacktop:", hex(stack_top), "readRange:", hex(stack_top - stack_size))
            buffer = target_process.read_memory(stack_top - stack_size, stack_size)
            index = 0
            byte_counter = 0
            temp_pointer = 0
            for byte in buffer:
                # read pointer, each pointer save in temp_pointer
                # buffer[7] << 64 ^ buffer[6] << (64-8) ... depends target_process.bitness
                temp_pointer = temp_pointer ^ (byte << 8 * byte_counter)
                byte_counter = byte_counter + 1
                if byte_counter == pointer_size:
                    if target_process.is_wow_64:
                        if base_thread_init_thunk_address == temp_pointer:
                            cheat_engine_thread_stack_list.append(hex(stack_top - stack_size + pointer_size * index))
                            print("index:", index, "hex:", hex(stack_top - stack_size + pointer_size * index),
                                  "temPointer",
                                  hex(temp_pointer))
                    else:
                        if base_thread_init_thunk_address <= temp_pointer <= base_thread_init_thunk_address + 0x100:
                            cheat_engine_thread_stack_list.append(hex(stack_top - stack_size + pointer_size * index))
                            print("index:", index, "hex:", hex(stack_top - stack_size + pointer_size * index),
                                  "temPointer",
                                  hex(temp_pointer))
                    index = index + 1
                    byte_counter = 0
                    temp_pointer = 0
        # cheat_engine_thread_stack_list[0] is THREADSTACK0 in CheatEngine
        return cheat_engine_thread_stack_list
