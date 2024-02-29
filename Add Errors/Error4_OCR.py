import random
import nlpaug.augmenter.char as nac
import string

random.seed(42)

# Use two other seed values 1 and 1234 for creating data with different seeds

def introduce_ocr_errors(lines, err_per):
   
    non_empty_lines = [(idx, line) for idx, line in enumerate(lines) if line.strip()]
    chosen_lines_idx = random.sample(non_empty_lines, int(err_per * len(non_empty_lines)))
    chosen_indices = {idx for idx, _ in chosen_lines_idx}

    print('Total number of words', len(non_empty_lines))
    print('Total nuumber of choosen words', len(chosen_lines_idx))
    
    aug = nac.OcrAug (aug_char_p=1.0)
    count_entity = []
    
    for idx, line in chosen_lines_idx:
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

# Introduce error to new word selected 
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
    
# Read file that needs modification
lines = read_file_content('train.txt')

# Different error rates for OCR Errors
err_per = [0.05, 0.10, 0.15, 0.20, 0.23]
for val in err_per:
    modified_lines = introduce_ocr_errors(lines, val)
    val = int(val * 100)
    write_modified_content(modified_lines, 'train_42_{}_ocr.txt'.format(val)) # Save file with new name indicating seed number, error percentage and error type 































'''def load_dataset(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    tokens, ner_tags = [], []
    sentence_tokens, sentence_tags = [], []

    for line in lines:
        line = line.strip()
        if line == '':
            if sentence_tokens:
                tokens.append(sentence_tokens)
                ner_tags.append(sentence_tags)
                sentence_tokens, sentence_tags = [], []
        else:
            word, tag = line.split()
            sentence_tokens.append(word)
            sentence_tags.append(tag)

    if sentence_tokens:
        tokens.append(sentence_tokens)
        ner_tags.append(sentence_tags)

    return {'tokens': tokens, 'ner_tags': ner_tags}

def spelling_error_in_data(dataset, seed_value=None):

    if seed_value is not None:
        random.seed(seed_value)
        np.random.seed(seed_value)

    all_words = [word for sentence in dataset['tokens'] for word in sentence]

    total_words = len(all_words)
    words_to_modify = int(0.22 * total_words)

    indices_to_modify = random.sample(range(total_words), words_to_modify)

    aug = nac.OcrAug (aug_char_p=1.0)

    for idx in indices_to_modify:
        augmented_word = aug.augment(all_words[idx])
        augmented_word = augmented_word[0] if isinstance(augmented_word, list) else augmented_word
        augmented_word = augmented_word.replace(" ", "")  # Remove spaces
        all_words[idx] = augmented_word

    reconstructed_sentences = []
    word_counter = 0
    for sentence in dataset['tokens']:
        sentence_length = len(sentence)
        reconstructed_sentences.append(all_words[word_counter:word_counter + sentence_length])
        word_counter += sentence_length

    print("Total number of words:", total_words)
    print("Total number of words modified:", words_to_modify)

    return {'tokens': reconstructed_sentences, 'tags': dataset['ner_tags']}

# Load and augment the dataset
dataset = load_dataset('/mnt/data/dibhad/conll_2003_datasets/train.txt')
augmented_data = spelling_error_in_data(dataset, seed_value=42)

def write_to_conll_format(dataset, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for tokens, tags in zip(dataset['tokens'], dataset['tags']):
            for token, tag in zip(tokens, tags):
                f.write(f"{token} {tag}\n")
            f.write("\n")  # Separate sentences by newline

write_to_conll_format(augmented_data,'/mnt/data/dibhad/conll_2003_datasets/ds4_22_OCR.txt')

'''
