<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:input="http://www.onderzoekinformatie.nl/nod/org"
                xmlns="https://www.openaire.eu/cerif-profile/1.1/"
                exclude-result-prefixes="input xsi"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.onderzoekinformatie.nl/nod/org ../xsd/nod-organisation-1-1.xsd"
                version="1.0">

    <!-- =================================================================================== -->
    <xsl:output encoding="UTF-8" indent="yes" method="xml" omit-xml-declaration="yes"/>
    <!-- =================================================================================== -->

    <!-- variable -->

    <xsl:template match="/">
        <OrgUnit>
            <xsl:attribute name="id">
                <xsl:value-of select="input:organisatie/input:identifier"/>
            </xsl:attribute>

            <xsl:if test="input:organisatie/input:acroniem">
                <Acronym>
                    <xsl:value-of select="input:organisatie/input:acroniem"/>
                </Acronym>
            </xsl:if>

            <xsl:if test="input:organisatie/input:naam_nl">
                <Name xml:lang="nl">
                    <xsl:value-of select="input:organisatie/input:naam_nl"/>
                </Name>
            </xsl:if>

            <xsl:if test="input:organisatie/input:naam_en">
                <Name xml:lang="en">
                    <xsl:value-of select="input:organisatie/input:naam_en"/>
                </Name>
            </xsl:if>

            <xsl:if test="input:organisatie/input:org_telefoon">
                <ElectronicAddress>
                    <xsl:value-of select="concat('tel:', input:organisatie/input:org_telefoon)"/>
                </ElectronicAddress>
            </xsl:if>

            <xsl:if test="input:organisatie/input:org_fax">
                <ElectronicAddress>
                    <xsl:value-of select="concat('fax:', input:organisatie/input:org_fax)"/>
                </ElectronicAddress>
            </xsl:if>

            <xsl:if test="input:organisatie/input:org_email">
                <ElectronicAddress>
                    <xsl:value-of select="concat('mailto:', input:organisatie/input:org_email)"/>
                </ElectronicAddress>
            </xsl:if>

            <xsl:if test="input:organisatie/input:org_url">
                <ElectronicAddress>
                    <xsl:value-of select="concat('url:', input:organisatie/input:org_url)"/>
                </ElectronicAddress>
            </xsl:if>

            <xsl:if test="input:organisatie/input:org_parent">
                <PartOf>
                    <OrgUnit>
                        <xsl:attribute name="id">
                            <xsl:value-of select="input:organisatie/input:org_parent"/>
                        </xsl:attribute>
                    </OrgUnit>
                </PartOf>
            </xsl:if>
        </OrgUnit>
    </xsl:template>

</xsl:stylesheet>
