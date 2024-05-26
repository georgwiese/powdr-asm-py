from hello_world import HelloWorldProcessor

if __name__ == "__main__":
    
    with open("hello_world.asm") as f:
        program = f.read()

    HelloWorldProcessor.run(program, num_steps=2**16)