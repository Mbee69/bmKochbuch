from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivymd.uix.textfield import TextInput
from kivy.uix.textinput import TextInput
from kivymd.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen

import uuid
import base64

import pickle
from kivy.uix.dropdown import DropDown 
from kivy.base import runTouchApp 

from  bmKochbuch import Kochbuch,Speise,Zutat,Lager

class MainWindow(Screen):
    pass

class EditSpeise(Screen):
    pass

class EditZutat(Screen):
    pass

class EditSpeiseZutat(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class MainApp(MDApp):
    def on_start(self):
        # Set colors
        self.theme_cls.primary_palette = 'Blue'
        self.active_tab = "Speisen"

        self.kochbuch = Kochbuch("Kochbuch")
        self.lager = Lager("Lager")

        self.lade_speisen()
        self.lade_zutaten()

    def build(self):
        A = ScreenManagement()
        A.current = 'main'

        return A

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.active_tab = tab_text
        #instance_tab.ids.label.text = tab_text
        return

    def lade_speisen(self):
        self.root.get_screen('main').ids.speisen_list.clear_widgets()
        for speise in self.kochbuch.get_speisen():
            self.add_new_speise(speise)

    def lade_zutaten(self):
        self.root.get_screen('main').ids.zutaten_list.clear_widgets()
        for zutat in self.lager.get_zutaten():
            self.add_new_zutat(zutat)

    def lade_speisen_zutaten(self, speise_guid):
        print("lade_speisen_zutaten: " + speise_guid)
        self.root.get_screen('edit_speise').ids.edit_speise_zutaten_list.clear_widgets()
        speise = self.kochbuch.get_speise(speise_guid)
        print("Zutaten in Speise: " + str(len(speise.get_zutaten())))
        for zutat in speise.get_zutaten():
            self.new_zutat_zeile = TwoLineAvatarIconListItem(
                text=zutat.get_name(), 
                secondary_text=zutat.get_guid()
                )
            self.new_zutat_zeile.bind(on_press=self.list_item_click_speise)
            self.root.get_screen('edit_speise').ids.edit_speise_zutaten_list.add_widget(self.new_zutat_zeile)


    def save_speise(self):
        self.kochbuch.get_speise(self.root.get_screen('edit_speise').ids.sp_guid.text).set_name(self.root.get_screen('edit_speise').ids.sp_name.text)
        self.lade_speisen()     
        self.root.current = "main"
        self.root.transition.direction = "right"

    def save_zutat(self):
        zutat = self.lager.get_zutat(self.root.get_screen('edit_zutat').ids.zt_guid.text)
        zutat.set_name(self.root.get_screen('edit_zutat').ids.zt_name.text)
        zutat.set_einheit(self.root.get_screen('edit_zutat').ids.zt_einheit.text)
        zutat.set_preis(self.root.get_screen('edit_zutat').ids.zt_preis.text)
        zutat.set_menge(self.root.get_screen('edit_zutat').ids.zt_menge.text)
        zutat.set_mindest(self.root.get_screen('edit_zutat').ids.zt_mindest.text)

        self.lade_zutaten()     
        self.root.current = "main"
        self.root.transition.direction = "right"

    def save_speise_zutat(self):
        speise_guid = self.root.get_screen('edit_speise_zutat').ids.zt_speise_guid.text
        zutat_guid = self.root.get_screen('edit_speise_zutat').ids.zt_guid.text

        zutat = self.kochbuch.get_speise(speise_guid).get_zutat(zutat_guid)
        zutat.set_name(self.root.get_screen('edit_speise_zutat').ids.zt_name.text)
        zutat.set_einheit(self.root.get_screen('edit_speise_zutat').ids.zt_einheit.text)
        zutat.set_preis(self.root.get_screen('edit_speise_zutat').ids.zt_preis.text)
        zutat.set_menge(self.root.get_screen('edit_speise_zutat').ids.zt_menge.text)
        zutat.set_mindest(self.root.get_screen('edit_speise_zutat').ids.zt_mindest.text)

#        self.lade_speise_zutaten()     
        self.root.current = "edit_speise"
        self.root.transition.direction = "right"

    def add_new_speise(self, new_speise):
        #print("Ok!")
        #self.speisen.append(new_speise)
        
        self.neue_speise_zeile = TwoLineAvatarIconListItem(
                text=new_speise.name, 
                secondary_text=str(new_speise.get_guid()),
                #on_touch_up=self.test
                )
        self.neue_speise_zeile.bind(on_press=self.list_item_click)

        self.root.get_screen('main').ids.speisen_list.add_widget(
            self.neue_speise_zeile
            )
 

    def add_new_zutat(self, new_zutat):
        #print("Ok!")
        self.new_zutat_zeile = TwoLineAvatarIconListItem(
                text=new_zutat.name, 
                secondary_text=str(new_zutat.get_guid())
                )
        self.new_zutat_zeile.bind(on_press=self.list_item_click)

        self.root.get_screen('main').ids.zutaten_list.add_widget(
            self.new_zutat_zeile
            )

    def add_new_speise_zutat(self):
        print(self.root.get_screen('edit_speise').ids.sp_guid.text)
        new_zutat = Zutat("Neue Zutat","","","","")
        self.new_zutat_zeile = TwoLineAvatarIconListItem(
                text=new_zutat.name, 
                secondary_text=str(new_zutat.get_guid())
                )
        self.new_zutat_zeile.bind(on_press=self.list_item_click_speise)

        self.kochbuch.get_speise(self.root.get_screen('edit_speise').ids.sp_guid.text).add_zutat(new_zutat)
        self.root.get_screen('edit_speise').ids.edit_speise_zutaten_list.add_widget(self.new_zutat_zeile)

    def add_new(self):
        if self.active_tab == "Speisen":
            neue_speise = Speise("Omlette NEW!")
            self.kochbuch.add_speise(neue_speise)
            self.add_new_speise(neue_speise)
        else:
            neue_zutat = Zutat("Zutat NEW!","","","","")
            self.lager.add_zutat(neue_zutat)
            self.add_new_zutat(neue_zutat)

    def list_item_click(self, listItem):
        if self.root.current == "main":
            if self.active_tab == "Speisen":
                print("list_item_click Speise: ",listItem.secondary_text)

                speise = self.kochbuch.get_speise(listItem.secondary_text)
                self.root.get_screen('edit_speise').ids.sp_name.text = speise.get_name()
                self.root.get_screen('edit_speise').ids.sp_guid.text = speise.get_guid()

                self.lade_speisen_zutaten(listItem.secondary_text)

                self.root.current = "edit_speise"
                self.root.transition.direction = "left"                            
        
            if self.active_tab == "Zutaten" :
                print("Zutat: ",listItem.secondary_text)

                zutat = self.lager.get_zutat(listItem.secondary_text)
                self.root.get_screen('edit_zutat').ids.zt_name.text = zutat.get_name()
                self.root.get_screen('edit_zutat').ids.zt_guid.text = zutat.get_guid()
                self.root.get_screen('edit_zutat').ids.zt_einheit.text = zutat.get_einheit()
                self.root.get_screen('edit_zutat').ids.zt_preis.text = zutat.get_preis()
                self.root.get_screen('edit_zutat').ids.zt_mindest.text = zutat.get_mindest()
                self.root.get_screen('edit_zutat').ids.zt_menge.text = zutat.get_menge()


                self.root.current = "edit_zutat"
                self.root.transition.direction = "left"

    def list_item_click_speise(self, listItem):
        print("Zutat: ",listItem.secondary_text)

        speise_guid = self.root.get_screen('edit_speise').ids.sp_guid.text
        zutat = self.kochbuch.get_speise(speise_guid).get_zutat(listItem.secondary_text)
        self.root.get_screen('edit_speise_zutat').ids.zt_name.text = zutat.get_name()
        self.root.get_screen('edit_speise_zutat').ids.zt_speise_guid.text = speise_guid
        self.root.get_screen('edit_speise_zutat').ids.zt_guid.text = zutat.get_guid()
        self.root.get_screen('edit_speise_zutat').ids.zt_einheit.text = zutat.get_einheit()
        self.root.get_screen('edit_speise_zutat').ids.zt_preis.text = zutat.get_preis()
        self.root.get_screen('edit_speise_zutat').ids.zt_mindest.text = zutat.get_mindest()
        self.root.get_screen('edit_speise_zutat').ids.zt_menge.text = zutat.get_menge()

        self.root.current = "edit_speise_zutat"
        self.root.transition.direction = "left"
        

    def del_current(self):
        if self.root.current == "edit_speise":
            print(self.root.get_screen('edit_speise').ids.sp_guid.text)
            self.kochbuch.del_speise(self.root.get_screen('edit_speise').ids.sp_guid.text)
            self.kochbuch.save()
            self.lade_speisen()
            
            self.root.current = "main"
            self.root.transition.direction = "right"

        if self.root.current == "edit_zutat":
            zt_guid = self.root.get_screen('edit_zutat').ids.zt_guid.text
            print(zt_guid)
            self.lager.del_zutat(zt_guid)
            self.lager.save()
            self.lade_zutaten()
            
            self.root.current = "main"
            self.root.transition.direction = "right"

        if self.root.current == "edit_speise_zutat":
            speise_guid = self.root.get_screen('edit_speise_zutat').ids.zt_speise_guid.text
            zutat_guid = self.root.get_screen('edit_speise_zutat').ids.zt_guid.text
            self.kochbuch.get_speise(speise_guid).del_zutat(zutat_guid)
            self.kochbuch.save()
            self.lade_speisen_zutaten(speise_guid)

            self.root.current = "edit_speise"
            self.root.transition.direction = "right"

    def tb_option_click(self):
        # dropdown = DropDown() 
        # for index in range(10): 
        
        #     # Adding button in drop down list 
        #     btn = Button(text ='Value % d' % index, size_hint_y = None, height = 40) 
        
        #     # binding the button to show the text when selected 
        #     btn.bind(on_release = lambda btn: dropdown.select(btn.text)) 
        
        #     # then add the button inside the dropdown 
        #     dropdown.add_widget(btn)
        # dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x)) 
        # runTouchApp(self.root.get_screen('edit_zutat')) 


        if self.root.current == "main":
            print("Konfig!")
            self.kochbuch.save()
            self.lager.save()

    def sort_speisen(self):
        print("sort")
        #self.root.ids.speisen_list.so
    
    def nav_main(self):
        self.root.current = "main"
        self.root.transition.direction = "right"

    def nav_speise_edit(self):
        self.root.current = "edit_speise"
        self.root.transition.direction = "right"


class Tab(FloatLayout, MDTabsBase):
    '''Class implementign content for a tab'''


if __name__ == "__main__":
    MainApp().run()





    
