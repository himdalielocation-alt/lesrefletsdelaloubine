#!/usr/bin/env python3
"""
Synchronise les données de tarification du Google Sheet vers un fichier JSON.
"""

import json
import os
from datetime import datetime
import sys

try:
    from google.auth.oauth2.service_account import Credentials as SACredentials
    from googleapiclient.discovery import build
except ImportError:
    print("⚠️  Google API libraries not installed.")
    sys.exit(0)

class SheetSynchronizer:
    def __init__(self):
        self.sheet_id = "12dweBPy5hBkJV4RrqfV-EZKO9lnFqGBpflB_MZcm1gU"
        self.calendar_range = "Calendrier!A:F"
        self.service = None
        
    def authenticate(self) -> bool:
        try:
            creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
            if creds_json:
                with open('/tmp/creds.json', 'w') as f:
                    f.write(creds_json)
                creds = SACredentials.from_service_account_file('/tmp/creds.json')
            else:
                print("⚠️  GOOGLE_SERVICE_ACCOUNT_JSON non défini")
                return False
                
            self.service = build('sheets', 'v4', credentials=creds)
            return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

    def get_calendar_data(self):
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=self.calendar_range
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []

            calendar = []
            headers = values[0] if values else []
            
            date_idx = self.find_column_index(headers, ['Date', 'Début'])
            avail_idx = self.find_column_index(headers, ['Disponible', 'Statut'])
            price_idx = self.find_column_index(headers, ['Prix', 'Tarif'])
            
            for row in values[1:]:
                if len(row) <= date_idx or not row[date_idx].strip():
                    continue
                
                date_str = row[date_idx].strip()
                available = True
                price = 89
                
                if avail_idx >= 0 and len(row) > avail_idx:
                    available = 'non' not in row[avail_idx].lower()
                
                if price_idx >= 0 and len(row) > price_idx:
                    try:
                        price = int(float(row[price_idx].replace('€', '').strip()))
                    except:
                        pass
                
                calendar.append({
                    "date": date_str,
                    "available": available,
                    "price": price,
                    "minStay": 1
                })

            return calendar

        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []

    @staticmethod
    def find_column_index(headers, keywords):
        for i, header in enumerate(headers):
            for keyword in keywords:
                if keyword.lower() in header.lower():
                    return i
        return -1

    def save_to_json(self, calendar_data):
        try:
            output_data = {
                "lastUpdate": datetime.utcnow().isoformat() + "Z",
                "property": {
                    "name": "Les Reflets de la Loubine",
                    "location": "Château-d'Olonne, Vendée",
                    "capacity": "2 pièces, 4 personnes"
                },
                "calendar": calendar_data
            }
            
            os.makedirs('data', exist_ok=True)
            with open('data/calendar.json', 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

    def run(self):
        if not self.authenticate():
            return False
        calendar_data = self.get_calendar_data()
        if not calendar_data:
            return False
        return self.save_to_json(calendar_data)

if __name__ == "__main__":
    sync = SheetSynchronizer()
    sync.run()
