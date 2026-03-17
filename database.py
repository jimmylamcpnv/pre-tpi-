import os
from supabase import create_client, Client
import streamlit as st
from typing import Iterable

# -----------
# Initializing
# -----------
url = "https://nsbfvaghqvgdiiizclst.supabase.co"
key = "sb_publishable_uN4WtLAtQWu3AoeTbKZQpA_USXH8wsM"
supabase: Client = create_client(url, key)

# ------------
# Devices
# ------------
def delete_device(serial_number):
    respons = (
        supabase.table("devices")
        .delete()
        .eq("serial_number", serial_number)
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

# ------------
# Users
# ------------

def delete_user(user_name):
    respons = (
        supabase.table("users")
        .delete()
        .eq("user_name", user_name)
        .execute()
    )
    return respons

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

def get_username():
    response = (
        supabase.table("users")
        .select("*")
        .execute()
    )
    usernames = [user["user_name"] for user in response.data]
    return usernames

# def search devices
def search_devices(keywords: Iterable[str]): # Iterable[str] = ["Dell", "Carlos"] or ("Dell", "Carlos") are accepted
    # Nettoyage des mots-clés
    words = [w.strip() for w in keywords if w and w.strip()]
    
    query = supabase.table("devices").select(
        "device_name, serial_number, manufacturer, assigned_user, tags, purchase_date, warranty_period"
    )

    if words:
        filters = []

        for word in words:
            escaped = word.replace(",", r"\,")  # évite de casser le or_ si virgule
            filters.extend([
                f"device_name.ilike.%{escaped}%",
                f"serial_number.ilike.%{escaped}%",
                f"manufacturer.ilike.%{escaped}%",
                f"assigned_user.ilike.%{escaped}%",
            ])

        query = query.or_(",".join(filters))

    response = query.execute()
    return response.data

# def number total devices
def total_devices():
    response = (
        supabase
        .table("devices")
        .select("*", count="exact")
        .execute()
    )
    
    return response.count

# def all devices name
def all_devices_name():
    response = (
        supabase
        .table("devices")
        .select("device_name")
        .execute()
    )
    
    return [device["device_name"] for device in response.data]