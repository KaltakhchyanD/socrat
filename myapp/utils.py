from functools import wraps


class URLShortener:
    """
    ShortURL: Bijective conversion between natural numbers (IDs) and short strings
    ShortURL.encode() takes an ID and turns it into a short string
    ShortURL.decode() takes a short string and turns it into an ID
    Features:
    + large alphabet (51 chars) and thus very short resulting strings
    + proof against offensive words (removed 'a', 'e', 'i', 'o' and 'u')
    + unambiguous (removed 'I', 'l', '1', 'O' and '0')
    Example output:
    123456789 <=> pgK8p
    """

    _alphabet = "23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_"
    _base = len(_alphabet)

    def encode(self, number):
        string = ""
        while number > 0:
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number


def admin_required(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            print(f"Error referer - {request.referrer}")
            flash("You are not an admin!")
            return redirect(url_for(request.referrer or "index"))

    return inner_func
