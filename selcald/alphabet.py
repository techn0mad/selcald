class Alphabet:

    TONES = dict({'Alpha': 312.6,
                  'Bravo': 346.7,
                  'Charlie': 384.6,
                  'Delta': 426.6,
                  'Echo': 473.2,
                  'Foxtrot': 524.8,
                  'Golf': 582.1,
                  'Hotel': 645.7,
                  'Juliette': 716.1,
                  'Kilo': 794.3,
                  'Lima': 881.0,
                  'Mike': 977.2,
                  'Papa': 1083.9,
                  'Quebec': 1202.3,
                  'Romeo': 1333.5,
                  'Sierra': 1479.1, })

    def frequency(self, name='Alpha'):
        try:
            return Alphabet.TONES[name]
        except KeyError:
            for tone in Alphabet.TONES:
                if str(tone[0]).upper() == str(name).upper():
                    return Alphabet.TONES[tone]
            return None

    def tone(self, frequency=TONES['Alpha'], accuracy=0.02):
        for tone in Alphabet.TONES:
            if abs((frequency / Alphabet.TONES[tone]) - 1) <= accuracy:
                return tone
        return None


if __name__ == "__main__":
    x = Alphabet()
    print x.frequency()
    print x.frequency('Sierra')
    print x.frequency('Foobar')
    print x.frequency('H')

    print x.tone(312.6)
    print x.tone(1479.1)
    print x.tone(500.0)
    print x.tone(500.0, 0.05)
    print x.tone(714.7)
