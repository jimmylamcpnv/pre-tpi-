#############################################
############## Display devices ##############
#############################################

# "items" will chose one of these list if not empty
# so by default, all devices will be displayed, then when we will choose a tag
items = search_options or devices_list

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

            errors = []
            if not name_val:
                errors.append("Device Name est obligatoire.")
            if not serial_val:
                errors.append("Serial Number est obligatoire.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.success("Appareil ajouté.")
                st.rerun()  # close the dialog to force the rerun

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
                    st.badge("1234", color="violet")
                    st.write(item)
                    
                with st.container(horizontal=True): # tags container
                    st.badge("Carlos", color="gray")
                    st.badge("Expiring soon", icon="🕑", color="red")
                    st.badge("12 days left", color="blue")
                    
                    # st.badge("14/04/2022 - 14/04/2026")    

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