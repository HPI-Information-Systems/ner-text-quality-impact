import random
import nlpaug.augmenter.word as naw
import string

# Use two other seed values 1 and 1234 for creating data with different seeds
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
        org_word, pos_tag, tag = line.split()
        
        augmented_word = aug.augment(org_word)
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")
        ori_idx = idx

        if(org_word != augmented_word):
            count_entity.append([ori_idx,org_word,augmented_word])
        
        attempt_counter = 0
        max_attempts = 10

        while org_word == augmented_word and attempt_counter < max_attempts :  # if the word did not change upon augmentation
            random_idx, new_word, new_pos_tag, new_tag = get_random_word(lines, chosen_indices)
            augmented_word1 = aug.augment(new_word)
            augmented_word1 = augmented_word1[0] if isinstance(augmented_word1, list) else augmented_word1
            augmented_word1 = augmented_word1.replace(" ", "")
            if augmented_word1 != new_word:
                count_entity.append([ori_idx,org_word,random_idx,new_word,augmented_word1])
                idx = random_idx
                pos_tag = new_pos_tag
                tag = new_tag
                augmented_word = augmented_word1

            attempt_counter += 1
            if attempt_counter == 9:
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
    
lines = read_file_content('train.txt')

# Different error rates for Spelling Errors
err_per = [0.03, 0.05, 0.10, 0.15, 0.20]

for val in err_per:
    modified_lines = introduce_spelling_errors(lines, val)
    val = int(val * 100)
    write_modified_content(modified_lines, 'train_42_{}.txt'.format(val)) # Save file with new name indicating seed number and error percentage