class TestPhrase():
    def test_phrase_check(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "Phrase has more tahn 15 symbols in it"
        