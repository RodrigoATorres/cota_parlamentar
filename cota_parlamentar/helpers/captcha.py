# from python_anticaptcha import AnticaptchaClient, ImageToTextTask, NoCaptchaTaskProxylessTask
from python3_anticaptcha.NoCaptchaTaskProxyless import NoCaptchaTaskProxyless

import os
import time

def imageCaptchaSolver(image_path):
    captcha_fp = open(image_path, 'rb')
    client = AnticaptchaClient(os.getenv("ANTI_CAPTCH_API_KEY"))
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    captcha_text = job.get_captcha_text()
    return captcha_text

def reCaptchaSolver(url, site_key, driver):

    captcha_obj = NoCaptchaTaskProxyless(anticaptcha_key=os.getenv("ANTI_CAPTCH_API_KEY"))
    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")

    recaptcha_element = driver.find_element_by_xpath('//*[@id="g-recaptcha-response"]')
    recaptcha_element.click()
    recaptcha_element.clear()
    # get captcha solution
    captcha_result = captcha_obj.captcha_handler(websiteURL=url, websiteKey=site_key)
    
    if captcha_result['errorId']>0:
        return False

    print(captcha_result)
    # insert captcha solution
    recaptcha_element.send_keys(captcha_result["solution"]["gRecaptchaResponse"])
    # wait success insertion
    time.sleep(2)

    return True

def form_submit(driver, token):
    driver.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML='{}';".format(token)
    )
    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTLM="{}";'.format(token))
    time.sleep(1)


# import requests
# import os
# import base64
 
# def get_base64_encoded_image(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode('utf-8')

# def imageCaptchaSolver(image_path):
#     image64 = get_base64_encoded_image(image_path)
    
#     r = requests.post(
#         'https://api.capmonster.cloud/createTask',
#         json = {
#             "clientKey":"4b09560fde218b7545a7a043089532df",
#             "task":
#             {
#                 "type":"ImageToTextTask",
#                 "body":image64
#             }
#         }
#     ).json()

#     print(r)

#     sol = {"status": "wait"}
#     while sol["status"]!= "ready":
#         sol = requests.post(
#             "https://api.capmonster.cloud/getTaskResult/",
#             json = {
#                 "clientKey":"4b09560fde218b7545a7a043089532df",
#                 "taskId": r["taskId"]
#             }
#         ).json()
#         print(sol)

#     captcha_text = sol["solution"]["text"]
#     print(captcha_text)
#     return captcha_text