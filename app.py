import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Page Replacement Simulator", layout="wide")

st.title("Page Replacement Algorithm Simulator")

# Sidebar Inputs
algo = st.sidebar.selectbox(
    "Select Algorithm",
    ["FIFO", "LRU", "Optimal"]
)

frames = st.sidebar.number_input(
    "Number of Frames",
    min_value=1,
    max_value=10,
    value=3
)

page_input = st.sidebar.text_input(
    "Page References (comma-separated)",
    "1,2,3,4,1,2,5,1,2,3"
)

try:
    pages = list(map(int, page_input.strip().split(',')))
except:
    st.error("Please enter valid comma-separated integers.")
    st.stop()

# FIFO Algorithm
def fifo(pages, frames):
    queue = []
    faults = 0
    history = []
    fault_idx = []

    for i, page in enumerate(pages):
        if page not in queue:
            if len(queue) < frames:
                queue.append(page)
            else:
                queue.pop(0)
                queue.append(page)

            faults += 1
            fault_idx.append(i)

        history.append(queue.copy())

    return history, faults, fault_idx


# LRU Algorithm
def lru(pages, frames):
    queue = []
    recent = {}
    faults = 0
    history = []
    fault_idx = []

    for i, page in enumerate(pages):

        if page in queue:
            recent[page] = i

        else:
            if len(queue) < frames:
                queue.append(page)

            else:
                lru_page = min(queue, key=lambda x: recent.get(x, -1))
                queue[queue.index(lru_page)] = page

            recent[page] = i
            faults += 1
            fault_idx.append(i)

        history.append(queue.copy())

    return history, faults, fault_idx


# Optimal Algorithm
def optimal(pages, frames):
    queue = []
    faults = 0
    history = []
    fault_idx = []

    for i in range(len(pages)):
        page = pages[i]

        if page not in queue:

            if len(queue) < frames:
                queue.append(page)

            else:
                future = pages[i + 1:]

                indices = [
                    future.index(p) if p in future else float('inf')
                    for p in queue
                ]

                replace_index = indices.index(max(indices))
                queue[replace_index] = page

            faults += 1
            fault_idx.append(i)

        history.append(queue.copy())

    return history, faults, fault_idx


# Run Simulation
if st.button("Run Simulation"):

    if algo == "FIFO":
        history, faults, fault_idx = fifo(pages, frames)

    elif algo == "LRU":
        history, faults, fault_idx = lru(pages, frames)

    else:
        history, faults, fault_idx = optimal(pages, frames)

    st.success(f"Total Page Faults: {faults}")

    # Table Output
    table = []

    for i, frame_state in enumerate(history):

        row = {
            "Step": i + 1,
            "Page": pages[i],
            "Status": "❌ Fault" if i in fault_idx else "✅ Hit"
        }

        for j in range(frames):
            row[f"Frame {j+1}"] = (
                frame_state[j] if j < len(frame_state) else "-"
            )

        table.append(row)

    df = pd.DataFrame(table)

    st.dataframe(df, use_container_width=True)

    # Chart
    fig, ax = plt.subplots()

    colors = [
        'red' if i in fault_idx else 'green'
        for i in range(len(history))
    ]

    ax.bar(range(len(pages)), [1]*len(pages), color=colors)

    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Events")
    ax.set_title(f"{algo} Page Replacement")

    st.pyplot(fig)