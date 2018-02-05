def apply_prefix(f):
    def wrapper(*args, **kwargs):
        name = f.__name__.lstrip('key_of_')
        key = '{}.{}'.format(name, f(*args, **kwargs))
        return key
    return wrapper


@apply_prefix
def key_of_vocabulary(word):
    return word


@apply_prefix
def key_of_relation(vocab_id, next_vocab_id):
    return '{}.{}'.format(vocab_id, next_vocab_id)


@apply_prefix
def key_of_vocabulary_queryset(prefix):
    return prefix


@apply_prefix
def key_of_phrase_queryset(word):
    return word
