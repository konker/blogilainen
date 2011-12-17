<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <src-meta>
            <xsl:attribute name="id">
                <xsl:value-of select="/html/head/meta[@name='Identifier']/@content"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </src-meta>
    </xsl:template>

    <!-- identity template -->
    <xsl:template match="@*|node()">
        <xsl:apply-templates select="@*|node()"/>
    </xsl:template>

    <xsl:template match="meta">
        <xsl:copy-of select="."/>
    </xsl:template>
</xsl:stylesheet>
