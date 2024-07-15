from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.carousel import Carousel
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview import RecycleView
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from plyer import gps, vibrator

import time

class pantalla_inicio (BoxLayout):
    def __init__(self, **kwargs):
        super(pantalla_inicio, self).__init__(**kwargs)
        self.orientacion = 'vertical'
        
        self.add_widget(Label(text="Usuario"))
        self.nombre_usuario = TextInput(multilinea=False)
        self.add_widget(self.nombre_usuario)
        
        self.add_widget(Label(text="Contrasena"))
        self.contraseña = TextInput(multilinea=False, contraseña=True)
        self.add_widget(self.contraseña)
        
        self.inicio_button = Button(text="Iniciar Sesion")
        self.inicio_button.bind(on_press=self.check_credentials)
        self.add_widget(self.inicio_button)
    
    def comprobar_usuario(self, instance):
        if self.nombre_usuario.text == "admin" and self.contraseña.text == "admin":
            self.clear_widgets()
            self.add_widget(panelprincipal())
        else:
            Popup = Popup(titulo='Error',
                          contenido=Label(text='Usuario o contrasena incorrectos'),
                          size_hint=(None, None), size=(400, 400))
            Popup.open()

class panelprincipal(TabbedPanel):
    def __init__(self, **kwargs):
        super(panelprincipal, self).__init__(**kwargs)
        self.do_default_tab = False
        
        self.add_widget(TabbedPanelHeader(text='Datos del Paciente', content=self.create_patient_data_panel()))
        self.add_widget(TabbedPanelHeader(text='GPS', content=self.create_gps_panel()))
        self.add_widget(TabbedPanelHeader(text='Galeria de Fotos', content=self.create_gallery()))
        self.add_widget(TabbedPanelHeader(text='Reproductor de Musica', content=self.create_music_player()))
        self.add_widget(TabbedPanelHeader(text='Recordatorios', content=self.create_reminders_panel()))
        self.add_widget(TabbedPanelHeader(text='Citas Medicas', content=self.create_appointments_panel()))
        self.add_widget(TabbedPanelHeader(text='Juegos de Memoria', content=self.create_games_panel()))
        
    def crear_datos_del_paciente(self):
        panel = BoxLayout(orientacion='vertical')
        panel.add_widget(Label(text="Nombre"))
        self.nombre_paciente = TextInput(multilinea=False)
        panel.add_widget(self.nombre_paciente)
        
        panel.add_widget(Label(text="Direccion"))
        self.crear_datos_del_paciente = TextInput(multiline=False)
        panel.add_widget(self.patient_address)
        
        panel.add_widget(Label(text="Numero de Contacto"))
        self.contacto_paciente = TextInput(multiline=False)
        panel.add_widget(self.contacto_paciente)
        
        return panel
    
    def crear_datos_gps(self):
        panel = BoxLayout(orientacion='vertical')
        obtener_ubicacion_button = Button(text='Obtener Ubicacion')
        obtener_ubicacion_button.bind(on_press=self.obtener_ubicacion)
        panel.add_widget(obtener_ubicacion_button)
        self.ubicacion_label = Label(text='Ubicacion: Desconocida')
        panel.add_widget(self.ubicacion_label)
        return panel
    
    def obtener_ubicacion(self, instance):
        try:
            gps.configuracion(on_ubicacion=self.on_ubicacion)
            gps.start()
        except NotImplementedError:
            popup = Popup(title='Error',
                          content=Label(text='El GPS no esta disponible en este dispositivo'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
    
    def on_ubicacion(self, **kwargs):
        self.ubicacion_label.text = f'Ubicacion: {kwargs}'
        gps.stop()
    
    def crear_galeria(self):
        panel = BoxLayout(orientacion='vertical')
        filechooser = FileChooserIconView(on_entrar=self.cargar_imagen)
        self.carrusel = Carousel(direccion='right')
        panel.add_widget(filechooser)
        panel.add_widget(self.carrusel)
        return panel
    
    def cargar_imagen(self, filechooser, seleccion, touch):
        for selected in seleccion:
            imagen = Image(source=selected)
            self.carrusel.add_widget(imagen)
    
    def crear_reproductor_musica(self):
        panel = BoxLayout(orientacion='vertical')
        # Aqui deberias implementar la funcionalidad del reproductor de musica
        panel.add_widget(Label(text='Reproductor de Musica de los 80 (pendiente de implementacion)'))
        return panel
    
    def crear_recordatorio_medicamento(self):
        panel = BoxLayout(orientacion='vertical')
        self.list_recordatorio =RecycleView(adapter=RecycleView(data=[], cls=Label))
        panel.add_widget(self.list_recordatorio)
        
        add_recordatorio_button = Button(text='Anadir Recordatorio')
        add_recordatorio_button.bind(on_press=self.add_recordatorio)
        panel.add_widget(add_recordatorio_button)
        
        return panel
    
    def add_recordatorio(self, instance):
        content = BoxLayout(orientacion='vertical')
        content.add_widget(Label(text='Medicamento'))
        medicinento = TextInput(multiline=False)
        content.add_widget(medicinento)
        
        content.add_widget(Label(text='Dosis'))
        dosis = TextInput(multiline=False)
        content.add_widget(dosis)
        
        content.add_widget(Label(text='Hora'))
        time_input = TextInput(multiline=False)
        content.add_widget(time_input)
        
        guardar_button = Button(text='Guardar')
        content.add_widget(guardar_button)
        
        popup = Popup(title='Anadir Recordatorio', content=content, size_hint=(0.9, 0.9))
        guardar_button.bind(on_press=lambda x: self.guardar_recordatorio(popup, medicinento, dosis, time_input))
        popup.open()
    
    def guardar_recordatorio(self, popup, medicinento, dosis, time_input):
        reminder_text = f'{medicinento.text} - {dosis.text} a las {time_input.text}'
        self.list_recordatorio.adapter.data.extend([reminder_text])
        self.list_recordatorio._trigger_reset_populate()
        popup.dismiss()
    
    def crear_citas_medicas(self):
        panel = BoxLayout(orientacion='vertical')
        self.list_citas= RecycleView(adapter=RecycleView(data=[], cls=Label))
        panel.add_widget(self.list_citas)
        
        add_citas_button = Button(text='Anadir Cita Medica')
        add_citas_button.bind(on_press=self.add_citas)
        panel.add_widget(add_citas_button)
        
        return panel
    
    def add_citas(self, instance):
        content = BoxLayout(orientacion='vertical')
        content.add_widget(Label(text='Nombre del Profesional'))
        professional = TextInput(multiline=False)
        content.add_widget(professional)
        
        content.add_widget(Label(text='Direccion'))
        direccion = TextInput(multiline=False)
        content.add_widget(direccion)
        
        content.add_widget(Label(text='Hora'))
        time_input = TextInput(multiline=False)
        content.add_widget(time_input)
        
        guardar_button = Button(text='Guardar')
        content.add_widget(guardar_button)
        
        popup = Popup(title='Anadir Cita Medica', content=content, size_hint=(0.9, 0.9))
        guardar_button.bind(on_press=lambda x: self.save_appointment(popup, professional, direccion, time_input))
        popup.open()
    
    def save_appointment(self, popup, professional, direccion, time_input):
        citas_text = f'{professional.text} - {direccion.text} a las {time_input.text}'
        self.list_citas.adapter.data.extend([citas_text])
        self.list_citas._trigger_reset_populate()
        popup.dismiss()
    
    def crear_juegos_memoriza(self):
        panel = BoxLayout(orientacion='vertical')
        
        puzzle_button = Button(text='Puzzle')
        puzzle_button.bind(on_prensa=lambda x: self.start_puzzle())
        panel.add_widget(puzzle_button)
        
        ajedrez_button = Button(text='Ajedrez')
        ajedrez_button.bind(on_prensa=lambda x: self.start_ajedrez())
        panel.add_widget(ajedrez_button)
        
        return panel
    
    def comenzar_puzzle(self):
        popup = Popup(title='Puzzle', content=Label(text='Aqui va el juego de Puzzle (pendiente de implementacion)'), size_hint=(0.9, 0.9))
        popup.open()
    
    def comenzar_ajedrez(self):
        popup = Popup(title='Ajedrez', content=Label(text='Aqui va el juego de Ajedrez (pendiente de implementacion)'), size_hint=(0.9, 0.9))
        popup.open()
    
    def alerta_familia(self):
        try:
            vibrator.vibrate(time=1)
        except NotImplementedError:
            popup = Popup(title='Error',
                          content=Label(text='El vibrador no esta disponible en este dispositivo'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()

class AlzheimerApp(App):
    def build(self):
        return panelprincipal()

if __name__ == '__main__':
    AlzheimerApp()
