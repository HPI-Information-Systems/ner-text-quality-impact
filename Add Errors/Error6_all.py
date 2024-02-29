import random
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
import string

random.seed(42)

def introduce_spelling_errors(lines, err_per):
   
    non_empty_lines = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    filtered_lines = [(idx, line) for idx, line in non_empty_lines if line.split()[0] not in string.punctuation]
    chosen_lines_with_idx = random.sample(filtered_lines, int(err_per * len(filtered_lines)))
    chosen_indices = {idx for idx, _ in chosen_lines_with_idx}

    print('Total number of words', len(filtered_lines))
    print('Total nuumber of choosen words', len(chosen_lines_with_idx))
    
    aug = naw.SpellingAug(aug_p=1.0)

    count_entity = []
    
    for idx, line in chosen_lines_with_idx:
        org_word, tag = line.split()
        
        augmented_word = aug.augment(org_word)
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")
        ori_idx = idx

        if(org_word != augmented_word):
            count_entity.append([ori_idx,org_word,augmented_word])
        
        attempt_counter = 0
        max_attempts = 10

        while org_word == augmented_word and attempt_counter < max_attempts :  # if the word did not change upon augmentation
            random_idx, new_word, new_tag = get_random_word(lines, chosen_indices)
            augmented_word1 = aug.augment(new_word)
            augmented_word1 = augmented_word1[0] if isinstance(augmented_word1, list) else augmented_word1
            augmented_word1 = augmented_word1.replace(" ", "")
            if augmented_word1 != new_word:
                count_entity.append([ori_idx,org_word,random_idx,new_word,augmented_word1])
                idx = random_idx
                tag = new_tag
                augmented_word = augmented_word1

            attempt_counter += 1
            if attempt_counter == 9:
                print(f'Loop ran 10 times for idx: {ori_idx}')

        lines[idx] = f"{augmented_word} {tag}\n"

    return lines

def introduce_typo_errors(lines,err_per):
   
    non_empty_lines = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    chosen_lines_idx = random.sample(non_empty_lines, int(err_per * len(non_empty_lines)))
    chosen_indices = {idx for idx, _ in chosen_lines_idx}

    print('Total number of words', len(non_empty_lines))
    print('Total nuumber of choosen words', len(chosen_lines_idx))

    char_max_choices = [1, 2]
    char_max_weights = [0.9, 0.1]  # Adjust the weights as needed

    aug_char_max = random.choices(char_max_choices, char_max_weights)[0]
    aug = nac.KeyboardAug(aug_char_p=1.0, aug_char_min=1, aug_char_max=aug_char_max)
    
    count_entity = []
    
    for idx, line in chosen_lines_idx:
        org_word, tag = line.split()
        
        augmented_word = aug.augment(org_word)
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")
        augmented_word = ''.join([char.upper() if orig_char.isupper() else char.lower() if orig_char.islower() else char for char, orig_char in zip(augmented_word, org_word)])
        ori_idx = idx

        if(org_word != augmented_word):
            count_entity.append([ori_idx,org_word,augmented_word])
        
        attempt_counter = 0
        max_attempts = 15

        while org_word == augmented_word and attempt_counter < max_attempts :  # if the word did not change upon augmentation
            random_idx, new_word, new_tag = get_random_word(lines, chosen_indices)
            augmented_word1 = aug.augment(new_word)
            augmented_word1 = augmented_word1[0] if isinstance(augmented_word1, list) else augmented_word1
            augmented_word1 = augmented_word1.replace(" ", "")
            augmented_word1= ''.join([char.upper() if orig_char.isupper() else char.lower() if orig_char.islower() else char for char, orig_char in zip(augmented_word1, new_word)])
            if augmented_word1 != new_word:
                count_entity.append([ori_idx,org_word,random_idx,new_word,augmented_word1])
                idx = random_idx
                tag = new_tag
                augmented_word = augmented_word1

            attempt_counter += 1
            if attempt_counter == 14:
                print(f'Loop ran 10 times for idx: {ori_idx}')

        lines[idx] = f"{augmented_word} {tag}\n"

    return lines

def introduce_ocr_errors(lines, err_per):
   
    non_empty_lines = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    chosen_lines_idx = random.sample(non_empty_lines, int(err_per * len(non_empty_lines)))
    chosen_indices = {idx for idx, _ in chosen_lines_idx}

    print('Total number of words', len(non_empty_lines))
    print('Total nuumber of choosen words', len(chosen_lines_idx))
    
    aug = nac.OcrAug (aug_char_p=1.0)
    count_entity = []
    
    for idx, line in chosen_lines_idx:
        org_word, tag = line.split()
        
        augmented_word = aug.augment(org_word)
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")
        ori_idx = idx

        if(org_word != augmented_word):
            count_entity.append([ori_idx,org_word,augmented_word])
        
        attempt_counter = 0
        max_attempts = 10

        while org_word == augmented_word and attempt_counter < max_attempts :  # if the word did not change upon augmentation
            random_idx, new_word, new_tag = get_random_word(lines, chosen_indices)
            augmented_word1 = aug.augment(new_word)
            augmented_word1 = augmented_word1[0] if isinstance(augmented_word1, list) else augmented_word1
            augmented_word1 = augmented_word1.replace(" ", "")
            if augmented_word1 != new_word:
                count_entity.append([ori_idx,org_word,random_idx,new_word,augmented_word1])
                idx = random_idx
                tag = new_tag
                augmented_word = augmented_word1

            attempt_counter += 1
            if attempt_counter == 9:
                print(f'Loop ran 10 times for idx: {ori_idx}')

        lines[idx] = f"{augmented_word} {tag}\n"

    return lines

def get_random_word(lines, chosen_indices):
    attempts = 0
    while attempts < 30:
        idx = random.randrange(len(lines))
        random_line = lines[idx]

        if idx not in chosen_indices and ' ' in random_line:
            word, tag = random_line.split()
            if word not in string.punctuation:
                return idx, word, tag

        attempts += 1

data_path = "train.txt"

with open(data_path, "r") as file:
    lines = file.readlines()

chunks = [lines[i:i + 450] for i in range(0, len(lines), 450)]

processed_chunks = []
for chunk in chunks:
    n = random.randint(1, 10)
    new_chunk = chunk[:-n]
    processed_chunks.extend(new_chunk)

processed_chunks = introduce_spelling_errors(processed_chunks, 0.20)
processed_chunks = introduce_typo_errors(processed_chunks, 0.25)
processed_chunks = introduce_ocr_errors(processed_chunks, 0.23)

destination = "train_202523_allerr.txt"

with open(destination, "w") as file:
    file.writelines(processed_chunks)
