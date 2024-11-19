from collections import defaultdict, Counter

def get_sorted_word(word):
    """Return the sorted characters of the word as a string."""
    return ''.join(sorted(word))

def calculate_total_frequency(words):
    """Calculate the total frequency of each character in the list of words."""
    total_freq = Counter()
    for word in words:
        total_freq.update(word)
    return total_freq

def main():

    input_words = input("Enter words separated by space: ").split()


    anagram_dict = defaultdict(list)


    for word in input_words:
        sorted_word = get_sorted_word(word)
        anagram_dict[sorted_word].append(word)


    ordered_anagram_dict = {}
    seen_anagram_groups = set()

    for word in input_words:
        sorted_word = get_sorted_word(word)
        if sorted_word not in seen_anagram_groups:
            seen_anagram_groups.add(sorted_word)
            ordered_anagram_dict[sorted_word] = anagram_dict[sorted_word]


    words_list = [word for group in ordered_anagram_dict.values() for word in group]
    print("words =", words_list)


    anagram_frequencies = {}

    for key, group in ordered_anagram_dict.items():
        anagram_frequencies[key] = calculate_total_frequency(group)


    max_freq_group = None
    max_freq = Counter()

    for group_key, freq in anagram_frequencies.items():
        if sum(freq.values()) > sum(max_freq.values()):
            max_freq = freq
            max_freq_group = group_key


    print("Anagram Dictionary")
    for key, value in ordered_anagram_dict.items():
        print(f"{key}: {value}")

    print(f"\nGroup with highest total character frequency: {max_freq_group}")
    print("Frequency:", dict(max_freq))

if __name__ == "__main__":
    main()
