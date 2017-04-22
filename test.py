import pytest

def test_this():
    assert 1
    
@pytest.mark.xfail
def test_fail():
    assert False
    
def test_pass_again():
    print ("Hey there")
    assert 1
    
def test_die():
    assert False