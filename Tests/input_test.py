from inputs import read_file,generate_timestamp,generate_timestamp_periodic
def test_read_file(path):
    resources,subsystem = read_file(path)
    print(resources)
    print(subsystem)

def test_generate_time_stamp(path):
    _,subsystem = read_file(path)
    time1 = generate_timestamp(subsystem[0])
    time2 = generate_timestamp(subsystem[1])
    time3 = generate_timestamp_periodic(subsystem[2])
    time4 = generate_timestamp(subsystem[3])
    print(f"Time stamp1 {time1}")
    print("---------------")
    print(f"Time stamp2 {time2}")
    print("---------------")
    print(f"Time stamp3 {time3}")
    print("---------------")
    print(f"Time stamp4 {time4}")
    print("---------------")
    
