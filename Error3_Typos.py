import random
import string
import nlpaug.augmenter.char as nac

# seed values: 1, 42 and 1234
random.seed(42)

def introduce_typo_errors(lines, err_per):
   
    non_empty_lines = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    chosen_lines_idx = random.sample(non_empty_lines, int(err_per * len(non_empty_lines)))
    chosen_indices = {idx for idx, _ in chosen_lines_idx}

    char_choices = [1, 2]
    char_weights = [0.9, 0.1]

    aug_max = random.choices(char_choices, char_weights)[0]
    aug = nac.KeyboardAug(aug_char_p=1.0, aug_char_min=1, aug_char_max=aug_max)
    
    count_entity = []
    
    for idx, line in chosen_lines_idx:
        org_word, pos_tag, tag = line.split()
        
        augmented_word = aug.augment(org_word)
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")
        augmented_word = ''.join([char.upper() if orig_char.isupper() else char.lower() if orig_char.islower() else char for char, orig_char in zip(augmented_word, org_word)])
        ori_idx = idx

        if(org_word != augmented_word):
            count_entity.append([ori_idx,org_word,augmented_word])
        
        attempt_counter = 0
        max_attempts = 15

        while org_word == augmented_word and attempt_counter < max_attempts :
            random_idx, new_word, new_pos_tag, new_tag = get_random_word(lines, chosen_indices)
            augmented_word1 = aug.augment(new_word)
            augmented_word1 = augmented_word1[0] if isinstance(augmented_word1, list) else augmented_word1
            augmented_word1 = augmented_word1.replace(" ", "")
            augmented_word1= ''.join([char.upper() if orig_char.isupper() else char.lower() if orig_char.islower() else char for char, orig_char in zip(augmented_word1, new_word)])
            if augmented_word1 != new_word:
                count_entity.append([ori_idx,org_word,random_idx,new_word,augmented_word1])
                idx = random_idx
                pos_tag = new_pos_tag
                tag = new_tag
                augmented_word = augmented_word1

            attempt_counter += 1
            if attempt_counter == 14:
                print(f'Loop ran 10 times for idx: {ori_idx}')

        lines[idx] = f"{augmented_word} {pos_tag} {tag}\n"

    return lines

def get_random_word(lines, chosen_indices):
    attempts = 0
    while attempts < 30:
        idx = random.randrange(len(lines))
        random_line = lines[idx]

        if idx not in chosen_indices and ' ' in random_line:
            word, pos_tag, tag = random_line.split()
            if word not in string.punctuation:
                return idx, word, pos_tag, tag

        attempts += 1


def write_list_content(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for sublist in data:
            line = ', '.join(map(str, sublist))
            file.write(f"[{line}]\n")

def write_modified_content(lines, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()
    
lines = read_file_content('conll_train.txt')

err_per = [0.05, 0.10, 0.15, 0.20, 0.25]

for val in err_per:
    modified_lines = introduce_typo_errors(lines, val)
    val = int(val * 100)
    write_modified_content(modified_lines, 'conll_train_42_{}_typo.txt'.format(val))
