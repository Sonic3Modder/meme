import streamlit as st
import requests

st.title("I have ur ip")
st.image("IP.png")
st.subheader("run. set ur computer on fire. enjoy.")


try:
	# Get visitor's IP
        client_ip = st.query_params().get('client_ip', ['unknown'])[0]
        st.write('Client IP:', client_ip)

        # Append IP to ips.txt
        with open("ips.txt", "a") as file:
            file.write(client_ip + "\n")
        
        st.write("Your IP has been saved in ips.txt")
except Exception as e:
        st.error(f"Error retrieving or saving IP: {e}")
