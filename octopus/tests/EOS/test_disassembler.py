import unittest

from octopus.platforms.EOS.disassembler import EosDisassembler


class EosDisassemblerTestCase(unittest.TestCase):

    def testDisassemble(self):
        def disassemble(bytecode, result):
            disasm = len(EosDisassembler(bytecode).disassemble())
            self.assertEqual(disasm, result)

        def disasmOne(bytecode, result):
            disasm = str(EosDisassembler(bytecode).disassemble_opcode(bytecode))
            self.assertEqual(disasm, result)

        def disasm(bytecode, result):
            text = EosDisassembler(bytecode).disassemble(r_format='text')
            self.assertEqual(text, result)

        def disasmModule(bytecode, result_func, result_insn):
            funcs = EosDisassembler().disassemble_module(bytecode)
            self.assertEqual(len(funcs), result_func)
            self.assertEqual(sum([len(i) for i in funcs]), result_insn)

        # Simple
        bytecode = bytearray([2, 127, 65, 24, 16, 28, 65, 0, 15, 11])
        result = 'block -1\ni32.const 24\ncall 28\ni32.const 0\nreturn\nend'

        disassemble(bytecode, 6)
        disasmOne(b'\x02\x7f', 'block -1')
        disasm(bytecode, result)

        # Helloworld
        bytecode_hex = "0061736d0100000001110460017f0060017e0060000060027e7e00021b0203656e76067072696e746e000103656e76067072696e7473000003030202030404017000000503010001071903066d656d6f7279020004696e69740002056170706c7900030a20020600411010010b17004120100120001000413010012001100041c00010010b0b3f050041040b04504000000041100b0d496e697420576f726c64210a000041200b0e48656c6c6f20576f726c643a20000041300b032d3e000041c0000b020a000029046e616d6504067072696e746e0100067072696e7473010004696e697400056170706c790201300131"
        disasmModule(bytecode_hex, 2, 14)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(EosDisassemblerTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
