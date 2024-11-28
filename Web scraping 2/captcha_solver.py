import requests

def solve_captcha(api_key, image_path):
    # Send CAPTCHA image to 2Captcha API
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            "https://2captcha.com/in.php",
            files={'file': image_file},
            data={'key': api_key, 'method': 'post'}
        )
    captcha_id = response.text.split('|')[1]

    # Get CAPTCHA solution
    while True:
        result = requests.get(f"https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}")
        if 'CAPCHA_NOT_READY' in result.text:
            continue
        return result.text.split('|')[1]
