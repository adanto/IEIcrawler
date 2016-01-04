<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/root/festivales">

		<festivales>
			<xsl:for-each select="child::node()">
				<festival>
					<name>
						<xsl:value-of select="name"/>
					</name>
					<price>
						<xsl:value-of select="price"/>
					</price>
					<startDate>
						<xsl:value-of select="startDate"/>
					</startDate>
					<endDate>
						<xsl:value-of select="endDate"/>
					</endDate>
					<url>
						<xsl:value-of select="url"/>						
					</url>
					<location>
						<coordinates>
							<longitude>
								<xsl:value-of select="position/longitude"/>
							</longitude>
							<latitude>
								<xsl:value-of select="position/latitude"/>
							</latitude>
						</coordinates>
						<address>
							<city>
								<xsl:value-of select="address/city"/>
							</city>
							<address>
								<xsl:value-of select="address/address"/>
							</address>
							<postalCode>
								<xsl:value-of select="address/postalCode"/>
							</postalCode>
						</address>
					</location>
					<styles>
						<xsl:for-each select="styles/item">
							<style>
								<xsl:value-of select="node()"/>
							</style>
						</xsl:for-each>
					</styles>
					<lineup>
						<xsl:for-each select="lineup/item">
							<artist>
								<xsl:value-of select="node()"/>
							</artist>
						</xsl:for-each>
					</lineup>
				</festival>
			</xsl:for-each>
		</festivales>


	</xsl:template>
</xsl:stylesheet>
