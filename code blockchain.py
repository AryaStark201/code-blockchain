# Save this as blockchain_diary_app.py
import streamlit as st
import hashlib
import json
from time import time

# ---------------- Blockchain Class ---------------- #
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_entries = []
        # Genesis block
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'entries': self.pending_entries,
            'previous_hash': previous_hash,
        }
        block['hash'] = self.hash(block)
        self.pending_entries = []
        self.chain.append(block)
        return block

    def add_entry(self, entry_text):
        self.pending_entries.append({
            'entry': entry_text
        })
        return True

    @staticmethod
    def hash(block):
        # Hash block without 'hash' key
        block_string = json.dumps({k: block[k] for k in block if k != 'hash'}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Blockchain Diary App", layout="wide")
st.title("📔 Blockchain Diary System")
st.markdown("This diary stores your daily entries permanently on a blockchain. Once written, entries cannot be modified.")

# Initialize blockchain
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

menu = ["Add Diary Entry", "Mine Block", "View Diary Timeline"]
choice = st.sidebar.selectbox("Menu", menu)

# 1. Add Diary Entry
if choice == "Add Diary Entry":
    st.subheader("Write Your Daily Entry")
    entry_text = st.text_area("What did you learn or experience today?")
    if st.button("Add Entry"):
        if entry_text.strip() != "":
            st.session_state.blockchain.add_entry(entry_text.strip())
            st.success("Entry added successfully! Mine it into a block to make it permanent.")
        else:
            st.error("Please write something before adding.")

# 2. Mine Block
elif choice == "Mine Block":
    st.subheader("Mine Pending Entries into a Block")
    if st.button("Mine Block"):
        if st.session_state.blockchain.pending_entries:
            previous_hash = st.session_state.blockchain.get_last_block()['hash']
            block = st.session_state.blockchain.create_block(previous_hash)
            st.success(f"Block #{block['index']} mined successfully! All entries are now permanent.")
            st.json(block)
        else:
            st.warning("No pending entries to mine.")

# 3. View Diary Timeline
elif choice == "View Diary Timeline":
    st.subheader("Diary Timeline (Immutable Entries)")
    for block in st.session_state.blockchain.chain:
        st.markdown(f"### Block #{block['index']}")
        st.write(f"Timestamp: {block['timestamp']}")
        st.write(f"Previous Hash: {block['previous_hash']}")
        st.write(f"Hash: {block['hash']}")
        st.write("Entries:")
        for entry in block['entries']:
            st.write(f"- {entry['entry']}")
