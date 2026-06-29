import customtkinter as ctk
from tkinter import filedialog
from dataclasses import dataclass, field
import threading
import time

#  FRONTEND

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, on_run):
        super().__init__()
        self.on_run = on_run
        self.title("Instruction Cycle Simulator")
        self.geometry("720x520")
        self.resizable(False, False)
        self._build_home()

    def _build_home(self):
        self._clear()

        ctk.CTkLabel(
            self, text="Instruction Cycle",
            font=ctk.CTkFont("Courier New", 36, "bold"),
            text_color="#00FF99"
        ).place(relx=0.5, rely=0.26, anchor="center")

        ctk.CTkLabel(
            self, text="Simulator",
            font=ctk.CTkFont("Courier New", 28),
            text_color="#AAAAAA"
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(
            self, text="UEM — Arquitetura e Organização de Computadores",
            font=ctk.CTkFont("Courier New", 11),
            text_color="#555555"
        ).place(relx=0.5, rely=0.50, anchor="center")

        ctk.CTkButton(
            self, text="Start",
            font=ctk.CTkFont("Courier New", 14, "bold"),
            fg_color="#00FF99", text_color="#000000",
            hover_color="#00CC77",
            width=160, height=42,
            command=self._build_load
        ).place(relx=0.5, rely=0.66, anchor="center")

    def _build_load(self):
        self._clear()

        ctk.CTkLabel(
            self, text="Load Program",
            font=ctk.CTkFont("Courier New", 22, "bold"),
            text_color="#00FF99"
        ).place(relx=0.5, rely=0.14, anchor="center")

        ctk.CTkLabel(
            self, text="Select an input file (.txt)",
            font=ctk.CTkFont("Courier New", 12),
            text_color="#888888"
        ).place(relx=0.5, rely=0.25, anchor="center")

        self._path_var = ctk.StringVar(value="")
        ctk.CTkEntry(
            self, textvariable=self._path_var,
            font=ctk.CTkFont("Courier New", 12),
            width=420, height=38,
            placeholder_text="file path...",
            fg_color="#1A1A1A", border_color="#333333"
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkButton(
            self, text="Browse",
            font=ctk.CTkFont("Courier New", 12),
            fg_color="#222222", text_color="#00FF99",
            hover_color="#2A2A2A", border_width=1,
            border_color="#00FF99",
            width=120, height=38,
            command=self._browse
        ).place(relx=0.5, rely=0.52, anchor="center")

        ctk.CTkLabel(
            self, text="Simulation Speed",
            font=ctk.CTkFont("Courier New", 11),
            text_color="#555555"
        ).place(relx=0.5, rely=0.63, anchor="center")

        self._delay_var = ctk.DoubleVar(value=0.3)
        ctk.CTkSlider(
            self, from_=0.05, to=1.0,
            variable=self._delay_var,
            width=260,
            progress_color="#00FF99",
            button_color="#00FF99",
            button_hover_color="#00CC77"
        ).place(relx=0.5, rely=0.71, anchor="center")

        ctk.CTkButton(
            self, text="Execute",
            font=ctk.CTkFont("Courier New", 14, "bold"),
            fg_color="#00FF99", text_color="#000000",
            hover_color="#00CC77",
            width=160, height=42,
            command=self._run
        ).place(relx=0.5, rely=0.82, anchor="center")

        ctk.CTkButton(
            self, text="← Back",
            font=ctk.CTkFont("Courier New", 11),
            fg_color="transparent", text_color="#555555",
            hover_color="#1A1A1A",
            width=80, height=28,
            command=self._build_home
        ).place(relx=0.5, rely=0.93, anchor="center")

        self._msg = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont("Courier New", 11),
            text_color="#FF4444"
        )
        self._msg.place(relx=0.5, rely=0.91, anchor="center")

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Selecionar arquivo de entrada",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self._path_var.set(path)

    def _run(self):
        path = self._path_var.get().strip()
        if not path:
            self._msg.configure(text="Select a file before running.")
            return
        self._msg.configure(text="")
        self._build_terminal()

        threading.Thread(
            target=self.on_run,
            args=(path, self, self._delay_var.get()),
            daemon=True
        ).start()

    def _build_terminal(self):
        self._clear()

        ctk.CTkLabel(
            self, text="Simulation",
            font=ctk.CTkFont("Courier New", 18, "bold"),
            text_color="#00FF99"
        ).place(relx=0.5, rely=0.06, anchor="center")

        self._terminal = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont("Courier New", 12),
            width=660, height=370,
            fg_color="#0A0A0A", text_color="#00FF99",
            border_color="#1F1F1F", border_width=1
        )
        self._terminal.place(relx=0.5, rely=0.46, anchor="center")
        self._terminal.configure(state="disabled")

        self._done_btn = ctk.CTkButton(
            self, text="← New File",
            font=ctk.CTkFont("Courier New", 12, "bold"),
            fg_color="#00FF99", text_color="#000000",
            hover_color="#00CC77",
            width=160, height=36,
            state="disabled",
            command=self._build_load
        )
        self._done_btn.place(relx=0.5, rely=0.93, anchor="center")

    def terminal_write(self, text: str, color: str = "#00FF99"):
        def _write():
            self._terminal.configure(state="normal")
            self._terminal.insert("end", text + "\n")
            self._terminal.see("end")
            self._terminal.configure(state="disabled")
        self.after(0, _write)

    def terminal_done(self):
        self.after(0, lambda: self._done_btn.configure(state="normal"))

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


