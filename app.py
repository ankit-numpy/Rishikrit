import streamlit as st

# Page configuration
st.set_page_config(page_title="Rishikrit Honey", page_icon="🍯", layout="wide")

# Sidebar navigation
st.sidebar.title("Rishikrit 🍯")
page = st.sidebar.radio("Navigate", ["Home", "Product", "Order"])

# Common header
st.markdown("<h1 style='text-align: center;'>Rishikrit 🍯</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Pure. Natural. Divine.</h4>", unsafe_allow_html=True)
st.markdown("---")

# Home Page
if page == "Home":
    st.image("https://images.unsplash.com/photo-1600431521340-491eca880813", caption="Pure Rishikrit Honey", use_column_width=True)
    st.markdown("""
    ### Welcome to Rishikrit
    At Rishikrit, we believe in the power of nature. Our honey is:
    
    - 🌿 100% pure and organic
    - 🐝 Sourced from local farmers
    - 🧪 Lab-tested for quality
    - 🍯 Packed with nutrients and flavor
    
    Taste the essence of the wild with every drop of Rishikrit Honey.
    """)

# Product Page
elif page == "Product":
    st.markdown("## Our Products")
    cols = st.columns(3)

    products = [
        {"name": "Forest Raw Honey", "price": "₹499 / 500g", "img": "https://images.unsplash.com/photo-1589820296156-2454bb8e1644"},
        {"name": "Wildflower Honey", "price": "₹599 / 500g", "img": "https://images.unsplash.com/photo-1612874742383-9b58175911d3"},
        {"name": "Himalayan Honey", "price": "₹699 / 500g", "img": "https://images.unsplash.com/photo-1612874891433-b9b4b0bbd16e"},
    ]

    for i, prod in enumerate(products):
        with cols[i]:
            st.image(prod["img"], use_column_width=True)
            st.markdown(f"**{prod['name']}**")
            st.markdown(f"*Price:* {prod['price']}")

# Order Page
elif page == "Order":
    st.markdown("## Place Your Order")

    with st.form("order_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        address = st.text_area("Shipping Address")
        product = st.selectbox("Select Product", ["Forest Raw Honey", "Wildflower Honey", "Himalayan Honey"])
        quantity = st.number_input("Quantity", min_value=1, step=1)
        submitted = st.form_submit_button("Submit Order")

        if submitted:
            st.success(f"Thank you, {name}! 🎉\n\nYour order for {quantity} x {product} has been placed.")
