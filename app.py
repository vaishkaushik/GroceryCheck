import streamlit as st
import json

st.set_page_config(page_title="Smart Grocery Saver", layout="centered")

# Load data
def load_prices():
    with open("data/prices.json") as f:
        return json.load(f)

# Parse input
def parse_input(text):
    items = []
    for line in text.strip().split("\n"):
        if line.strip():
            parts = line.split()
            if len(parts) == 2:
                items.append((parts[0].lower(), float(parts[1])))
    return items

# Calculate total
def calculate(cart, platform, prices):
    total = 0
    missing = []

    for item, qty in cart:
        if item in prices:
            total += prices[item][platform] * qty
        else:
            missing.append(item)
            total += 50 * qty  # fallback

    return round(total, 2), missing

# UI
st.title("🛒 Smart Grocery Saver")

st.markdown("Enter items like:")
st.code("milk 1\natta 5\ntomato 2")

user_input = st.text_area("Your Grocery List")

if st.button("Compare Prices"):

    prices = load_prices()
    cart = parse_input(user_input)

    if not cart:
        st.warning("Please enter valid items")
    else:
        platforms = ["blinkit", "zepto", "instamart"]
        results = {}

        for p in platforms:
            total, missing = calculate(cart, p, prices)
            results[p] = total

        best = min(results, key=results.get)

        st.subheader("💰 Comparison")

        for k, v in results.items():
            if k == best:
                st.success(f"{k.capitalize()} → ₹{v} ✅ Cheapest")
            else:
                st.write(f"{k.capitalize()} → ₹{v}")

        st.info(f"💡 You can save approx ₹{max(results.values()) - min(results.values())}")