import os
import unittest
from base_test import BaseTest
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy


class BitbarBiometricsIOS(BaseTest):
    def setUp(self):
        super().setUp()
        bitbar_project_name = (
            os.environ.get("BITBAR_PROJECT") or "iOS biometrics sample project"
        )
        automation_name = os.environ.get("BITBAR_AUTOMATION_NAME") or "XCUITest"
        if self.bitbar_device == "":
            self._find_device("iOS")

        self.desired_capabilities_cloud["bitbar_project"] = bitbar_project_name
        self.desired_capabilities_cloud["bitbar_device"] = self.bitbar_device
        self.desired_capabilities_cloud["platformName"] = "iOS"
        self.desired_capabilities_cloud["deviceName"] = "iPhone device"
        self.desired_capabilities_cloud["bitbar_target"] = "ios"
        self.desired_capabilities_cloud["automationName"] = automation_name
        self.desired_capabilities_cloud["bitbar_biometricInstrumentation"] = True

    def test_sample(self):
        super()._start_webdriver()
        self.driver.implicitly_wait(2)
        self.driver.execute_script("mobile: alert", {"action": "accept"})
        self.utils.screenshot("start_screen")

        button = self.driver.find_element(
            By.XPATH, '(//*[@name="Biometric authentication"])[3]'
        )
        self.utils.log("view1: Clicking button - BIOMETRIC AUTHENTICATION")
        button.click()
        self.utils.screenshot("second_screen")

        element = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "Sensor type value"
        )
        assert element.text == ("TOUCHID" or "FACEID"), self.utils.log(
            "view2: Error in biometry injection"
        )
        self.utils.log("view2: Biometry injected properly")

        button = self.driver.find_element(
            By.XPATH,
            '//XCUIElementTypeOther[@name="Ask biometric authentication"]',
        )
        button.click()
        self.utils.log("view2: Accepting biometry prompt")
        self.utils.screenshot("authentication_prompt")

        self.driver.execute_script(
            "mobile: alert", {"action": "accept", "buttonLabel": "Pass"}
        )
        element = self.driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "Authentication status value"
        )
        assert element.text == "SUCCEEDED"
        self.utils.log("view2: Test passed")
        self.utils.screenshot("biometry_checked")


def initialize():
    return BitbarBiometricsIOS


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(BitbarBiometricsIOS)
    unittest.TextTestRunner(verbosity=2).run(suite)
