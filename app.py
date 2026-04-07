import streamlit as st
from pathlib import Path
import tempfile
import pandas as pd

from payment_detail import PaymentDetail
from payment_summary import PaymentSummary

st.set_page_config(page_title="Payment Reports → FYBoard", layout="wide")
st.title("Payment Reports → FYBoard")

st.write("Upload Payment Detail / Payment Summary files (.msg or .pdf).")

uploads = st.file_uploader(
    "Upload files",
    type=["msg", "pdf"],
    accept_multiple_files=True
)

def save_upload_to_temp(upload) -> Path:
    # preserve extension
    suffix = "." + upload.name.split(".")[-1].lower()
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    p = Path(tmp_path)
    with open(p, "wb") as f:
        f.write(upload.getbuffer())
    return p

def parse_inputs(files):
    payment_summary = PaymentSummary()
    payment_details = []

    for up in files:
        p = save_upload_to_temp(up)
        name_lower = up.name.lower()

        # Decide what it is based on filename
        is_summary = ("payment" in name_lower and "summary" in name_lower)
        is_detail  = ("payment" in name_lower and "detail" in name_lower)

        # If user uploads PDFs directly, use load_from_pdf
        if p.suffix.lower() == ".pdf":
            if is_summary:
                payment_summary.load_from_pdf(str(p))
            elif is_detail:
                d = PaymentDetail()
                d.load_from_pdf(str(p))
                payment_details.append(d)
            else:
                st.warning(f"Skipping PDF (can't classify): {up.name}")

        # If user uploads MSG emails, use load_from_email (your current path)
        elif p.suffix.lower() == ".msg":
            if is_summary:
                payment_summary.load_from_email(str(p))
            elif is_detail:
                d = PaymentDetail()
                d.load_from_email(str(p))
                payment_details.append(d)
            else:
                st.warning(f"Skipping MSG (can't classify): {up.name}")

    # Build the same df your script builds
    dfs = [d.to_df() for d in payment_details]
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        totals = df.select_dtypes("number").sum()
        totals_df = totals.to_frame().T
        totals_df.insert(0, df.columns[0], "{Payment Detail Totals}")
        df = pd.concat([df, totals_df], ignore_index=True)
    else:
        df = pd.DataFrame()

    # Add the payment summary line (same as your script)
    df = pd.concat([df, payment_summary.to_df()], ignore_index=True)
    return df

if uploads:
    if st.button("Run conversion"):
        with st.spinner("Parsing…"):
            df = parse_inputs(uploads)
            st.session_state["df"] = df

if "df" in st.session_state:
    df = st.session_state["df"]
    st.subheader("Preview")
    st.dataframe(df, use_container_width=True)

    csv_bytes = df.round(2).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download output.csv",
        data=csv_bytes,
        file_name="output.csv",
        mime="text/csv"
    )