crontable = []
outputs = []
channel = "C02GGKFFX"  # TEST
#channel = "C0B8T790S"  # quick-order

def process_message(data):
    if data['channel'] == channel and "why" in data['text']:
        outputs.append([data['channel'], "Why not..?"])
