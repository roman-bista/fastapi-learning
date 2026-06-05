def test_equall_or_not_equall():
    assert 3 == 3
    assert 3!=1

def test_is_instance():
    # isinstance(object, type)
    assert isinstance('this is a sttring', str)
    assert not isinstance('10', int)

# def test_boolean():
#     validated = True
#     assert validated is True
#     assert ('hello'=='world') is False

def test_boolean():
    validated = True

    assert validated
    assert 'hello' != 'world'

def test_type():
    assert type('hello') is str
    assert type(10) is int

def test_greater():
    assert 3<5

def test_list():
    num_lis=[2,1,23,4,5]
    any_list= [False,False]
    assert 1 in num_lis
    assert 2 in num_lis
    assert all(num_lis)
    assert not any(any_list)