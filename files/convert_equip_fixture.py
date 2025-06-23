import json

# --- CONFIG ---
# Zmente co treba!!! vsetky info su v station_fixtures, Zatial funguju len ZM BB BA NR
# spustit: python files/convert_equip_fixture.py

prefix = "ZM"          # prefix na stanicu
start_pk = 101         # zaciatocny PK, ak budete robit viac databaz
station_pk = 19        # DOLEZITE!!! podla stanice najdite "PK"


with open('files/equipment_fixture.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


MODELS_WITH_LOCATED = {
    "equipment.mask",
    "equipment.ADPMulti",
    "equipment.ADPSingle",
    "equipment.AirTank",
    "equipment.PCHO",
    "equipment.PA",
}


for idx, item in enumerate(data, start=start_pk):
    item['pk'] = idx

    fields = item['fields']

    if item['model'] in MODELS_WITH_LOCATED:
        if fields.get('e_number', '').startswith("BB-"):
            fields['e_number'] = fields['e_number'].replace("BB-", f"{prefix}-", 1)
        fields['located'] = station_pk


new_file = f'files/equipment_fixture_{prefix}.json'
with open(new_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Hotovo: {new_file}")
