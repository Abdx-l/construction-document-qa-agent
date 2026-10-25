from ingest import sections
def test_headings():
 result=list(sections("SECTION 03 30 00\nConcrete shall be cured.\nPART 2 PRODUCTS\nCement."));assert len(result)==2;assert result[1][0]=="PART 2 PRODUCTS"
