import random

random.seed(42)

data_path = 'train.txt'

with open(data_path, "r") as file:
    lines = file.readlines()

chunks = [lines[i:i + 450] for i in range(0, len(lines), 450)]

processed_chunks = []
for chunk in chunks:
    n = random.randint(1, 10)
    new_chunk = chunk[:-n]
    processed_chunks.extend(new_chunk)

with open("train_42_sse.txt", "w") as file:
    file.writelines(processed_chunks)

