import requests
from collections import defaultdict
import matplotlib.pyplot as plt
from multiprocessing import Pool
import string
from functools import reduce
from concurrent.futures import ThreadPoolExecutor

def fetch_text_from_url(url):
    response = requests.get(url)
    return response.text

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def visualize_top_words (frequency_stat):
    words, counts = zip(*frequency_stat)
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10')
    plt.xticks(rotation=45)
    plt.show()

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_reduce(text):
    words = text.split()


    return 

def main(url):
    try:
        print(f"download file {url}...")
        text = fetch_text_from_url(url)
        
        words = remove_punctuation(text).split(" ")
        
        chunk_size = len(words) // 8  
        words_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        with ThreadPoolExecutor() as executor:
            mapped_values = list(executor.map(map_function, words))

        shuffled_values = shuffle_function(mapped_values)

        with ThreadPoolExecutor() as executor:
            reduced_values = list(executor.map(reduce_function, shuffled_values))
            
        top_words = sorted(dict(reduced_values).items(), key=lambda x: -x[1])[:10]
                
        visualize_top_words(top_words)
    except Exception as e:
        print(f"Error: {e}")

url = 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt'
main(url)
