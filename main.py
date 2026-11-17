from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.resources import resource_add_path
import sqlite3

import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_db_path():

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    db_dir = os.path.join(application_path, 'db')

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    return os.path.join(db_dir, 'loc_list.db')

class SomeApp(App):
    pass

    class CityRoot(BoxLayout, GridLayout, Screen):
        def __init__(self, **kw):
            super().__init__(**kw)
            search_input = ObjectProperty()
            results_list = ObjectProperty()

        def search_list(self):
            cnt = 0
            results_list = self.results_list
            print("Пользователь искал '{}'".format(self.search_input.text))
            conn = sqlite3.connect(get_db_path())
            curs = conn.cursor()
            curs.execute("SELECT * FROM Locs")
            loc_list = [item[0] for item in curs.fetchall()]
            for i in loc_list:
                print(i)
            results_list.clear_widgets()
            for city_base in loc_list:
                if self.search_input.text in city_base:
                    results_list.add_widget(Label(text=city_base))
                    cnt += 1
            self.search_input.text = ""
            cnt = 10 - cnt
            while cnt > 0:
                results_list.add_widget(Label(text=""))
                cnt -= 1
            conn.commit()
            conn.close()

    class NewLocation(BoxLayout, GridLayout, Screen):
        def __init__(self, **kw):
            super().__init__(**kw)
            add_input = ObjectProperty()
            add_list = ObjectProperty()

        def add_to_list(self):
            add_flag = False
            self.add_list.clear_widgets()
            conn = sqlite3.connect(get_db_path())
            curs = conn.cursor()
            curs.execute("SELECT * FROM Locs")
            loc_list = [item[0] for item in curs.fetchall()]
            if self.add_input.text == "":
                self.add_list.add_widget(Label(text="Вы ничего не ввели"))
            else:
                for city_base in loc_list:
                    if self.add_input.text in city_base:
                        add_flag = True
                if add_flag == False:
                    curs.execute("INSERT INTO Locs VALUES (:first)",
                                 {
                                     'first': self.add_input.text,
                                 })
                    self.add_list.add_widget(Label(text=self.add_input.text + " добавлен"))
                else:
                    self.add_list.add_widget(Label(text=self.add_input.text + " уже находится в базе"))
            self.add_input.text = ""
            conn.commit()
            conn.close()

    class WinMan(ScreenManager, App):
        pass

    class SomeApp(App):
        def build(self):
            self.icon = 'pics/icon.png'

        conn = sqlite3.connect(get_db_path())
        curs = conn.cursor()
        curs.execute("""CREATE TABLE if not exists Locs(
                name text)
            """)
        conn.commit()
        conn.close()

    if __name__ == '__main__':
        resource_add_path(resource_path('.'))
        SomeApp().run()


