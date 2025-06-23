import streamlit as st
import pandas as pd
import cloudpickle

@st.cache_resource
def load_model():
    try:
        with open("models/final_pipelineY.pkl", "rb") as f:
            return cloudpickle.load(f)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

model = load_model()

st.title("Gene Mutation Classifier")

all_cols = ['CHROM', 'POS', 'REF', 'ALT', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'CLNDISDB',
            'CLNDN', 'CLNHGVS', 'CLNVC', 'MC', 'ORIGIN', 'CLASS', 'Allele', 'Consequence',
            'IMPACT', 'SYMBOL', 'Feature_type', 'Feature', 'BIOTYPE', 'EXON', 'cDNA_position',
            'CDS_position', 'Protein_position', 'Amino_acids', 'Codons', 'STRAND', 'BAM_EDIT',
            'SIFT', 'PolyPhen', 'LoFtool', 'CADD_PHRED', 'CADD_RAW', 'BLOSUM62']

target = 'PolyPhen'
input_cols = [c for c in all_cols if c != target]

inputs = {}

numerical_cols = ['POS', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'ORIGIN', 'CLASS', 'STRAND', 'LoFtool',
                  'CADD_PHRED', 'CADD_RAW', 'BLOSUM62']
categorical_cols = [c for c in input_cols if c not in numerical_cols]

st.header("Numerical Features")
for col in numerical_cols:
    inputs[col] = st.number_input(col, value=0.0, format="%.6f")

st.header("Categorical Features")
for col in categorical_cols:
    inputs[col] = st.text_input(col, "")

if st.button("Predict"):
    input_df = pd.DataFrame([inputs])
    input_df = input_df[input_cols]
    if model:
        prediction = model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)
        st.subheader("Prediction Result")
        label = "Benign" if prediction[0] == 0 else "Pathogenic"
        st.write(f"Predicted PolyPhen class: {label}")
    else:
        st.error("Model not loaded. Please check the file path or model format.")