#  BACKEND

@dataclass
class Register:
    size: int
    value: int = 0

    def __post_init__(self):
        self._mask = (1 << self.size) - 1

    def read(self) -> int:
        return self.value

    def write(self, value: int):
        self.value = value & self._mask

    def reset(self):
        self.value = 0

@dataclass
class RegisterA(Register):
    size: int = 40

@dataclass
class RegisterB(Register):
    size: int = 40

@dataclass
class ProgramCounter(Register):
    size: int = 12
    def increment(self): self.write(self.value + 1)

@dataclass
class Accumulator(Register):
    size: int = 40

@dataclass
class MultiplierQuotient(Register):
    size: int = 40

@dataclass
class MemoryBufferRegister(Register):
    size: int = 40

@dataclass
class InstructionBufferRegister(Register):
    size: int = 20

@dataclass
class InstructionRegister(Register):
    size: int = 8
    def opcode(self) -> int: return self.read()

@dataclass
class MemoryAddressRegister(Register):
    size: int = 12

@dataclass
class RemainderRegister(Register):
    size: int = 40

@dataclass
class RAM:
    capacity: int = 256
    word_size: int = 40
    memory: list[int] = field(default_factory=lambda: [0] * 256)

    def read(self, address: int) -> int:
        return self.memory[address]

    def write(self, address: int, value: int):
        self.memory[address] = value

@dataclass
class Flag(Register):
    size: int = 1
    def set(self):   self.write(1)
    def clear(self): self.write(0)
    def is_set(self) -> bool: return self.value == 1

@dataclass
class CarryFlag(Flag):    pass
@dataclass
class NegativeFlag(Flag): pass
@dataclass
class ZeroFlag(Flag):     pass

@dataclass
class ALU:
    C: CarryFlag    = field(default_factory=CarryFlag)
    N: NegativeFlag = field(default_factory=NegativeFlag)
    Z: ZeroFlag     = field(default_factory=ZeroFlag)

    def _update_flags(self, result: int, carry: int = 0):
        self.C.write(carry)
        self.N.write(1 if result < 0 else 0)
        self.Z.write(1 if result == 0 else 0)

    def add(self, a: int, b: int) -> int:
        result = a + b
        self._update_flags(result, carry=1 if result > (1 << 40) - 1 else 0)
        return result

    def sub(self, a: int, b: int) -> int:
        result = a - b
        self._update_flags(result)
        return result

    def mul(self, a: int, b: int) -> int:
        result = a * b
        self._update_flags(result)
        return result

    def div(self, a: int, b: int) -> tuple[int, int]:
        result, remainder = divmod(a, b)
        self._update_flags(result)
        return result, remainder

@dataclass
class CPU:
    ram: RAM
    alu: ALU                   = field(default_factory=ALU)
    pc:  ProgramCounter        = field(default_factory=ProgramCounter)
    mar: MemoryAddressRegister = field(default_factory=MemoryAddressRegister)
    mbr: MemoryBufferRegister  = field(default_factory=MemoryBufferRegister)
    ir:  InstructionRegister   = field(default_factory=InstructionRegister)
    ac:  Accumulator           = field(default_factory=Accumulator)
    mq:  MultiplierQuotient    = field(default_factory=MultiplierQuotient)
    r:   RemainderRegister     = field(default_factory=RemainderRegister)
    a:   RegisterA             = field(default_factory=RegisterA)
    b:   RegisterB             = field(default_factory=RegisterB)

    def fetch(self):
        self.mar.write(self.pc.read())
        self.mbr.write(self.ram.read(self.mar.read()))
        self.ir.write(self.mbr.read())
        self.pc.increment()

    def LOAD(self, address: int):
        self.mar.write(address)
        self.mbr.write(self.ram.read(self.mar.read()))
        self.ac.write(self.mbr.read())

    def STORE(self, address: int):
        self.mar.write(address)
        self.mbr.write(self.ac.read())
        self.ram.write(self.mar.read(), self.mbr.read())

    def ADD(self, address: int):
        self.mar.write(address)
        self.mbr.write(self.ram.read(self.mar.read()))
        self.ac.write(self.alu.add(self.ac.read(), self.mbr.read()))

    def SUB(self, address: int):
        self.mar.write(address)
        self.mbr.write(self.ram.read(self.mar.read()))
        self.ac.write(self.alu.sub(self.ac.read(), self.mbr.read()))

    def DIV(self, address: int):
        self.mar.write(address)
        self.mbr.write(self.ram.read(self.mar.read()))
        result, remainder = self.alu.div(self.ac.read(), self.mbr.read())
        self.ac.write(result)
        self.r.write(remainder)

    def PUSH_A(self): self.a.write(self.ac.read())
    def PUSH_B(self): self.b.write(self.ac.read())
    def POP_A(self):  self.ac.write(self.a.read())
    def POP_B(self):  self.ac.write(self.b.read())

    def SUB_REG_B(self):
        self.ac.write(self.alu.sub(self.ac.read(), self.b.read()))

    def ADD_REG_B(self):
        self.ac.write(self.alu.add(self.ac.read(), self.b.read()))


