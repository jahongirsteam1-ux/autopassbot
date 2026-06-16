import json
import pymongo
from pathlib import Path

MONGO_URL = "mongodb+srv://Jahongir:Jahongir2006@cluster0.t4fbvgd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URL)
db = client["autopass_db"]

DATA_DIR = Path("data")

if not DATA_DIR.exists():
    print("No data directory found!")
else:
    # Migrate admin
    af = DATA_DIR / "admin.json"
    if af.exists():
        admin_data = json.loads(af.read_text("utf-8"))
        db.admin.update_one({"_id": "config"}, {"$set": admin_data}, upsert=True)
        print("Admin settings migrated.")

    # Migrate subs
    sf = DATA_DIR / "subscriptions.json"
    if sf.exists():
        subs_data = json.loads(sf.read_text("utf-8"))
        db.state.update_one({"_id": "subscriptions"}, {"$set": {"data": subs_data}}, upsert=True)
        print("Subscriptions migrated.")

    # Migrate pending
    pf = DATA_DIR / "pending_payments.json"
    if pf.exists():
        pend_data = json.loads(pf.read_text("utf-8"))
        db.state.update_one({"_id": "pending_payments"}, {"$set": {"data": pend_data}}, upsert=True)
        print("Pending payments migrated.")

    # Migrate users
    for uf in DATA_DIR.glob("*.json"):
        if uf.name in ["admin.json", "subscriptions.json", "pending_payments.json"]:
            continue
        uid = uf.stem
        try:
            udata = json.loads(uf.read_text("utf-8"))
            db.users.update_one({"_id": uid}, {"$set": udata}, upsert=True)
            print(f"User {uid} migrated.")
        except Exception as e:
            print(f"Error migrating {uid}: {e}")

print("Migration completed!")
