import imaplib
import email
from email.header import decode_header
import subprocess
import re
from datetime import datetime, timedelta

# ==========================================
# MODE SÉCURITÉ & DÉBOGAGE
# False = PRODUCTION (Recherche sur 24h, Envoi MQTT activé)
# True  = TEST (Recherche sur 48h, Envoi MQTT bloqué)
# ==========================================
DRY_RUN = False

def check_email():
	try:
		# L'ingénierie de l'Architecte : Fenêtre dynamique selon le mode.
		# En production, on cherche uniquement les courriels d'AUJOURD'HUI.
		days_offset = 2 if DRY_RUN else 0
		search_date = (datetime.now() - timedelta(days=days_offset)).strftime("%d-%b-%Y")
		
		mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
		mail.login("yourEmail@xxx.com", "appropriateToken")
		mail.select("inbox")

		search_criteria = f'(SINCE "{search_date}" FROM "hydroquebec")'
		status, messages = mail.search(None, search_criteria)
		
		# Si aucun courriel trouvé AUJOURD'HUI (en production) -> On efface les senseurs.
		if status != "OK" or not messages[0]:
			print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Aucun courriel HQ trouvé depuis le {search_date}. Exécution du Reset...")
			if not DRY_RUN:
				subprocess.run("/home/gimisa/alerte_hq_mqtt.sh reset", shell=True)
			else:
				print("[DRY RUN] -> Commande de RESET bloquée par sécurité.")
			return

		# Prendre le courriel le plus récent
		latest_email_id = messages[0].split()[-1]
		res, msg_data = mail.fetch(latest_email_id, "(RFC822)")
		
		body = ""
		for response in msg_data:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				
				if msg.is_multipart():
					for part in msg.walk():
						if part.get_content_type() in ["text/plain", "text/html"]:
							part_body = part.get_payload(decode=True).decode(errors='ignore')
							body += part_body + " "
				else:
					body = msg.get_payload(decode=True).decode(errors='ignore')

		# Nettoyage drastique (HTML et espaces)
		clean_body = re.sub(r'<[^>]+>', ' ', body)
		clean_body = " ".join(clean_body.lower().split())

		# Frontières de mots pour isolation stricte (Fix_2)
		has_matin = bool(re.search(r'\b6\s*h', clean_body))
		has_soir = bool(re.search(r'\b16\s*h', clean_body))
		
		print(f"=== ANALYSE HQ ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
		print(f"Détection: Matin (6h) = {has_matin}")
		print(f"Détection: Soir (16h) = {has_soir}")
		print("==========================================")

		# Transmission des décisions
		if has_matin:
			print(">>> TRANSMISSION MQTT : hq06 (MATIN)")
			if not DRY_RUN:
				subprocess.run("/home/gimisa/alerte_hq_mqtt.sh hq06", shell=True)
			else:
				print("[DRY RUN] -> 'alerte_hq_mqtt.sh hq06' bloqué.")

		if has_soir:
			print(">>> TRANSMISSION MQTT : hq16 (SOIR)")
			if not DRY_RUN:
				subprocess.run("/home/gimisa/alerte_hq_mqtt.sh hq16", shell=True)
			else:
				print("[DRY RUN] -> 'alerte_hq_mqtt.sh hq16' bloqué.")

		if not has_matin and not has_soir:
			print(">>> AUCUNE POINTE DÉTECTÉE DANS LE TEXTE. AUCUNE ACTION.")

		mail.close()
		mail.logout()

	except Exception as e:
		print(f"Erreur fatale : {e}")

if __name__ == "__main__":
	check_email()
