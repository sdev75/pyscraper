import random


class ScraperUtils:
    @staticmethod
    def text_to_rand_chunks(text):
        min = 2
        max = len(text)
        if min >= max:
            min = max
        rand = random.randrange(min, max-1)
        chunks = [text[i:i+rand] for i in range(0, max, rand)]
        for chunk in chunks:
            yield chunk
