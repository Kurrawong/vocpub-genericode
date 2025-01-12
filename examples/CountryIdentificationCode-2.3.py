from vocpub_genericode.model import CodeList, ColumnSet, SimpleCodeList, Column, Key, Identification, \
    AlternateFormatLocationUri, LongName, Agency, Identifier
from rdflib.namespace import XSD
from lxml import etree


i = Identification(
    "UnitOfMeasureCode",
    long_names = [
        LongName("Unit Of Measure Code", language="en"),
        LongName("UNECE Recommendation N°. 20 - Codes for Units of Measure Used in International Trade",
                 identifier="listID")
    ],
    version="12e_2016",
    canonical_uri="urn:oasis:names:specification:ubl:codelist:gc:UnitOfMeasureCode",
    canonical_version_uri="urn:oasis:names:specification:ubl:codelist:gc:UnitOfMeasureCode:2.3",
    location_uris=[
        "http://docs.oasis-open.org/ubl/os-UBL-2.3/cl/gc/default/UnitOfMeasureCode-2.3.gc"
    ],
    alternative_location_uris=[
        AlternateFormatLocationUri(
            "jar:https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20.zip!/rec20/rec20_Rev13e_2017.xls",
            mime_type="application/vnd.ms-excel"
        )
    ],
    publisher=Agency(
        long_name=LongName("United Nations Economic Commission for Europe", language="en"),
        identifier=Identifier("6", identifier="http://www.unece.org/trade/untdid/d18a/tred/tred3055.htm")
    )
)
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
c1 = Column(identifier="code", datatype=XSD.normalizedString, identification=Identification(short_name="Code"), language="en", required=True)
c2 = Column(identifier="name", datatype=XSD.string, identification=Identification(short_name="Name",  language="en"))
c3 = Column(identifier="numericcode", datatype=XSD.integer, identification=Identification(short_name="NumericCode"))
c4 = Column(
    identifier="french",
    datatype=XSD.string,
    identification=Identification(
        short_name="French"),
    language="fr"
)
c5 = Column(identifier="ref", datatype=XSD.string, identification=Identification(short_name="CrossReference", language="en"))
"""
      <Key Id="codeKey">
         <ShortName>CodeKey</ShortName>
         <ColumnRef Ref="code"/>
      </Key>
"""
cs = ColumnSet(
    columns=[c1, c2, c3, c4, c5],
    keys=[Key(identifier="codeKey", identification=Identification(short_name="CodeKey"), columns=[c1])]
)

cl = CodeList(
    identification=i,
    defined_column_sets=[cs]
)

print(etree.tostring(c1.to_etree(), pretty_print=True).decode())
