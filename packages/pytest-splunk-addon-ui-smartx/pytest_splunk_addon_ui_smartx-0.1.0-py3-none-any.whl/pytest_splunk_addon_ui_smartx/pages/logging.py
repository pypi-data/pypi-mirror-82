# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ..components.base_component import Selector
from ..components.tabs import Tab
from ..components.entity import Entity
from ..components.controls.single_select import SingleSelect
from ..backend_confs import SingleBackendConf
from selenium.webdriver.common.by import By
import time


class Logging(Entity):

    def __init__(self, ucc_smartx_configs, ta_name, ta_conf=""):
        """
            :param ucc_smartx_configs: Fixture with selenium driver, urls(web, mgmt) and session key
            :param ta_name: Name of TA
            :param ta_conf: Name of conf file
        """
        entity_container = Selector(select= "#logging-tab")
        super(Logging, self).__init__(ucc_smartx_configs.browser, entity_container)
        self.splunk_web_url = ucc_smartx_configs.splunk_web_url
        self.splunk_mgmt_url = ucc_smartx_configs.splunk_mgmt_url
        self.ta_name = ta_name
        self.ta_conf = ta_conf
        if self.ta_conf == "":
            self.ta_conf = "{}_settings".format(self.ta_name.lower())
        self.open()

        # Components
        self.log_level = SingleSelect(
            ucc_smartx_configs.browser, Selector(select=".loglevel"))
        self.backend_conf = SingleBackendConf(
            self._get_logging_url(), ucc_smartx_configs.session_key)

    def open(self):
        """
        Open the required page. Page(super) class opens the page by default.
        """
        self.browser.get(
            '{}/en-US/app/{}/configuration'.format(self.splunk_web_url, self.ta_name))
        tab = Tab(self.browser)
        tab.open_tab("logging")

    def _get_logging_url(self):
        """
        get rest endpoint for the configuration
        """
        return '{}/servicesNS/nobody/{}/configs/conf-{}/logging'.format(self.splunk_mgmt_url, self.ta_name, self.ta_conf)
