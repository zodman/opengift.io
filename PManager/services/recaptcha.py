__author__ = 'gvammer'


def validate(code, skip_recaptcha=None):
    if skip_recaptcha:
        return True

    import requests, json
    from tracker import settings
    if hasattr(settings, 'CAPTCHA_DISABLED'):
        return True

    r = requests.post("https://www.google.com/recaptcha/api/siteverify",
                      data={
                          'secret': '6LdiPUIUAAAAABNMYT_2RZaxrsllqyTbIHwS5Kol',
                          'response': code
                      })
    r = json.loads(r.text)

    return True if r['success'] else False
