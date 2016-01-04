<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/root/festivales">
  <html>
  <body>

    <h1>Festivales</h1>

    <xsl:for-each select="child::node()">

      <h3>
        Name: <xsl:value-of select="name"/>
      </h3>

      <p>
        <xsl:value-of select="description"/>
      </p>

      <p>
        Position: (<xsl:value-of select="position/latitude"/>, <xsl:value-of select="position/longitude"/>) 
      </p>

      <p>
        url: <xsl:value-of select="url"/>
      </p>

      <p>
        price: <xsl:value-of select="price"/>
      </p>

      <p>
        id: <xsl:value-of select="id"/>
      </p>

      <p>
        startDate: <xsl:value-of select="startDate"/>
      </p>

      <p>
        endDate: <xsl:value-of select="endDate"/>
      </p>

      <p>
        lineup: 
        <xsl:for-each select="child::lineup/item">
          <xsl:value-of select="node()"/>,
        </xsl:for-each>
      </p>

      <p>
        styles: 
        <xsl:for-each select="child::styles/item">
          <xsl:value-of select="node()"/>,
        </xsl:for-each>
      </p>

      <p>
        address: <xsl:value-of select="address/address"/>, PC:<xsl:value-of select="address/postalCode"/> (<xsl:value-of select="address/city"/>)
      </p>



    </xsl:for-each>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>

