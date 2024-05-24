from main_processor import MainProcessor

mp = MainProcessor()

mp.attach_co_processor(hash_5)
cpu_instructions = load("File.asm")
mp.load_program(cpu_instructions)

pil = generate_pil(mp.generate_constraints())
proof = run(pil)
