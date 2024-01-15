'''

Zephyr AutoDocumentation for ProgMasters
Authors: Adorján Mészáros, Ádám Farkas
14.01.2024

Username, password, URL, Jira board name should be in a login_details.json file in the same directory in the following format:

{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "user": {
      "type": "string"
    },
    "password": {
      "type": "string"
    },
    "url": {
      "type": "string"
    },
    "jira_board": {
      "type": "string"
    }
  },
  "required": [
    "user",
    "password",
    "url",
    "jira_board"
  ]
}

Place the documentation files into ./documentation folder. Documentation should have the following JSON format:

{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "folder": {
      "type": "string"
    },
    "testCases": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "objective": {
              "type": "string"
            },
            "precondition": {
              "type": "string"
            },
            "folder": {
              "type": "string"
            },
            "priority": {
              "type": "string"
            },
            "testSteps": {
              "type": "array",
              "items": [
                {
                  "type": "object",
                  "properties": {
                    "testStep": {
                      "type": "string"
                    },
                    "testData": {
                      "type": "string"
                    },
                    "expectedResult": {
                      "type": "string"
                    },
                    "status": {
                      "type": "string"
                      "enum": ["pass", "fail", "blocked"]
                    }
                  },
                  "required": [
                    "testStep",
                    "testData",
                    "expectedResult",
                    "status"
                  ]
                }
              ]
            }
          },
          "required": [
            "name",
            "objective",
            "precondition",
            "folder",
            "priority",
            "testSteps"
          ]
        }
      ]
    }
  },
  "required": [
    "name",
    "description",
    "folder",
    "testCases"
  ]
}

'''
import json
import os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

path = os.getcwd()
print(path)
documentation_path = os.path.join(path, "documentation")
print(documentation_path)
file_lista = os.listdir(documentation_path)
print(file_lista)

test_cycles = []

login_details = {}

for current_file in file_lista:
    file_path = os.path.join(documentation_path, current_file)
    print(file_path)

    with open(file_path, "r", encoding="UTF-8") as json_file:
        test_cycles.append(json.loads(json_file.read()))

with open("login_details.json", "r", encoding="UTF-8") as login_details_file:
    login_details = json.loads(login_details_file.read())

options = ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

URL = login_details["url"]
driver.get(URL)

user_input = driver.find_element(By.ID, 'login-form-username')
password_input = driver.find_element(By.ID, 'login-form-password')
login_btn = driver.find_element(By.ID, 'login')

user_input.send_keys(login_details["user"])
password_input.send_keys(login_details["password"])
login_btn.click()

board_name = login_details["jira_board"]

