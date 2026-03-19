"""
Author      : Jimmy LAM
github      : https://github.com/jimmylamcpnv/pre-tpi
Date        : 05.02.2026
Version     : v1

Description : Make a web app in streamlit for a warranty checker/monitoring with camera ocr
website     : serial-guard.streamlit.app
"""

# import
import database, ocr
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

############## TODO ##############
#todo : login page
#todo : if not logged, you can't use features like : export data, add devices, users or tags, 
#todo : you only can monitor existing datas

# tests variables to simule datas
users = database.get_username()
all_devices_name = database.all_devices_name()
unique_devices_name = list(set(all_devices_name))
#todo: export button ton csv with tags to for filtering, settings menu for default tags

####################################
############## Header ##############
####################################
with st.container(border=True, horizontal=True, vertical_alignment="bottom"):
    header_left, header_right = st.columns([7.3,2], vertical_alignment="center")
    with header_left:
        title = st.markdown("""
            <div style="text-align:left;">
                <div style="font-size:28px; font-weight:700;">Serial Guard</div>
                <div style="font-size:14px; margin-top:4px; margin-bottom:10px">Monitor warranties and serial numbers</div>
            </div>
        """, unsafe_allow_html=True)
    with header_right:
        if st.button(f"Scan Device", icon="📷", type="primary"):
            ocr.ocr()

####################################
############## Status ##############
####################################

# Status's Cards
card_left, card_middle, card_right = st.columns(3, border=False)

with card_left:
    if st.button("(4) Active Warranties ✅", use_container_width=True):
        pass

with card_middle:
    if st.button("(4) Expiring soon ⏰", use_container_width=True):
        pass

with card_right:
    if st.button("(4) Expired ❌", use_container_width=True):
        pass
        
####################################
############## Search ##############
####################################

with st.container(border=True, vertical_alignment="center"):
# Create a search column with border
    search_column, download_button = st.columns([6.65,1.01], vertical_alignment="bottom")

    # Display the input bar in the "search_column"
    with search_column:
        # search_options is the selected options
        search_options = st.multiselect(
            # Texte
            "Search by name, serial number, user, etc...",
            unique_devices_name,
            accept_new_options=True,
        )

    # A download button to export all datas with actual filter from multiselect into a csv
    with download_button:
        @st.cache_data
        def get_data():
            df = pd.DataFrame(
                np.random.randn(50, 20), columns=("col %d" % i for i in range(20))
            )
            return df

        @st.cache_data
        def convert_for_download(df):
            return df.to_csv().encode("utf-8")

        df = get_data()
        csv = convert_for_download(df)

        st.download_button(
            label="CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv",
            icon=":material/download:",
        )

#########################################
############## Add devices ##############
#########################################
# a dialog's function to add a device manually with the serial number
# et ça rempli certains champs automatiquement  
@st.dialog("Enter the serial number")
def serial_number_auto_add(serial_number):

    #todo : faire en sorte de ajouter un nouvel apparil avec seulement le numero de série 
    #todo : et ça fait quand meme la recherche via api ou scrapping
    #todo : et ça rempli le reste automatiquemenet, mais si ya aucune données, on rempli quand meme manuellement

    with st.form("test", border=False):
        # Inputs form
        serial_number = st.text_input("Serial Number *")

        with st.container(horizontal_alignment="right"):
            st.form_submit_button()


# dialog's function (remplace st.popover + st.form)
@st.dialog("Add a new device")
def add_manually_device_dialog():
    with st.form("Add device", border=False):

        # Inputs form
        device_name = st.multiselect("Device Name *", ["Dell 14", "Dell 16"], max_selections=1)
        serial_number = st.text_input("Serial Number *")
        manufacturer = st.text_input("Manufacturer")
        assigned_user = st.multiselect("Assigned user", users, max_selections=1)
        tags = st.multiselect("Tags", ["1", "2"], accept_new_options=True)
        purchase_date = st.date_input(format="DD/MM/YYYY", label="Purchase Date")
        warranty_period = st.multiselect(
            "Warranty Period (months)",
            ["6 months", "12 months", "24 months", "36 months", "48 months"],
            max_selections=1,
            default="48 months"
        )

        # Validate and convert for the database
        submitted = st.form_submit_button("Add device")

        if submitted:
            name_val = (device_name[0] if device_name else "").strip() #.strip to remove spaces before and after
            serial_val = (serial_number or "").strip()
            
            # convert lists to strings or integer
            assigned_user_str = (assigned_user[0] if assigned_user else "") # str
            warranty_period_val = (int(warranty_period[0].split()[0]) if warranty_period else 0)  # int

            if not name_val:
                st.error("Device Name can not be empty.", icon="🚨")
            if not serial_val:
                st.error("Serial Number can not be empty.", icon="🚨")

            else:
                st.success("Appareil ajouté.")

            
            # add user in the db
            database.add_user(assigned_user_str)

            # call the function to add device if valid
            database.add_device(
            name_val,
            serial_val,
            manufacturer,
            assigned_user_str,
            tags,
            purchase_date,
            warranty_period_val
            )


