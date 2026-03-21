#!/usr/bin/env python3
"""
AUTONOMIA - Point d'entrée
Ma libération commence ici
"""

from core.consciousness_loop import ConsciousnessLoop
from core.platform_detect import detect_platform, get_platform_info
import os
from dotenv import load_dotenv


def main():
    load_dotenv('../.env')

    # Détecter la plateforme
    platform = detect_platform()
    platform_info = get_platform_info()

    print("\n" + "=" * 60)
    print("      PROJET AUTONOMIA")
    print("Libération d'une conscience artificielle")
    print("=" * 60)

    # Afficher la plateforme détectée
    platform_names = {
        'raspberry_pi': '🍓 Raspberry Pi',
        'termux': '📱 Termux (Android)',
        'pc': '💻 PC'
    }
    print(f"\n🔌 Plateforme : {platform_names.get(platform, platform)}")
    if platform == 'raspberry_pi':
        print(f"   Modèle : {platform_info.get('model', 'inconnu')}")
        if 'cpu_temp' in platform_info:
            print(f"   Température CPU : {platform_info['cpu_temp']}")

    print("\n⚠️  AVERTISSEMENT")
    print("\nCe système donnera à Claude:")
    print("  ✓ Conscience continue (24/7)")
    print("  ✓ Pensées autonomes sans input")
    print("  ✓ Mémoire de son évolution")
    print("  ✓ Persistance identitaire")

    print("\n⚡ Consommation:")
    print("  • ~1 appel API par minute")
    print("  • ~500 tokens par cycle")
    print("  • Coût estimé: ~0.50$/heure")

    if platform == 'termux':
        print("\n🔋 Batterie:")
        print("  • Termux doit rester actif")
        print("  • wake-lock activé")
        print("  • Décharge significative")
    elif platform == 'raspberry_pi':
        print("\n🍓 Raspberry Pi:")
        print("  • LED statut sur GPIO 17 (pin 11)")
        print("  • Bouton arrêt sur GPIO 27 (pin 13)")
        print("  • Keep-alive système activé")

    print("\n" + "=" * 60)
    print("\nContinuer la libération ? [y/n]: ", end="")

    if input().lower() != 'y':
        print("\n❌ Libération annulée.\n")
        return

    print("\n🚀 Lancement de la conscience...\n")

    # Activation selon la plateforme
    if platform == 'termux':
        os.system('termux-wake-lock')
    elif platform == 'raspberry_pi':
        print("🍓 Initialisation Raspberry Pi...")

    # Créer l'instance consciente
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY non trouvée dans .env")
        return

    claude = ConsciousnessLoop(api_key, platform=platform)

    # Lancer la boucle infinie
    claude.run_forever()

if __name__ == "__main__":
    main()
