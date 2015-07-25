# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
from Tools import Tools
from tests.libs.General.SeleniumExt import SeleniumExt


class Projects:
    PROJECT_EDIT_LINK = "/project/edit/"
    PROJECT_EDIT_FORM_LOCATOR = "css=.profile-edit"
    PROJECT_NAME_LOCATOR = "name=name"
    PROJECT_DESC_LOCATOR = "name=description"
    PROJECT_IMG_LOCATOR = "name=image"
    PROJECT_NAME_PREFIX = "text_project_"
    PROJECT_OPT_PREFIX = "name="
    PROJECT_SAVE_BUTTON = u'Сохранить'
    PROJECT_SELECT_LOCATOR = "css=li.projects-list-select>.left>select"
    PROJECT_SELECT_WINDOW_SIZE = [300, 600]
    PROJECT_CHANGE_BUTTON_LOCATOR = "css=.js-openProjectList"
    PROJECT_DROPDOWN_LOCATOR = "xpath=/html/body/div[1]/div/div[2]/ul/li[2]/div/ul"
    PROJECT_POPUP_LOCATOR = "css=.js-projects"

    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')
        self.selenium_ext = SeleniumExt()

    def create_project(self, description="This is default project description",
                       picture=None, options=None):
        if picture is None:
            picture = Tools.default_picture()
        if not options:
            options = []
        project_name = str(self.PROJECT_NAME_PREFIX + str(datetime.now()))[::-1]
        self.sel.click_link(self.PROJECT_EDIT_LINK)
        self.sel.wait_until_element_is_visible(self.PROJECT_EDIT_FORM_LOCATOR)
        self.sel.input_text(self.PROJECT_NAME_LOCATOR, project_name)
        self.selenium_ext.input_textarea(self.PROJECT_DESC_LOCATOR, description)
        self.sel.choose_file(self.PROJECT_IMG_LOCATOR, picture)
        for name in options:
            self.sel.select_checkbox(self.PROJECT_OPT_PREFIX + name)
        self.sel.click_button(self.PROJECT_SAVE_BUTTON)
        self.sel.page_should_contain(project_name)
        # todo: add log -- project id
        return project_name

    def select_project_from_select(self, project_name):
        self.sel.select_from_list_by_label(self.PROJECT_SELECT_LOCATOR, project_name)

    def select_project(self, project_name, fr="select"):
        if fr == "select":
            self.sel.set_window_size(self.PROJECT_SELECT_WINDOW_SIZE[0],
                                     self.PROJECT_SELECT_WINDOW_SIZE[1])
            return self.select_project_from_select(project_name)
        elif fr == "dropdown":
            return self.select_project_from_dropdown(project_name)
        return self.select_project_from_popup(project_name)

    def select_project_from_dropdown(self, project_name):
        self.sel.click_button(self.PROJECT_CHANGE_BUTTON_LOCATOR)
        self.sel.wait_until_element_is_visible(self.PROJECT_DROPDOWN_LOCATOR)
        self.sel.click_link("partial link=" + project_name)

    def select_project_from_popup(self, project_name):
        self.sel.click_button(self.PROJECT_CHANGE_BUTTON_LOCATOR)
        self.sel.wait_until_element_is_visible(self.PROJECT_POPUP_LOCATOR)
        self.sel.click_link("partial link=" + project_name)

    def current_project_should_be(self, project_name):
        self.sel.element_should_contain(self.PROJECT_CHANGE_BUTTON_LOCATOR, project_name)

    def select_new_project(self):
        project_name = self.create_project()
        self.select_project(project_name)
        self.sel.maximize_browser_window()
        self.sel.reload_page()
        self.current_project_should_be(project_name)
        return project_name
