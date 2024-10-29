from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from plyer import filechooser
#from training import CycloneSeverity
#from changedetection import ChangeDetection
Builder.load_string("""
<NavigationDrawer>

    MDNavigationDrawerMenu:
        
        MDNavigationDrawerHeader:
            title: "Made In India"
            text: " "
            source: "Tiranga.jpeg" 
            spacing: "10dp"
                
        MDNavigationDrawerDivider:
            
        MDNavigationDrawerItem:
            text: "Severity"
            icon: "wind-power"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 1"

        MDNavigationDrawerItem:
            text: "Change Detection"
            icon: "compare"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 2"
            
        MDNavigationDrawerItem:
            text: "Settings"
            icon: "cog"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 3"

        MDNavigationDrawerDivider:

<WelcomeScreen>:
    MDScreen:
        MDBoxLayout:
            orientation:'vertical'
            md_bg_color:(120/255.0,170/255.0,160/255.0,1)

            MDLabel:
                text:'Welcome to UI Change Detection APP'
                halign:'center'
                font_style:'H3'

            MDFloatingActionButton:
                icon:'arrow-right'
                pos_hint:{'center_x': 0.9, 'center_y':0.2}
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'settings'

<MainScreen>
    MDScreen:

        MDTopAppBar:    
            id: top
            title: app.title
            pos_hint: {"top": 1}
            elevation: 4
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

        MDNavigationLayout:

            MDScreenManager:
                id: screen_manager

                MDScreen:
                    name: "scr 1"

                    MDLabel:
                        text: "Cyclones are caused by atmospheric disturbances around a low-pressure area distinguished by swift and often destructive air circulation. Cyclones are usually accompanied by violent storms and bad weather. The air circulates inward in an anticlockwise direction in the Northern hemisphere and clockwise in the Southern hemisphere. Cyclones are classified into five different levels on the basis of wind speed. They are further divided into the following categories according to their capacity to cause damage:-"
                        halign: "center"
                        pos_hint: {"center_x":0.5, "center_y":0.85}
                        bold: True
                        font_style: "H6"

                    Image:
                        source: "Untitled.jpeg"
                        pos_hint: {"center_x":0.5, "center_y":0.7}

                    MDFillRoundFlatButton:
                        text: 'Choose File'
                        pos: root.width*0.15, root.height*0.44
                        md_bg_color: "black"
                        text_color: 'white'
                        on_release: root.file_chooser()

                    MDLabel:
                        id: selected_path
                        text: ""
                        pos_hint: {"center_x":0.57, "center_y":0.5}
                        theme_text_color: "Custom"
                        text_color: (1, 0, 0, 1)
                        bold: True

                    MDRectangleFlatIconButton:
                        icon: 'wind-power'
                        text: 'Check Severity of Cyclone'
                        pos: root.width*0.15, root.height*0.37
                        line_color: 'red'
                        on_release: root.cyclone_severity()
 
                MDScreen:
                    name: "scr 2"

                    MDLabel:
                        text: "Change detection for GIS (geographical information systems) is a process that measures how the attributes of a particular area have changed between two or more time periods. Change detection often involves comparing aerial photographs or satellite imagery of the area taken at different times. The process is most frequently associated with environmental monitoring, natural resource management, or measuring urban development. Change detection is done by comparing two raster images that were taken at different times but which cover the same area. As the images cover the same area, the images overlay each other. Imagine two grids stacked on top of each other. It is then a matter of comparing whether the value of a pixel in the new raster is the same as the value of the pixel in the old raster. Pixels that have changed are then marked. The output is usually a raster that covers the same extents as the two images with the changed areas highlighted."
                        halign: "center"
                        pos_hint: {"center_x":0.5, "center_y":0.85}
                        bold: True
                        font_style: "H6"

                    Image:
                        source: "uoo5z.png"
                        pos_hint: {"center_x":0.2, "center_y":0.62}
                    
                    MDFillRoundFlatButton:
                        text: 'Choose File 1'
                        pos: root.width*0.15, root.height*0.34
                        md_bg_color: "black"
                        text_color: 'white'
                        on_release: root.file_chooser()
                    
                    MDLabel:
                        id: selected_path
                        text: ""
                        pos_hint: {"center_x":0.57, "center_y":0.5}
                        theme_text_color: "Custom"
                        text_color: (1, 0, 0, 1)
                        bold: True
                    
                    MDFillRoundFlatButton:
                        text: 'Choose File 2'
                        pos: root.width*0.15, root.height*0.18
                        md_bg_color: "black"
                        text_color: 'white'
                        on_release: root.file_chooser()
                    
                    MDLabel:
                        id: selected_path
                        text: ""
                        pos_hint: {"center_x":0.57, "center_y":0.5}
                        theme_text_color: "Custom"
                        text_color: (1, 0, 0, 1)
                        bold: True
                    
                    MDRectangleFlatIconButton:
                        icon: 'compare'
                        text: 'Detect Change'
                        pos: root.width*0.35, root.height*0.26
                        line_color: 'red'
                        on_release: root.cyclone_severity()
                
                MDScreen:
                    name: "scr 3"

                    MDLabel:
                        text: "Settings"
                        halign: "center"
                        font_style: "H4"

            MDNavigationDrawer:
                id: nav_drawer
                radius: (0, 16, 16, 0)

                NavigationDrawer:
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer
""")

class WelcomeScreen(Screen):
    pass

class MainScreen(Screen):

    def file_chooser(self):
        filechooser.open_file(on_selection = self.selected)

    def selected(self, selection):
        if selection:
            self.selected_path = self.selected
            self.root.ids.selected_path.text = selection[0]
        pass
    def cyclone_severity(self):
        try:
            if hasattr(self, 'selected_file'):
                file_content = CycloneSeverity(self.selected_path)
                print("File content:")
                print(file_content)
            else:
                print("No file selected.")
        except Exception as e:
            print(f"Error processing the file: {e}")

        CycloneSeverity.open_file(on_selection = self.selected_path)

    def change_detection(self):
        try:
            if hasattr(self, 'selected_file'):
                file_content = ChangeDetection(self.selected_path)
                print("File content:")
                print(file_content)
            else:
                print("No file selected.")
        except Exception as e:
            print(f"Error processing the file: {e}")
            
        ChangeDetection.open_file(on_selection = self.selected_path)
    pass
    
class NavigationDrawer(MDScrollView):    
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    
class App(MDApp):
    def __init__(self, **kwargs):
        self.title = "Change Detection UI"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='menu'))
        sm.add_widget(MainScreen(name='settings'))
        return sm

if __name__ == "__main__":
    App().run()
