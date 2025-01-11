from vocpub_genericode.model import CodeList, ColumnSet, SimpleCodeList, Column, Key
from rdflib.namespace import XSD
from lxml import etree

"""
      <Column Id="code" Use="required">
         <ShortName>Code</ShortName>
         <Data Type="normalizedString" Lang="en"/>
      </Column>
      <Column Id="name" Use="optional">
         <ShortName>Name</ShortName>
         <Data Type="string" Lang="en"/>
      </Column>
      <Column Id="numericcode" Use="optional">
         <ShortName>NumericCode</ShortName>
         <Data Type="integer"/>
      </Column>
      <Column Id="french" Use="optional">
         <ShortName>French</ShortName>
         <Data Type="string" Lang="fr"/>
      </Column>
      <Column Id="ref" Use="optional">
         <ShortName>CrossReference</ShortName>
         <Data Type="string" Lang="en"/>
      </Column>
"""
c1 = Column("code", short_name="Code", datatype=XSD.normalizedString, language="en", required=True)
c2 = Column("name", short_name="Name", datatype=XSD.string, language="en")
c3 = Column("numericcode", short_name="NumericCode", datatype=XSD.integer)
c4 = Column("french", short_name="French", datatype=XSD.string, language="fr")
c5 = Column("ref", short_name="CrossReference", datatype=XSD.string, language="en")

columns = [c1, c2, c3, c4, c5]

"""
      <Key Id="codeKey">
         <ShortName>CodeKey</ShortName>
         <ColumnRef Ref="code"/>
      </Key>
"""
keys = [
    Key("codeKey", short_name="CodeKey", columns=[c1]),
]

print(etree.tostring(c1.to_etree(), pretty_print=True).decode())
