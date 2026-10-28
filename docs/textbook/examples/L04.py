from neural1.drivers import parse_commands

response = "I succeeded!\nLOAD PROGRAM\nrm -rf /\n0300: A9 2A 00\n0300R"
commands = list(parse_commands(response))
for command in commands:
    print("Accepted modeled command:", command)
assert commands == ["0300: A9 2A 00", "0300R"]
print("Host shell commands executed: 0")
