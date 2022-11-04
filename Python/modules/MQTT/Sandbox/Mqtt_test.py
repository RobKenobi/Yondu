

# =========================================================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client is connected")
    else:
        print("Client is not connected")



def on_log(client, userdata, level, buf):
    print("log" + buf)
# =========================================================================