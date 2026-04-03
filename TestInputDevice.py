import sounddevice as sd
print("Available devices: ")
print(sd.query_devices())
print("\n" + "current: ")
print(sd.default.device[0])