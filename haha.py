import streamlit as st
import requests

st.title("I have ur ip")
st.image("IP.png")
st.subheader("run. set ur computer on fire. enjoy.")


try:
	# Get visitor's IP
        ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        st.success(f"Your IP address: {ip}")

        # Append IP to ips.txt
        with open("ips.txt", "a") as file:
            file.write(ip + "\n")
        
        st.write("Your IP has been saved in ips.txt")
except Exception as e:
        st.error(f"Error retrieving or saving IP: {e}")
