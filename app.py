import streamlit as st
from ingest import collection
st.title("Construction specification search")
division=st.sidebar.text_input("Division (blank for all)")
question=st.text_input("Question")
if question:
 c=collection()
 if c.count()==0:st.info("Ingest specifications first.")
 else:
  result=c.query(query_texts=[question],n_results=min(5,c.count()),where={"division":division} if division else None)
  found=False
  for text,metadata,distance in zip(result["documents"][0],result["metadatas"][0],result["distances"][0]):
   if distance>.65:continue
   found=True;st.write(text);st.caption(f'{metadata["source"]}, page {metadata["page"]}, {metadata["section"]}')
  if not found:st.write("Not found in the documents.")