def execute_instruction(cpu, instruction, log):
    parts = instruction.replace(",", "").split()
    op    = parts[0].upper()
    reg   = parts[1].upper()
    target = cpu.a if reg == "A" else cpu.b

    log(f"  ▶  {instruction}")

    if op == "MOV":
        src = cpu.a if parts[2].upper() == "A" else cpu.b
        target.write(src.read())
        cpu.ac.write(target.read())
        log(f"     {reg} ← {src.read()}   |  AC = {cpu.ac.read()}")
        cpu.pc.increment()
        return

    addr = int(parts[2], 16) if "0x" in parts[2].lower() else int(parts[2])

    if op == "LOAD":
        cpu.mar.write(addr)
        cpu.mbr.write(cpu.ram.read(cpu.mar.read()))
        target.write(cpu.mbr.read())
        cpu.ac.write(target.read())
        log(f"     MAR={hex(addr)}  MBR={cpu.mbr.read()}  {reg}={target.read()}  AC={cpu.ac.read()}")

    elif op == "STORE":
        cpu.mar.write(addr)
        cpu.mbr.write(target.read())
        cpu.ram.write(cpu.mar.read(), cpu.mbr.read())
        log(f"     MAR={hex(addr)}  MEM[{hex(addr)}] ← {target.read()}")

    elif op == "ADD":
        antes = target.read()
        cpu.mar.write(addr)
        cpu.mbr.write(cpu.ram.read(cpu.mar.read()))
        result = cpu.alu.add(target.read(), cpu.mbr.read())
        target.write(result)
        cpu.ac.write(result)
        log(f"     {antes} + MEM[{hex(addr)}]({cpu.mbr.read()}) = {result}  |  C={cpu.alu.C.read()} N={cpu.alu.N.read()} Z={cpu.alu.Z.read()}")

    elif op == "SUB":
        antes = target.read()
        cpu.mar.write(addr)
        cpu.mbr.write(cpu.ram.read(cpu.mar.read()))
        result = cpu.alu.sub(target.read(), cpu.mbr.read())
        target.write(result)
        cpu.ac.write(result)
        log(f"     {antes} - MEM[{hex(addr)}]({cpu.mbr.read()}) = {result}  |  C={cpu.alu.C.read()} N={cpu.alu.N.read()} Z={cpu.alu.Z.read()}")

    elif op == "MULT":
        antes = target.read()
        cpu.mar.write(addr)
        cpu.mbr.write(cpu.ram.read(cpu.mar.read()))
        result = cpu.alu.mul(target.read(), cpu.mbr.read())
        target.write(result)
        cpu.ac.write(result)
        log(f"     {antes} × MEM[{hex(addr)}]({cpu.mbr.read()}) = {result}  |  C={cpu.alu.C.read()} N={cpu.alu.N.read()} Z={cpu.alu.Z.read()}")

    cpu.pc.increment()
    log(f"     PC ← {hex(cpu.pc.read())}")


def load_program(ram, cpu, filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    data, instructions = [], []
    start_address = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("0x") and not any(c in line for c in [",", " "]):
            start_address = int(line, 16)
            instructions  = lines[i + 1:]
            break
        else:
            data.append(int(line))
        i += 1

    for addr, value in enumerate(data):
        ram.write(addr, value)

    cpu.pc.write(start_address)
    return instructions


def run_program(filename, app, delay):
    ram = RAM()
    cpu = CPU(ram)

    def log(msg):
        app.terminal_write(msg)
        time.sleep(delay)

    try:
        instructions = load_program(ram, cpu, filename)

        log(f"{'─' * 50}")
        log(f"  Program loaded: {filename.split('/')[-1]}")
        log(f"  {len(instructions)} instruction(s) found")
        log(f"  Initial PC: {hex(cpu.pc.read())}")
        log(f"{'─' * 50}")

        for i, instruction in enumerate(instructions):
            log(f"\n[ Instruction {i + 1} ]")
            execute_instruction(cpu, instruction, log)

        log(f"\n{'─' * 50}")
        log(f"  Execution completed")
        log(f"{'─' * 50}")
        log(f"  A   = {cpu.a.read()}")
        log(f"  B   = {cpu.b.read()}")
        log(f"  AC  = {cpu.ac.read()}")
        log(f"  PC  = {hex(cpu.pc.read())}")
        log(f"  MAR = {hex(cpu.mar.read())}")
        log(f"  MBR = {cpu.mbr.read()}")
        log(f"  C={cpu.alu.C.read()}  N={cpu.alu.N.read()}  Z={cpu.alu.Z.read()}")
        log(f"{'─' * 50}")

    except Exception as e:
        log(f"\n  ERRO: {e}")

    app.terminal_done()


def main():
    app = App(on_run=run_program)
    app.mainloop()


if __name__ == "__main__":
    main()