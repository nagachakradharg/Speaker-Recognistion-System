import pytest
import itertools
from hashtable import Hashtable


@pytest.mark.parametrize(
    "key,hval",
    [
        ("one", 156130),
        ("two", 163318),
        ("three", 222830492),
        ("four", 5323008),
    ],
)
def test_hash_function(key, hval):
    h = Hashtable(10, 0, 0.5, 2)
    assert h._hash(key) == hval


def test_hashtable_init():
    h = Hashtable(10, 0, 0.5, 2)
    assert len(h._items) == 10

    h = Hashtable(27, None, 0.4, 3)
    assert len(h._items) == 27


def test_hashtable_get_default():
    h = Hashtable(10, 7, 0.5, 2)
    assert h["test"] == 7


def test_hashtable_set_then_get():
    h = Hashtable(10, 7, 0.5, 2)
    h["test"] = 5
    assert h["test"] == 5


def test_hashtable_set_then_get_overwrite():
    h = Hashtable(10, 7, 0.5, 2)
    h["test"] = 5
    assert h["test"] == 5
    h["test"] = 9
    assert h["test"] == 9


def test_hashtable_delete():
    h = Hashtable(10, 7, 0.5, 2)
    h["test"] = 5
    assert h.pop("test") == 5
    assert h["test"] == 7


def test_hashtable_len_simple():
    h = Hashtable(10, 0, 0.5, 2)
    h["one"] = 1
    assert len(h) == 1
    h["two"] = 2
    assert len(h) == 2


def test_hashtable_len_overwrite():
    h = Hashtable(10, 0, 0.5, 2)
    h["one"] = 1
    assert len(h) == 1
    h["one"] = "one"
    assert len(h) == 1


def test_hashtable_len_delete():
    h = Hashtable(10, 0, 0.5, 2)
    h["one"] = 1
    h["two"] = 2
    del h["one"]
    assert len(h) == 1
    del h["two"]
    assert len(h) == 0


def test_hashtable_delete_keyerror():
    h = Hashtable(10, 0, 0.5, 2)
    with pytest.raises(KeyError):
        del h["one"]


def test_hashtable_delete_keyerror_on_second_delete():
    h = Hashtable(10, 0, 0.5, 2)
    h["one"] = "one"
    del h["one"]
    with pytest.raises(KeyError):
        del h["one"]
    assert len(h) == 0


def test_hashtable_collision_insert():
    h = Hashtable(10, 0, 0.5, 2)
    # "two" and "four" will collide in a hashtable with size 10
    assert h._hash("two") % 10 == h._hash("four") % 10
    h["two"] = 2
    h["four"] = 4
    assert h["two"] == 2
    assert h["four"] == 4


def test_hashtable_collision_insert_len():
    h = Hashtable(10, 0, 0.5, 2)
    # "two" and "four" will collide in a hashtable with size 10
    assert h._hash("two") % 10 == h._hash("four") % 10
    h["two"] = 2
    h["four"] = 4
    assert len(h) == 2


def test_hashtable_collision_then_delete():
    h = Hashtable(10, 0, 0.5, 2)
    # "two" and "four" will collide in a hashtable with size 10
    assert h._hash("two") % 10 == h._hash("four") % 10
    h["two"] = 2
    h["four"] = 4
    del h["two"]
    assert h["two"] == 0
    assert len(h) == 1

    del h["four"]
    assert h["four"] == 0
    assert len(h) == 0


def test_hashtable_three_chain():
    # this example tests the chaining behavior of the hashtable
    # c-h-m all hash to the same value at the end of the list
    # NOTE: this test should pass regardless of algorithm used
    h = Hashtable(5, 0, 0.9, 2)
    # all three hash to same value
    assert h._hash("c") % 5 == h._hash("h") % 5 == h._hash("m") % 5
    h["c"] = 1
    h["h"] = 2
    h["m"] = 3
    assert h["c"] == 1
    assert h["h"] == 2
    assert h["m"] == 3


def test_hashtable_three_chain_with_deletes():
    # this example tests that the chain is maintained after a delete
    h = Hashtable(5, 0, 0.9, 2)
    h["c"] = 1
    h["h"] = 2
    h["m"] = 3
    assert h["c"] == 1
    del h["c"]
    assert h["h"] == 2
    del h["h"]
    assert h["m"] == 3


def test_hashtable_three_chain_with_deletes_middle_first():
    # this example tests that the chain is maintained after a delete from the middle of the chain
    h = Hashtable(5, 0, 0.9, 2)
    h["c"] = 1
    h["h"] = 2
    h["m"] = 3
    del h["h"]  # delete the middle of the chain
    assert h["m"] == 3  # ensure m and c are intact
    assert h["c"] == 1


def test_hashtable_grow_and_rebalance():
    h = Hashtable(5, 0, 0.5, 2)
    for ll in "abc":
        h[ll] = ll
    assert len(h) == 3
    assert len(h._items) == 10
    for ll in "def":
        h[ll] = ll
    assert len(h) == 6
    assert len(h._items) == 20
    for ll in "ghijk":
        h[ll] = ll
    assert len(h) == 11
    assert len(h._items) == 40
    for ll in "abcdefghijk":
        assert h[ll] == ll


def test_hashtable_grow_and_rebalance_params():
    h = Hashtable(20, 0, 0.1, 5)
    for ll in "abc":
        h[ll] = ll
    assert len(h) == 3
    assert len(h._items) == 100


def test_big_hashtable():
    h = Hashtable(1000, -1, 0.5, 2)
    characters = "abcABC1"
    perms = list(enumerate(itertools.permutations(characters)))
    for idx, perm in perms:
        h[perm] = idx

    assert len(h) == len(perms)
    for idx, perm in perms:
        assert h[perm] == idx


# def test_hashtable_iter():
#     h = Hashtable(100, 0, 0.5, 2)
#     alphabet = "abcdefghijklmnopqrstuvwxyz"
#     for ll in alphabet:
#         h[ll] = ll
#     assert set(h.keys()) == set(alphabet)
#     assert set(h.items()) == set(zip(alphabet, alphabet))
