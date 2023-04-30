import time
import requests

class CaptchaMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    def process_response(self, request, response, spider):
        if 'captcha' in response.url:
            # solve the CAPTCHA and get the solution
            solution = self.solve_captcha(response.content)

            # resend the original request with the CAPTCHA solution
            request.meta['captcha_solution'] = solution
            return request

        return response

    def process_request(self, request, spider):
        if 'captcha_solution' in request.meta:
            # add the CAPTCHA solution to the request headers
            solution = request.meta['captcha_solution']
            request.headers['X-Captcha-Solution'] = solution

            # wait for a few seconds to allow the CAPTCHA solution to be verified
            time.sleep(5)

    def solve_captcha(self, image):
        # send the CAPTCHA image to the CAPTCHA-solving service and get the solution
        captcha_api_key = self.settings.get('CAPTCHA_API_KEY')
        captcha_api_url = self.settings.get('CAPTCHA_API_URL')
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {'key': captcha_api_key, 'method': 'base64', 'body': image}
        response = requests.post(captcha_api_url, headers=headers, data=data)
        solution = response.text.split('|')[0]

        return solution
