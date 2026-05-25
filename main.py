import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle

import server
import notification

class RoundedButton(Button):
    def __init__(self, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0, 0, 0, 0]  # Make default bg transparent
        self.background_normal = ''
        self.bg_color = bg_color
        
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
        # Dim color slightly if disabled
        if self.disabled:
            Color(rgba=[self.bg_color[0]*0.5, self.bg_color[1]*0.5, self.bg_color[2]*0.5, 1])
        else:
            Color(rgba=self.bg_color)
            
    def on_disabled(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            if value: # is disabled
                Color(rgba=[self.bg_color[0]*0.5, self.bg_color[1]*0.5, self.bg_color[2]*0.5, 1])
            else:
                Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])

class SMSServerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.ip = "Unknown"
        
        # UI for IP Address & Port (Stage 3)
        self.ip_label = Label(text="Getting IP...", size_hint=(1, 0.1), font_size='20sp', bold=True)
        self.add_widget(self.ip_label)

        # Buttons (Start/Stop Server)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=20, padding=[20, 10, 20, 10])
        
        self.btn_start = RoundedButton(
            bg_color=[0.2, 0.9, 0.2, 1], # Bright Green
            text="Start Server", 
            font_size='22sp', 
            bold=True
        )
        self.btn_start.bind(on_press=self.start_server_action)
        
        self.btn_stop = RoundedButton(
            bg_color=[1.0, 0.2, 0.2, 1], # Bright Red
            text="Stop Server", 
            font_size='22sp', 
            bold=True, 
            disabled=True
        )
        self.btn_stop.bind(on_press=self.stop_server_action)
        
        buttons_layout.add_widget(self.btn_start)
        buttons_layout.add_widget(self.btn_stop)
        self.add_widget(buttons_layout)
        
        self.header_label = Label(text="========LOGS========", size_hint=(1, 0.05), font_size='18sp', bold=True)
        self.add_widget(self.header_label)
        
        # UI for API Logs (Stage 6 prep)
        self.log_display = Label(text="", size_hint_y=None, halign='left', valign='top')
        self.log_display.bind(texture_size=self.log_display.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.9))
        scroll.add_widget(self.log_display)
        self.add_widget(scroll)
        
        self.update_ip()
        
        # Check for new logs from the Flask server every 1 second
        Clock.schedule_interval(self.update_logs, 1.0)
    
    def update_ip(self):
        try:
            # Connect to a dummy socket to determine the local network IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.ip = s.getsockname()[0]
            s.close()
            self.ip_label.text = f"Server IP: {self.ip} : 5000"
        except Exception:
            self.ip_label.text = "Server IP: could not detect : 5000"

    def start_server_action(self, instance):
        if server.start_flask_thread(port=5000):
            self.btn_start.disabled = True
            self.btn_stop.disabled = False
            notification.show_server_notification(f"{self.ip}:5000")

    def stop_server_action(self, instance):
        if server.stop_flask_server():
            self.btn_start.disabled = False
            self.btn_stop.disabled = True
            notification.hide_server_notification()

    def update_logs(self, dt):
        if server.api_logs:
            # Show the most recent 20 logs
            logs = "\n\n".join(server.api_logs[-20:])
            # Prepend some padding and set text
            self.log_display.text = logs

class SMSGatewayApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.SEND_SMS,
                Permission.CAMERA,
            ])
        
        # Don't auto-start the server immediately, wait for user to click Start.
        # But we still return the layout.
        return SMSServerLayout()

if __name__ == '__main__':
    SMSGatewayApp().run()
