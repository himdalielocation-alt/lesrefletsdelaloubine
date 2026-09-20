#!/usr/bin/env python3
import json
import os
from datetime import datetime
import sys

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    sys.exit(0)

class SheetSynchronizer:
    def __init__(self):
        self.sheet_id = "12dweBPy5hBkJV4RrqfV-EZKO9lnFqGBpflB_MZcm1gU"
        self.calendar_range = "Calendrier!A:L"
        self.service = None
        
    def authenticate(self):
        try:
            creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
            if creds_json:
                with open('/tmp/creds.json', 'w') as f:
                    f.write(creds_json)
                creds = Credentials.from_service_account_file('/tmp/creds.json')
            else:
                return False
            self.service = build('sheets', 'v4', credentials=creds)
            return True
        except Exception as e:
            print(f"Error: {e}")
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
            
            for row in values[1:]:
                if len(row) < 2:
                    continue
                
                # Colonne A = Date
                date_str = row[0].strip() if len(row) > 0 else ""
                if not date_str:
                    continue
                
                # Colonne D = Réservé (index 3)
                reserved = row[3].strip().lower() if len(row) > 3 else ""
                available = "oui" not in reserved

                calendar.append({
                    "date": date_str,
                    "available": available
                })

            print(f"Loaded {len(calendar)} dates")
            return calendar

        except Exception as e:
            print(f"Error: {e}")
            return []

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
            print(f"Error: {e}")
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
