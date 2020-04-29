from hamcrest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from helpers.driver_extended import DriverExtended


class TestGuerrilla:
    SUBJECT = "some subject"
    BODY = "some message body"
    REPLY_BODY = "some reply body"

    def test_email_creation_and_response(self, get_driver_factory, get_config):
        url = get_config["urls"]["url"]
        driver1 = get_driver_factory.create_driver(url)
        driver2 = get_driver_factory.create_driver(url)
        driver1 = DriverExtended(driver1)
        driver2 = DriverExtended(driver2)

        driver1.driver.implicitly_wait(2)
        driver2.driver.implicitly_wait(2)

        driver1.read_and_unscramble_email()
        driver2.read_and_unscramble_email()

        # send message as driver1
        driver1.go_to_send()
        driver1.fill_recipient(driver2.email_address_unscrambled)
        driver1.fill_subject(self.SUBJECT)
        driver1.fill_body(self.BODY)
        driver1.click_send()

        # read message as driver2
        driver2.go_to_inbox()
        driver2.click_email_by_subject(self.SUBJECT)

        subject_text = driver2.wait_and_find_by_xpath('//h3[@class="email_subject"]').text
        assert_that(subject_text, equal_to(self.SUBJECT))
        sender = driver2.wait_and_find_by_xpath('//strong[@class="email_from"]').text
        assert_that(sender, is_in(
            [driver1.user_name_scrambled + "@sharklasers.com", driver1.user_name_scrambled + "@guerrillamail.com"]))
        body = driver2.wait_and_find_by_xpath('//div[@class="email_body"]').text
        assert_that(body, contains_string(self.BODY))

        # reply message as driver2
        driver2.click_reply()
        driver2.fill_body(Keys.PAGE_UP)
        driver2.fill_body(self.REPLY_BODY)
        driver2.wait.until(ec.invisibility_of_element_located((By.XPATH, '//div[@class="status_alert shadow"]')))
        driver2.click_send()

        # read reply as driver 1
        driver1.go_to_inbox()
        driver1.click_email_by_subject("Re: " + self.SUBJECT)
        subject_text = driver1.wait_and_find_by_xpath('//h3[@class="email_subject"]').text
        assert_that(subject_text, equal_to("Re: " + self.SUBJECT))
        sender = driver1.wait_and_find_by_xpath('//strong[@class="email_from"]').text
        assert_that(sender, is_in(
            [driver2.user_name_scrambled + "@sharklasers.com", driver2.user_name_scrambled + "@guerrillamail.com"]))
        body = driver1.wait_and_find_by_xpath('//div[@class="email_body"]').text
        assert_that(body, contains_string(self.REPLY_BODY))
