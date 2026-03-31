import secrets, string


def generate_random_letters(length: int) -> str:
    return "".join(secrets.choice(string.ascii_lowercase) for _ in range(length))


from wonderwords import RandomWord, RandomSentence


r = RandomWord()

def generate_mock_word(length: int) -> str:
    return r.word(word_min_length=length, word_max_length=length).lower()


s = RandomSentence()

def generate_mock_sentence() -> str:
    return "".join(char for char in s.sentence().lower() if char.isalpha())


def generate_random_word_text(length: int) -> str:
    sentence = []
    counter = 0
    while counter < length:
        if length - counter < 3:
            counter -= len(sentence.pop(-1))
            word = r.word(word_min_length=length - counter, word_max_length=length - counter)
            counter += len(word)
            sentence.append(word)
        else:
            word = r.word(word_max_length=min(15, length - counter))
            counter += len(word)
            sentence.append(word)
    return "".join(sentence).lower()


def generate_mock_text(sentence_count: int) -> str:
    return "".join(generate_mock_sentence() for _ in range(sentence_count))


def generate_random_text(length: int) -> str:
    return generate_random_letters(length)


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


key         = RSA.generate(2048)
private_key = key
public_key  = key.publickey()
rsa_cipher      = PKCS1_OAEP.new(public_key)


def generate_random_rsa_cipher_text_hex(sentence_count: int) -> str:
    text = generate_random_text(sentence_count)
    ciphertext_bytes = rsa_cipher.encrypt(text.encode())
    return str(ciphertext_bytes.hex())


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


key    = get_random_bytes(32)
nonce  = get_random_bytes(8)
aes_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)


def generate_random_aes_cipher_text_hex(sentence_count: int) -> str:
    text = generate_mock_text(sentence_count)
    return str(aes_cipher.encrypt(text.encode()).hex())


def compare_text_to_text(sentence_count: int, write: bool = False) -> float:
    text1 = generate_mock_text(sentence_count)
    text2 = generate_mock_text(sentence_count)

    # Выравнивание длины текста
    min_len = min(len(text1), len(text2))
    text1 = text1[:min_len]
    text2 = text2[:min_len]

    if write:
        print(f"text1: {text1}")
        print(f"text2: {text2}")

    return sum(text1[i] == text2[i] for i in range(len(text1))) / len(text1)


def run_single_text_comparison(sentence_count: int) -> tuple[int, float]:
    return sentence_count, compare_text_to_text(sentence_count)


def compare_text_to_random_letters(sentence_count: int, write: bool = False) -> float:
    text1 = generate_mock_text(sentence_count)
    text2 = generate_random_letters(len(text1))

    if write:
        print(f"text1: {text1}")
        print(f"text2: {text2}")

    return sum(text1[i] == text2[i] for i in range(len(text1))) / len(text1)


def run_single_text_to_random_letters_comparison(sentence_count: int) -> tuple[int, float]:
    return sentence_count, compare_text_to_random_letters(sentence_count)


def compare_text_to_random_word_text(sentence_count: int, write: bool = False) -> float:
    text1 = generate_mock_text(sentence_count)
    text2 = generate_random_word_text(len(text1))

    if write:
        print(f"text1: {text1}")
        print(f"text2: {text2}")

    return sum(text1[i] == text2[i] for i in range(len(text1))) / len(text1)


def run_single_text_to_random_word_text_comparison(sentence_count: int) -> tuple[int, float]:
    return sentence_count, compare_text_to_random_word_text(sentence_count)


def compare_random_text_to_random_text(letter_count: int, write: bool = False) -> float:
    text1 = generate_random_letters(letter_count)
    text2 = generate_random_letters(letter_count)

    if write:
        print(f"text1: {text1}")
        print(f"text2: {text2}")

    return sum(text1[i] == text2[i] for i in range(letter_count)) / letter_count


def run_single_random_text_comparison(letter_count: int) -> tuple[int, float]:
    return letter_count, compare_random_text_to_random_text(letter_count)


def compare_random_word_text_to_random_word_text(letter_count: int, write: bool = False) -> float:
    text1 = generate_random_word_text(letter_count)
    text2 = generate_random_word_text(letter_count)

    if write:
        print(f"text1: {text1}")
        print(f"text2: {text2}")

    return sum(text1[i] == text2[i] for i in range(letter_count)) / letter_count

def run_single_random_word_text_comparison(letter_count: int) -> tuple[int, float]:
    return letter_count, compare_random_word_text_to_random_word_text(letter_count)