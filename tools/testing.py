def assert_values(v1, v2, text):
    try:
        assert v1 == v2
        print('%50s: %10s' % (text, "OK"))
        return True
    except AssertionError:
        print('%50s: %10s' % (text, "ERROR"))
        return False
        