for test_cycle in test_cycles:

    for test_case in test_cycle["testCases"]:

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ktm_top_menu'))).click()

        project_selection_menu_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span/div/span[@role="presentation"]/..')))
        project_selection_menu_btn.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[@data-testid="{board_name}"]'))).click()

        new_test_case_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="New Test Case"]')))
        new_test_case_btn.click()

        tc_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'name')))
        tc_name_input.click()
        tc_name_input.send_keys(test_case["name"])

        tc_objective_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'objective')))
        tc_objective_input.click()
        tc_objective = driver.find_element(By.XPATH, '//rich-text[@name="objective"]//div[@contenteditable="true"]')
        tc_objective.send_keys(test_case["objective"])

        tc_precondition_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'precondition')))
        tc_precondition_input.click()
        tc_precondition = driver.find_element(By.XPATH,
                                              '//rich-text[@name="precondition"]//div[@contenteditable="true"]')
        tc_precondition.send_keys(test_case["precondition"])

        folder_dropdown = driver.find_element(By.ID, 'select-box-4-button')
        folder_dropdown.click()

        folder_name = test_case["folder"]

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//a[@title="{folder_name}"]'))).click()

        priority_dropdown = driver.find_element(By.ID, 'select-box-2-button')
        priority_dropdown.click()

        priority_class = test_case["priority"]

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@title="{priority_class}"]'))).click()

        test_script_btn = driver.find_element(By.XPATH, '//span[text()="Test Script"]')
        test_script_btn.click()

        for index, step in enumerate(test_case["testSteps"]):
            ts_step_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, f'stepDescription-{index + 1}')))
            ts_step_input.click()
            ts_step = driver.find_element(By.XPATH,
                                          f'//rich-text[@name="stepDescription-{index + 1}"]//div[@contenteditable="true"]')
            ts_step.send_keys(step["testStep"])

            ts_data_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, f'stepTestData-{index + 1}')))
            ts_data_input.click()
            ts_data = driver.find_element(By.XPATH,
                                          f'//rich-text[@name="stepTestData-{index + 1}"]//div[@contenteditable="true"]')
            ts_data.send_keys(step["testData"])

            ts_expectedResult_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, f'stepExpectedResult-{index + 1}')))
            ts_expectedResult_input.click()
            ts_expectedResult = driver.find_element(By.XPATH,
                                                    f'//rich-text[@name="stepExpectedResult-{index + 1}"]//div[@contenteditable="true"]')
            ts_expectedResult.send_keys(step["expectedResult"])

            add_step_btns = driver.find_elements(By.XPATH, '//button[text()="Add step"]')
            add_step_btns[-1].click()

        ts_expectedResult_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, f'stepExpectedResult-{len(test_case["testSteps"]) + 1}')))
        ts_expectedResult_input.click()
        ts_expectedResult = driver.find_element(By.XPATH,
                                                f'//rich-text[@name="stepExpectedResult-{len(test_case["testSteps"]) + 1}"]//div[@contenteditable="true"]')
        ts_expectedResult.send_keys(step["expectedResult"])

        delete_step_btns = driver.find_elements(By.XPATH, '//button[text()="Delete"]')
        delete_step_btns[-1].click()

        save_tc_btn = driver.find_element(By.XPATH, '//button[@ng-click="submitForm()"]')
        save_tc_btn.click()

        tc_id = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@ng-if="entity.id"]/a'))).text
        test_case["id"] = tc_id.split(" ")[0]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ktm_top_menu'))).click()

    project_selection_menu_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span/div/span[@role="presentation"]/..')))
    project_selection_menu_btn.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//li[@data-testid="{board_name}"]'))).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="zscale-testcycle-library"]'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="New Test Cycle"]'))).click()

    tc_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'name')))
    tc_name_input.click()
    tc_name_input.send_keys(test_cycle["name"])

    tc_objective_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'description')))
    tc_objective_input.click()
    tc_objective = driver.find_element(By.XPATH, '//rich-text[@name="description"]//div[@contenteditable="true"]')
    tc_objective.send_keys(test_cycle["description"])

    folder_dropdown = driver.find_element(By.ID, 'select-box-0-button')
    folder_dropdown.click()

    folder_name = test_cycle["folder"]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//a[@title="{folder_name}"]'))).click()

    test_cases_btn = driver.find_element(By.XPATH, '//span[contains(text(), "Test Cases")]')
    test_cases_btn.click()

    for test_case in test_cycle["testCases"]:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Add test cases")]'))).click()

        project_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="project-picker"]')))
        project_picker.click()
        project_picker_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="project-picker"]//input')))
        project_picker_input.send_keys(board_name)
        project_picker_input.send_keys(Keys.ENTER)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-testid="folder-name-with-count-root"]'))).click()

        current_id = test_case["id"]
        search_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'zephyr-scale-grid-search')))
        search_bar.clear()
        search_bar.send_keys(current_id)

        checkbox_xpath = f'//td/a[text()="{current_id}"]/../../td/input'

        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
        checkbox.click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Add (1)"]'))).click()

    save_tcycle_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@ng-click="submitForm()"]')))
    save_tcycle_btn.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Go to test player"]'))).click()

    for test_case in test_cycle["testCases"]:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f'//a[contains(text(), "{test_case["id"]}")]/../span/span/span'))).click()
        pass_btns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@ng-click="changeStatusTo(statusPass)"]')))
        fail_btns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@ng-click="changeStatusTo(statusFail)"]')))
        blocked_btns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@ng-click="changeStatusTo(statusBlocked)"]')))

        for index, test_step in enumerate(test_case["testSteps"]):
            driver.execute_script("arguments[0].scrollIntoView();", blocked_btns[index])
            if test_step["status"] == "pass":
                pass_btns[index].click()
            elif test_step["status"] == "fail":
                fail_btns[index].click()
            else:
                blocked_btns[index].click()
