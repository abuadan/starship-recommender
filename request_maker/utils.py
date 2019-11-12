"""

"""


def num_to_words(num, join=True):

    """
    words = {} convert an integer number into words
    :param num:
    :param join:
    :return:
    """
    units = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    teens = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
             'seventeen', 'eighteen', 'nineteen']
    tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
            'eighty', 'ninety']
    thousands = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion',
                 'quintillion', 'sextillion', 'septillion', 'octillion',
                 'nonillion', 'decillion', 'undecillion', 'duodecillion',
                 'tredecillion', 'quattuordecillion', 'sexdecillion',
                 'septendecillion', 'octodecillion', 'novemdecillion',
                 'vigintillion']
    words = []
    if num == 0:
        words.append('zero')
    else:
        num_str = '%d' % num
        num_str_len = len(num_str)
        groups = (num_str_len + 2) / 3
        print(groups)
        num_str = num_str.zfill(int(groups) * 3)
        for i in range(0, int(groups) * 3, 3):
            h, t, u = int(num_str[i]), int(num_str[i + 1]), int(num_str[i + 2])
            g = groups - (i / 3 + 1)
            if h >= 1:
                words.append(units[h])
                words.append('hundred')
            if t > 1:
                words.append(tens[t])
                if u >= 1:
                    words.append(units[u])
            elif t == 1:
                if u >= 1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            else:
                if u >= 1:
                    words.append(units[u])
            if (g >= 1) and ((h + t + u) > 0):
                words.append(thousands[int(g)] + ',')
    if join:
        return ' '.join(words)
    return words


if __name__ == "__main__":
    print(num_to_words(0o2))
    print(num_to_words(2121212))