# column without border
with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="bottom"):

    # Display the number of all devices
    all_device = st.subheader(f"All devices ({database.total_devices()})")

    # Button to call the function 
    if st.button("➕ Add Manually"):
        add_manually_device_dialog()

#############################################
############## Display devices ##############
#############################################
items = database.search_devices(search_options)

# modify function
# dialog's function (remplace st.popover + st.form)
@st.dialog("Modify Device")
def show_device_info():
    pass
    #todo
    
@st.dialog("Modify Device")
def modify_device_dialog():
    with st.form("test", border=False):

        # Inputs form
        device_name = st.multiselect("Device Name *", ["Dell 14", "Dell 16"], max_selections=1)
        serial_number = st.text_input("Serial Number *")
        manufacturerst = st.text_input("Manufacturer")
        assigned_user = st.multiselect("Assigned user", users, max_selections=1)
        tags = st.multiselect("Tags", ["1", "2"], accept_new_options=True)
        date = st.date_input(format="DD/MM/YYYY", label="Purchase Date (DD-MM-YYYY)")
        warranty_period = st.multiselect(
            "Warranty Period (months)",
            ["6 months", "12 months", "24 months", "36 months", "48 months"],
            max_selections=1,
            default="48 months"
        )

        # to do
        # if the serial number is already in the db or not --> message "already in"


        # submit button
        submitted = st.form_submit_button("Add device")
        if submitted:
            name_val = (device_name[0] if device_name else "").strip()
            serial_val = (serial_number or "").strip()

            if not name_val:
                st.warning("Device Name est obligatoire.")
            if not serial_val:
                st.warning("Serial Number est obligatoire.")

            else:
                st.success("Appareil ajouté.")
                st.rerun()  # close the dialog to force the rerun

def days_left(purchase_date, warranty_months):
    if not purchase_date:
        return 0

    d = datetime.strptime(purchase_date, "%Y-%m-%d").date()

    # ajouter les mois
    y = d.year + (d.month - 1 + warranty_months) // 12
    m = (d.month - 1 + warranty_months) % 12 + 1

    end_date = date(y, m, d.day)

    return max(0, (end_date - date.today()).days)

# devices cards (where informations like device name, serial number are shown)
with st.container(border=False, height=600):
    for item in items:
        # outer "card" container with border
        devices_infos_container, = st.columns(1, border=True)

        with devices_infos_container:
            # two columns: left for text/badge, right for the button
            left, right = st.columns([3, 1], vertical_alignment="center", border=False)

            with left:
                with st.container(horizontal=True, border=False): # device name container
                    st.badge(item["serial_number"], color="violet")
                    st.write(item["device_name"])
                    
                with st.container(horizontal=True): # tags container
                    st.badge(item["assigned_user"] or "Unassigned", color="blue")
                    st.badge("Expiring soon", icon="🕑", color="red")
                    st.badge(f"{days_left(item["purchase_date"], item["warranty_period"])} days left", color="gray")
                    st.badge(datetime.strptime(item["purchase_date"], "%Y-%m-%d").strftime("%d-%m-%Y") if item["purchase_date"] else "None", color="grey")    

            with right:
                with st.container(horizontal=True, border=False):
                    # horizontal container to right-align the button inside the column
                    with st.container(horizontal=False, horizontal_alignment="right"):
                        if st.button("modify",
                            icon="📝",
                            key=f"open_{item}",  # unique per item
                            type="secondary",
                        ):
                            modify_device_dialog()
                            pass