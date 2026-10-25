import re,sys
from pathlib import Path
import fitz,chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
def collection():
 return chromadb.PersistentClient(path="index").get_or_create_collection("specifications",embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2"),metadata={"hnsw:space":"cosine"})
def sections(text):
 heading="General"
 for block in re.split(r"(?m)^(?=\d{2}\s+\d{2}\s+\d{2}|PART\s+\d|SECTION\s)",text):
  lines=block.strip().splitlines()
  if not lines:continue
  if re.match(r"(\d{2}\s|PART|SECTION)",lines[0]):heading=lines[0]
  words=block.split()
  for start in range(0,len(words),450):yield heading," ".join(words[start:start+500])
def ingest(folder):
 c=collection();count=0
 for file in Path(folder).glob("*.pdf"):
  with fitz.open(file) as pdf:
   division="Unknown"
   for number,page in enumerate(pdf,1):
    text=page.get_text();match=re.search(r"(?:DIVISION|SECTION)\s+(\d{2})",text,re.I)
    if match:division=match[1]
    for index,(heading,chunk) in enumerate(sections(text)):
     c.upsert(ids=[f"{file.name}:{number}:{index}"],documents=[chunk],metadatas=[{"division":division,"section":heading,"page":number,"source":file.name}]);count+=1
 return count
if __name__=="__main__":print("Indexed",ingest(sys.argv[1]),"sections")
