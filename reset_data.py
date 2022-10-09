import gzip
RESET = False

def reset():
    with gzip.open("data.json.gz", "wb") as f:
        f.write("".encode("utf-8"))
    with open("searched_matches.txt", "w") as f:
        f.write("")

if RESET:
    reset()