from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, StackedEmbeddings, FlairEmbeddings
from flair.models import SequenceTagger
import torch
import os
from flair.trainers import ModelTrainer
from torch.optim.lr_scheduler import OneCycleLR
from typing import List

columns = {0: 'text', 1: 'ner'}

data_folder = 'Ontonotes_v5_Dataset/'

train_data = 'train_ontonotes_iob.txt'


corpus = ColumnCorpus(data_folder, columns, train_file=train_data,
                    dev_file='val_ontonotes_iob.txt',
                    test_file='test_ontonotes_iob.txt')

model_dir = '{}'.format(os.path.splitext(train_data)[0])

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

tag_type = 'ner'
label_dictionary = corpus.make_label_dictionary(label_type='ner')

embedding_types = [
    WordEmbeddings('crawl'),
    FlairEmbeddings('news-forward'),
    FlairEmbeddings('news-backward'),
]

embeddings = StackedEmbeddings(embeddings=embedding_types)

tagger = SequenceTagger(hidden_size=256,
                        embeddings=embeddings,
                        tag_dictionary=label_dictionary,
                        tag_type=tag_type)



trainer = ModelTrainer(tagger, corpus)

trainer.train(model_dir,
            train_with_dev=True,
            max_epochs=20)
