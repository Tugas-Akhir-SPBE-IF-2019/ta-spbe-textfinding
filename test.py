def test(keyword):
    for key in keyword:
        print(key)
    return keyword

abc = ['a','c','d','e','f']
abc = test(abc)
print(abc)