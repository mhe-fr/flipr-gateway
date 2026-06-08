import asyncio
from bleak import BleakClient, BleakScanner

FLIPR_CHARACTERISTIC_UUID = "00000006-0000-1000-8000-00805f9b34fb"
FLIPR_ANALYZE_UUID = "0000940d-0000-1000-8000-00805f9b34fb"
SYNC_CHAR_UUID = "000073b4-0000-1000-8000-00805f9b34fb"

# CONFIGURATION - À remplacer par vos valeurs nRF Connect
DEVICE_ADDRESS = "FD:07:B5:E5:6B:A0"  # Adresse MAC de votre device
CHARACTERISTIC_UUID = FLIPR_CHARACTERISTIC_UUID  # Exemple (ex: Heart Rate)


# Fonction de callback pour les notifications
def notification_handler(sender_handle: int, data: bytearray):
    """Cette fonction est appelée à chaque fois que le device envoie une nouvelle donnée."""
    print(f"[Notification] Reçu de handle {sender_handle}: {data.hex().upper()}")
    # C'est ici que vous décoderez vos octets plus tard
    # Exemple : valeur_entiere = int.from_bytes(data, byteorder='little')


async def main():
    print(f"Recherche de l'appareil {DEVICE_ADDRESS}...")

    # Optionnel : On vérifie que l'appareil est bien visible avant de se connecter
    device = await BleakScanner.find_device_by_address(DEVICE_ADDRESS, timeout=10.0)
    if not device:
        print(f"Impossible de trouver l'appareil avec l'adresse {DEVICE_ADDRESS}.")
        return

    print(f"Appareil trouvé ! Connexion en cours à {device.name}...")

    # Connexion au client
    async with BleakClient(device) as client:
        if client.is_connected:
            print(f"Connecté avec succès à {device.name}")
        else:
            print("Échec de la connexion.")
            return

        # -------------------------------------------------------------
        # 1. Exploration (Optionnel - pour valider la structure)
        # -------------------------------------------------------------
        print("\n--- Exploration des Services et Caractéristiques ---")
        for service in client.services:
            print(f"[Service] {service.uuid} : {service.description}")
            for char in service.characteristics:
                print(
                    f"  [Carac] {char.uuid} | Propriétés: {char.properties}"
                )
        print("-----------------------------------------------------\n")

        # -------------------------------------------------------------
        # 2. Exemple de LECTURE UNIQUE (Read)
        # -------------------------------------------------------------
        # À activer si votre caractéristique supporte le 'read'
        try:
            print(f"Tentative de lecture de la caractéristique...")
            raw_data = await client.read_gatt_char(CHARACTERISTIC_UUID)
            print(f"[Read] Donnée brute (Hex): {raw_data.hex().upper()}")
        except Exception as e:
            print(f"La lecture directe a échoué (normal si non supporté) : {e}")

        # -------------------------------------------------------------
        # 3. Exemple d'ÉCOUTE EN CONTINU (Notifications)
        # -------------------------------------------------------------
        # À activer si votre caractéristique supporte 'notify'

        # try:
        #     print(f"\nActivation des notifications pour {CHARACTERISTIC_UUID}...")
        #     await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        #     print("Écoute en cours pendant 20 secondes... Bougez le capteur !")
        #     await asyncio.sleep(20.0)

        #     # Arrêt propre des notifications
        #     await client.stop_notify(CHARACTERISTIC_UUID)
        #     print("Notifications arrêtées.")

        # except Exception as e:
        #     print(f"Erreur avec les notifications : {e}")

    print("Déconnecté.")


# Lancement du programme asynchrone
if __name__ == "__main__":
    asyncio.run(main())