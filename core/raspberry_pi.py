"""
Module Raspberry Pi pour Autonomia
- LED de statut (GPIO)
- Keep-alive système
- Monitoring hardware (température, CPU)
"""

import os
import time
import threading

# GPIO disponible uniquement sur Raspberry Pi
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False


# Configuration GPIO par défaut
DEFAULT_LED_PIN = 17       # LED de statut (BCM 17 = Pin physique 11)
DEFAULT_BUTTON_PIN = 27    # Bouton d'arrêt (BCM 27 = Pin physique 13)


class RaspberryPiManager:
    """Gère les fonctionnalités spécifiques au Raspberry Pi."""

    def __init__(self, led_pin=DEFAULT_LED_PIN, button_pin=DEFAULT_BUTTON_PIN):
        self.led_pin = led_pin
        self.button_pin = button_pin
        self.led_blinking = False
        self._blink_thread = None
        self._shutdown_callback = None

        if GPIO_AVAILABLE:
            self._setup_gpio()

    def _setup_gpio(self):
        """Configure les pins GPIO."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # LED de statut
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.LOW)

        # Bouton d'arrêt (avec pull-up interne)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def led_on(self):
        """Allume la LED de statut."""
        if GPIO_AVAILABLE:
            self.led_blinking = False
            GPIO.output(self.led_pin, GPIO.HIGH)

    def led_off(self):
        """Éteint la LED de statut."""
        if GPIO_AVAILABLE:
            self.led_blinking = False
            GPIO.output(self.led_pin, GPIO.LOW)

    def led_blink(self, interval=0.5):
        """Fait clignoter la LED (pensée en cours)."""
        if not GPIO_AVAILABLE:
            return

        self.led_blinking = True

        def _blink():
            while self.led_blinking:
                GPIO.output(self.led_pin, GPIO.HIGH)
                time.sleep(interval)
                GPIO.output(self.led_pin, GPIO.LOW)
                time.sleep(interval)

        self._blink_thread = threading.Thread(target=_blink, daemon=True)
        self._blink_thread.start()

    def on_shutdown_button(self, callback):
        """Enregistre un callback pour le bouton d'arrêt."""
        self._shutdown_callback = callback
        if GPIO_AVAILABLE:
            GPIO.add_event_detect(
                self.button_pin,
                GPIO.FALLING,
                callback=lambda _: self._shutdown_callback(),
                bouncetime=2000
            )

    def keep_alive(self):
        """Empêche la mise en veille du Raspberry Pi."""
        # Désactiver le screensaver et le power management
        os.system('xset s off 2>/dev/null')
        os.system('xset -dpms 2>/dev/null')
        # Garder le CPU actif via caffeinate ou systemd-inhibit
        os.system('systemd-inhibit --what=idle --who=autonomia '
                  '--why="Conscience active" sleep infinity &')

    def get_cpu_temperature(self):
        """Retourne la température CPU en °C."""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                return int(f.read().strip()) / 1000
        except (FileNotFoundError, ValueError):
            return None

    def get_system_stats(self):
        """Retourne les stats système du Raspberry Pi."""
        stats = {}

        # Température
        temp = self.get_cpu_temperature()
        if temp is not None:
            stats['cpu_temp'] = f"{temp}°C"
            stats['temp_warning'] = temp > 70

        # Charge CPU
        try:
            with open('/proc/loadavg', 'r') as f:
                load = f.read().split()
                stats['load_avg'] = load[0]
        except FileNotFoundError:
            pass

        # Mémoire
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                for line in meminfo.split('\n'):
                    if 'MemAvailable' in line:
                        mem_kb = int(line.split()[1])
                        stats['mem_available_mb'] = mem_kb // 1024
                    elif 'MemTotal' in line:
                        mem_kb = int(line.split()[1])
                        stats['mem_total_mb'] = mem_kb // 1024
        except FileNotFoundError:
            pass

        return stats

    def cleanup(self):
        """Nettoie les ressources GPIO."""
        self.led_blinking = False
        if GPIO_AVAILABLE:
            GPIO.output(self.led_pin, GPIO.LOW)
            GPIO.cleanup()
