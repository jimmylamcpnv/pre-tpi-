import os
from supabase import create_client, Client
import streamlit as st

# -----------
# Initializing
# -----------
url = "https://nsbfvaghqvgdiiizclst.supabase.co"
key = "sb_publishable_uN4WtLAtQWu3AoeTbKZQpA_USXH8wsM"
supabase: Client = create_client(url, key)

def delete_device(serial_number):
    respons = (
        supabase.table("countries")
        .delete()
        .eq("id", 1)
        .execute()
    )
    return respons

def add_device(name_val,
               serial_val,
               manufacturer,
               assigned_user_str,
               tags,
               purchase_date,
               warranty_period_val):

    data = {
        "device_name": name_val,
        "serial_number": serial_val,
        "manufacturer": manufacturer,
        "assigned_user": assigned_user_str,
        "tags": tags,
        "purchase_date": purchase_date.isoformat() if purchase_date else None,
        "warranty_period": warranty_period_val
    }

    response = supabase.table("devices").insert(data).execute()
    return response

def add_user(user_name):

    data = {
        "user_name": user_name
    }

    response = (
        supabase
        .table("users")
        .upsert(data, on_conflict="user_name") # add if not exist
        .execute()
    )

    return response