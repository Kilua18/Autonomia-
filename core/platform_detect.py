"""
Détection de plateforme - Raspberry Pi, Termux, ou PC standard
"""

import os
import platform


def detect_platform():
    """Détecte la plateforme d'exécution.

    Returns:
        str: 'raspberry_pi', 'termux', ou 'pc'
    """
    # Vérifier Raspberry Pi
    if _is_raspberry_pi():
        return 'raspberry_pi'

    # Vérifier Termux (Android)
    if _is_termux():
        return 'termux'

    return 'pc'


def _is_raspberry_pi():
    """Détecte si on tourne sur un Raspberry Pi."""
    # Vérifier /proc/cpuinfo pour le modèle
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo:
                return True
    except FileNotFoundError:
        pass

    # Vérifier /proc/device-tree/model
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            if 'Raspberry Pi' in model:
                return True
    except FileNotFoundError:
        pass

    # Vérifier la variable d'environnement (override manuel)
    if os.environ.get('AUTONOMIA_PLATFORM') == 'raspberry_pi':
        return True

    return False


def _is_termux():
    """Détecte si on tourne sur Termux (Android)."""
    return os.environ.get('PREFIX', '').startswith('/data/data/com.termux')


def get_platform_info():
    """Retourne les informations détaillées de la plateforme."""
    plat = detect_platform()
    info = {
        'platform': plat,
        'system': platform.system(),
        'machine': platform.machine(),
        'node': platform.node(),
    }

    if plat == 'raspberry_pi':
        try:
            with open('/proc/device-tree/model', 'r') as f:
                info['model'] = f.read().strip('\x00')
        except FileNotFoundError:
            info['model'] = 'Raspberry Pi (modèle inconnu)'

        # Température CPU
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read().strip()) / 1000
                info['cpu_temp'] = f"{temp}°C"
        except (FileNotFoundError, ValueError):
            pass

    return info
