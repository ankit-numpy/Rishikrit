import streamlit as st

# Page configuration
st.set_page_config(page_title="Rishikrit Honey", page_icon="🍯", layout="wide")

# ---- LOGO ----
st.image("image/logo.png", width=120)  # Place your logo in the "image" folder

# ---- Horizontal Navigation ----
st.markdown(
    """
    <style>
    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .nav-buttons button {
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        background-color: #f4c542;
        font-weight: bold;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "Home"

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
with col2:
    if st.button("🍯 Product"):
        st.session_state.page = "Product"
with col3:
    if st.button("🛒 Order"):
        st.session_state.page = "Order"

# Common header
st.markdown("<h1 style='text-align: center;'>Rishikrit 🍯</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Pure. Natural. Divine.</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---- Pages ----
# Home Page
if st.session_state.page == "Home":
    st.image("image/home.jpg", caption="Pure Rishikrit Honey", use_column_width=True)  # Local image
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
elif st.session_state.page == "Product":
    st.markdown("## Our Products")
    cols = st.columns(3)

    products = [
        {"name": "Forest Raw Honey", "price": "₹499 / 500g", "img": "image/forest_raw_honey.jpg"},
        {"name": "Wildflower Honey", "price": "₹599 / 500g", "img": "image/wildflower_honey.jpg"},
        {"name": "Himalayan Honey", "price": "₹699 / 500g", "img": "image/himalayan_honey.jpg"},
    ]

    for i, prod in enumerate(products):
        with cols[i]:
            st.image(prod["img"], use_column_width=True)
            st.markdown(f"**{prod['name']}**")
            st.markdown(f"*Price:* {prod['price']}")

# Order Page
elif st.session_state.page == "Order":
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


