import streamlit as st
import pandas as pd
import joblib
import cloudpickle

# Load pipeline (cached for performance)
def load_model():
    with open(r"C:\Users\Anmol\OneDrive\Desktop\Gene-Mutation\models\final_pipelineY.pkl", "rb") as f:
        return cloudpickle.load(f)

model = load_model()

# All columns including target
all_cols = ['CHROM', 'POS', 'REF', 'ALT', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'CLNDISDB',
            'CLNDN', 'CLNHGVS', 'CLNVC', 'MC', 'ORIGIN', 'CLASS', 'Allele', 'Consequence',
            'IMPACT', 'SYMBOL', 'Feature_type', 'Feature', 'BIOTYPE', 'EXON', 'cDNA_position',
            'CDS_position', 'Protein_position', 'Amino_acids', 'Codons', 'STRAND', 'BAM_EDIT',
            'SIFT', 'PolyPhen', 'LoFtool', 'CADD_PHRED', 'CADD_RAW', 'BLOSUM62']

target = 'PolyPhen'
input_cols = [c for c in all_cols if c != target]

st.title("Predict PolyPhen using your Pipeline")

# Prepare input dictionary
inputs = {}

# You can customize input types here based on your knowledge of each feature:
numerical_cols = ['POS', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'ORIGIN', 'CLASS', 'STRAND', 'LoFtool',
                  'CADD_PHRED', 'CADD_RAW', 'BLOSUM62']
categorical_cols = [c for c in input_cols if c not in numerical_cols]

st.header("Numerical Features")
for col in numerical_cols:
    inputs[col] = st.number_input(col, value=0.0, format="%.6f")

st.header("Categorical Features")
for col in categorical_cols:
    inputs[col] = st.text_input(col, "")

# When button is clicked:
if st.button("Predict"):
    # Create DataFrame for prediction
    input_df = pd.DataFrame([inputs])

    # Reorder columns as required
    input_df = input_df[input_cols]

    # Predict with pipeline
    prediction = model.predict(input_df)
    prediction_proba = model.predict_proba(input_df)

    st.subheader("Prediction Result")
    if prediction[0] == 0:
        st.write("Predicted PolyPhen class: Benign")
    else:
        st.write("Predicted PolyPhen class: Pathogenic")

