<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:exsl="http://exslt.org/common">

    <xsl:param name="format"/>

    <!-- load in 'all-resources-meta.xml' -->
    <xsl:variable name="all-resources-meta" select="document('all-resources-meta.xml')"/>

    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="$format = 'html'">
                <xsl:apply-templates mode="html"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="resource" mode="html">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html></xsl:text>
        <html>
            <head>
                <xsl:copy-of select="/resource/head/*"/>
            </head>
            <body>
                [<xsl:copy-of select="$format"/>]
                <nav id="main-nav">
                    <ul>
                        <xsl:for-each select="$all-resources-meta/resources/resource">
                            <li>
                                <a>
                                    <xsl:attribute name="href">
                                        <xsl:value-of select="concat(system-meta/meta[@name='relpath']/@content, '/', source-meta/meta[@name='Identifier']/@content, '.', $format)"/>
                                    </xsl:attribute>
                                    <xsl:value-of select="source-meta/meta[@name='Identifier']/@content"/>
                                </a>
                            </li>
                        </xsl:for-each>
                    </ul>
                </nav>
                <hr/>
                <div id="content">
                    <xsl:call-template name="page-title"/>
                    <xsl:call-template name="page-date"/>
                    <xsl:call-template name="page-creator"/>

                    <xsl:apply-templates select="/resource/body/*"/>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- identity template -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template name="page-title">
        <h1><xsl:value-of select="/resource/head/title"/></h1>
    </xsl:template>

    <xsl:template name="page-date">
        <h2 class="date"><xsl:value-of select="/resource/head/meta[@name='Date']/@content"/></h2>
    </xsl:template>

    <xsl:template name="page-creator">
        <h2 class="date"><xsl:value-of select="/resource/head/meta[@name='Creator']/@content"/></h2>
    </xsl:template>

    <xsl:template match="em">
        <em style="color:#ff0000"><xsl:apply-templates/></em>
    </xsl:template>

    <!-- swallow comments -->
    <xsl:template match="comment()"/>
</xsl:stylesheet>

