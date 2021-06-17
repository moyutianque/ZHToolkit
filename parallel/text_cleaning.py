"""
Test filtered text quality
"""

import re
import os
import os.path as osp
import json
from bs4 import BeautifulSoup
import string
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import sys
import yaml

from urllib.parse import urlparse
from urllib.parse import quote, unquote
import multiprocessing as mp

# NOTE: timeout handler
import time
import signal
def handler(signum, frame):
    raise Exception('TIMEOUT Handler raise!')
signal.signal(signal.SIGALRM, handler)


import unicodedata
combined_file = None
config = None

# function to remove accented characters
def remove_accented_chars(text):
    new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text

CONTRACTION_MAP = {
"İt's": "It is",
"It's": "It is",
"it's": "it is",
"ı'm":"I am",
"ı'd":"I would",
"İ'd":"I would",

"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

# function to expand contractions
def expand_contractions(text, map=CONTRACTION_MAP):
    if text is None or text.strip()=='':
        return ''
    
    pattern = re.compile('({})'.format('|'.join(map.keys())), flags=re.IGNORECASE|re.DOTALL)
    def get_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded = map.get(match) if map.get(match) else map.get(match.lower())
        if expanded is None:
            logger.info('Warning for text: {}'.format(match))
            return match
        expanded = first_char+expanded[1:]
        return expanded 
    new_text = pattern.sub(get_match, text)
    new_text = re.sub("'", "", new_text)
    return new_text


import nltk
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')


def clean_raw(sent):
    # step 1
    # remove html tags, and urls
    sent = re.sub(r'<a href=.*?\s?(.*?)</a>', '', sent)
    sent = BeautifulSoup(sent, 'html.parser').get_text()
    #sent = re.sub(r'\bhttps?:\/\/.*[\r\n]*\b', '', sent)
    sent = re.sub(r"\b(\w*\.)+\w*\b", '', sent)
    sent = re.sub(r"https?:\/\/", "", sent)
    sent = sent.replace("_", " ")
    sent = sent.replace("/", " ")
    
    def letter_ratio(sent):
        numbers = sum(c.isdigit() for c in sent[:1000])
        letters = sum(c.isalpha() for c in sent[:1000])
        return letters/(numbers+1e-3)
    
    if letter_ratio(sent) < 1:
        return None
 
    # Remove pure digit token
    sent = re.sub(r'\b\d+\b', '', sent)

    # Remove accented chars (fr, de...)
    sent = remove_accented_chars(sent)

    # Handle contractions
    sent = expand_contractions(sent)
   
    # remove puncs
    sent = re.sub(r'[^\w\s.,-]','',sent)
 
    # replace pattern \s\.\s to '. '
    sent = re.sub(r'\s+\.\s*', '. ', sent)
    sent = re.sub(r'\s+,\s*', ', ', sent)
    sent = re.sub(r'[,\.]\s+', ' ', sent)

    # replace \n or \t ... as space
    sent = re.sub(r'^\s*|\s\s*', ' ', sent)

    sent = sent.strip()
    if sent != '':
        tmp_split = sent.split()
        if len(tmp_split)>200:
            sent = " ".join(tmp_split[:200])
        return sent
    else:
        return None

def word_check(sent, threshold = 1.):
    # step 2
    tokens = tokenizer.tokenize(sent)
    # Remove this condition, dataset size will grow from 12.7M to 17M 
    if len(tokens)<2 or len(sent.split()) < 2:
        return False

    cnt = 0    
    for token in tokens:
        token = token.lower()
        if token in english_vocab:
            if len(token) == 1 and token != 'a':
                continue
            cnt += 1

    if cnt/len(tokens) < threshold:
        return False

    return True


def cleaner_pipline(sent):
    # Hard constraint used in CC3M
    mask = [False, False, False]
    sent_processed = clean_raw(sent)
    if sent_processed is not None:
        if word_check(sent_processed, config.threshold):
            mask = [True, True, False]
        else:
            mask = [True, False, False]   
    else:
        mask = [False, False, False]
    return sent_processed, mask


# Main funcs
def process_step(x):
    title = unquote(x.split("\t")[6]).replace("+"," ")
    desc = unquote(x.split("\t")[7]).replace("+", " ")
    user_tags = unquote(x.split("\t")[8]).replace("+", " ")
    url = x.split("\t")[14]
    url_path = urlparse(url).path[1:]
    if "video" in url_path:
        return None, [False, False, False]   

    if config.desc:
        sent, mask = cleaner_pipline(title.strip() + '. ' + desc.strip())
    else:
        sent, mask = cleaner_pipline(title.strip())
    
    if sent is not None:
        return url_path+"^"+sent+"\n", mask
    return None, [False, False, False]   


def worker(sub_list, filepath, out):
    flist = dict()
    for name in out:
        flist[name] = open(filepath+'-'+str(name), 'w')

    for row in sub_list:
        try:
            signal.alarm(5)
            sent, mask = process_step(row)

            for i in range(len(mask)):
                if sent is not None and mask[i]:
                    flist[i].write(sent)
                    flist[i].flush()

        except Exception as exc:
            print(exc)
            title = unquote(row.split("\t")[6]).replace("+"," ")
            desc = unquote(row.split("\t")[7]).replace("+", " ")
            print((title + desc).replace("\n", " "))
            print('='*20)
            print('\n')
            continue
    
    for name in out:
        flist[name].close()

    return 0

def parse_yfcc_dataset_partitaion(split, filename, partition, out = [0, 1, 2]):
    path = f'../../data/yfcc_root/yfcc100m_dataset-{split}'
    filename = filename+f"/combined-{split}"

    #must use Manager queue here, or will not work
    process_pool = mp.Pool(partition)

    jobs = []
    with open(path) as f:
        lines = f.readlines()
        print(f"Start processing {split}")
        for i in range(partition):
            file_path = f"{filename}-{i}"
            jobs.append(process_pool.apply_async(
                worker, (lines[i::partition], file_path, out)
            )) 

    process_pool.close() # No more tasks
    process_pool.join() # Wait for all finished

    for job in jobs:
        job.get()

    for name in out:
        outfile = filename+'-step'+str(name)
        with open(outfile, 'w') as outf:
            for i in range(partition):
                tmp_file = f"{filename}-{i}"+'-'+str(name)
                with open(tmp_file, 'r') as f:
                    for row in f:
                        outf.write(row)
                os.remove(tmp_file)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='YFCC parsing')
    parser.add_argument('--num', default=0, type=int)
    parser.add_argument('--config', default="./config_speedup.yaml", type=str)
    args = parser.parse_args()

    from easydict import EasyDict
    config = yaml.load(open(args.config), Loader=yaml.FullLoader)
    config = EasyDict(config)
    
    out_path = f"{config.combined_out}/v{config.threshold}"
    print(f"Writing to directory {out_path}") 
    os.makedirs(out_path, exist_ok=True)
    parse_yfcc_dataset_partitaion(args.num, out_path, partition=config.writePool)
    print("Finish processing")
