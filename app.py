import streamlit as st
import pandas as pd
from googletrans import Translator
from pandas import ExcelWriter
translate = Translator()

@st.cache
def en_xx(text,target_language):
	out = translate.translate(text=text,dest=target_language)
	return out.text

languages = ('en_IN','hi_IN','mr_IN','tl_IN','ta_IN','gu_IN','bn_IN')
filetypes = ('Excel', 'Excel With Multiple Sheet', 'CSV')


def  process_csv(uploaded_file):
	# Can be usd wherever a "file-like" object is accepted:
	df = pd.read_csv(uploaded_file)
	for column in df.columns:
		df[column] = df[column].apply(lambda x : en_xx(x,'hi'))	
	st.write(df)

def process_xl(uploaded_file):
	# Can be usd wherever a "file-like" object is accepted:
	file = pd.ExcelFile(uploaded_file)
	sheets = file.sheet_names
	with ExcelWriter('output.xlsx') as writer:
		for sheet in sheets:
			df = pd.read_excel(uploaded_file,sheet_name=sheet)
			for column in df.columns:
				df[column] = df[column].apply(lambda x : en_xx(x,'hi'))	
				df.to_excel(writer,sheet_name=sheet)
			st.write(df)
		writer.save()
			

# Add a selectbox to the sidebar:
lang = st.selectbox(
    'Select Language',
    languages
)

uploaded_file = st.file_uploader("Upload a CSV or Excel file (.csv or .xlsx)")
if uploaded_file is not None:
	ex = str(uploaded_file.name).split('.')[1]
	if ex=='csv':
		process_csv(uploaded_file)
	elif ex=='xlsx':
		process_xl(uploaded_file)
	else:
		st.write("File Not Supported \n File supported are: CSV and Excel")
	
