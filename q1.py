def equalsWhenOneCharRemoved(str1, str2):
    if len(str1) == len(str2):
        return False
    if len(str1) - len(str2) > 1:
        return False

    long_str = str1 if len(str1) > len(str2) else str2
    short_str = str1 if len(str1) < len(str2) else str2

    for i, c in enumerate(long_str):
        if len(short_str) == i:
            return False
        if long_str[i] != short_str[i]:
            temp_long_str = long_str
            if i == 0:
                temp_long_str = temp_long_str[i:]
            else:
                temp_long_str = temp_long_str[:i-1] + temp_long_str[i:]
            if temp_long_str == short_str:
                return True

    return False


if __name__ == '__main__':
    # tests
    # case 1
    str1 = '{}{}{}{}'.format('a' * 6, 'b' * 5, 'c' * 4, 'd' * 3)
    str2 = '{}{}{}{}'.format('a' * 6, 'b' * 6, 'c' * 4, 'd' * 3)
    print(equalsWhenOneCharRemoved(str1, str2))

    # case 2
    str1 = '{}{}{}{}'.format('a' * 600000, 'b' * 500000, 'c' * 400000, 'd' * 300000)
    str2 = '{}{}{}{}'.format('a' * 600000, 'b' * 500001, 'c' * 400000, 'd' * 300000)
    print(equalsWhenOneCharRemoved(str1, str2))

    # case 3
    str1 = '{}{}{}{}'.format('a' * 600000, 'b' * 500000, 'c' * 400002, 'd' * 300000)
    str2 = '{}{}{}{}'.format('a' * 600000, 'b' * 500000, 'c' * 400000, 'd' * 300000)
    print(equalsWhenOneCharRemoved(str1, str2))

