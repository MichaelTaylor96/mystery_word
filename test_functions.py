from demoner_words import split_pool

def test_split_pool():
    word_pool = ['funday', 'excite', 'mushro', 'axolot']
    guess = 'a'
    sub_pool = split_pool(word_pool, guess)
    assert sub_pool == ['excite', 'mushro']
    