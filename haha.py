import streamlit as st
import requests

st.title("I have ur ip")
st.image("IP.png")
st.subheader("run. set ur computer on fire. enjoy.")

# This returns a dict-like object
query_params = st.experimental_get_query_params()

# Example: retrieve 'client_ip' parameter if present
client_ip = query_params.get('client_ip', ['unknown'])[0]

st.write('Client IP:', client_ip)


        # Append IP to ips.txt
with open("ips.txt", "a") as file:
            file.write(client_ip + "\n")
        
st.write("Your IP has been saved in ips.txt")
        