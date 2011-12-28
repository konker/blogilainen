<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    >

    <xsl:param name="format"/>
    <xsl:output method="html" doctype-system="about:legacy-compat" indent="yes" />

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
        <html lang="en" class="no-js">
            <head>
                <xsl:copy-of select="/resource/head/*"/>

                <meta name="MSSmartTagsPreventParsing" content="TRUE" />
                <meta name="fb:admins" content="574602300" />
                <meta name="generator" content="KVDM" />
                <meta name="author" content="KVDM" />
                <meta name="copyright" content="Copyright (c) 2011 Konrad Markus" />

                <link rel="stylesheet" href="/assets/css/style.css?v=2"/>
                <link rel="stylesheet" href="/assets/css/content.css?v=2"/>
                <link href="http://fonts.googleapis.com/css?family=Francois+One" rel="stylesheet" type="text/css"/>
            </head>
            <body>
                <div id="container">
                    <header>
                        <h1>Konrad Markus</h1>

                        <nav id="mainNav">
                            <ul>
                                <li>
                                    <xsl:if test="//meta[@name='Navigation.1']/@content = 'index'">
                                        <xsl:attribute name="class">selected</xsl:attribute>
                                    </xsl:if>
                                    <a href="/">Home</a>
                                </li>
                                <!--
                                <li>
                                    <xsl:if test="/resource/head/meta[@name='Navigation.1']/@content = 'blog'">
                                        <xsl:attribute name="class">selected</xsl:attribute>
                                    </xsl:if>
                                    <a href="http://blog.konradmarkus.com/">Blog</a>
                                </li>
                                <li>
                                    <xsl:if test="/resource/head/meta[@name='Navigation.1']/@content = 'code'">
                                        <xsl:attribute name="class">selected</xsl:attribute>
                                    </xsl:if>
                                    <a href="/code/">Code</a>
                                </li>
                                -->
                                <li>
                                    <xsl:if test="/resource/head/meta[@name='Navigation.1']/@content = 'cv'">
                                        <xsl:attribute name="class">selected</xsl:attribute>
                                    </xsl:if>
                                    <a href="/cv/" title="My Curriculum Vitae">cv</a>
                                </li>
                                <li>
                                    <xsl:if test="/resource/head/meta[@name='Navigation.1']/@content = 'contact'">
                                        <xsl:attribute name="class">selected</xsl:attribute>
                                    </xsl:if>
                                    <a href="/contact/" title="Contact Details">contact</a>
                                </li>
                            </ul>
                        </nav>
                    </header>
                    <div id="main">
                        <xsl:apply-templates select="body" mode="html"/>
                    </div>
                    <footer>
                        <p>
                            <xsl:text disable-output-escaping="yes">&amp;copy; 2007-2012 </xsl:text>

                            <a href="http://konradmarkus.com/" title="Konrad Markus">Konrad Markus</a> | 
                            <a href="http://validator.w3.org/check?uri=referer" title="Valid HTML">HTML</a> |
                            <a href="http://jigsaw.w3.org/css-validator/check/referrer" title="Valid CSS">CSS</a> |
                            Design by <a href="http://milkmilklemonadearoundthecornerchocolatesmade.com/" title="Milk Milk, Lemonade, Aroud the Corner Chocolate's Made">Milk Milk, Lemonade</a> |
                            Build by <a href="http://morningwoodsoftware.com/" title="Morningwood Software">Morningwood Software</a> |
                            <a href="http://www.linode.com/?r=fd388bb5ef75c0e610250fee39e291a713e5a450" title="Hosting by Linode" class="linode"><img src="/assets/images/linode.png" alt="Hosting by Linode"/></a>
                        </p>
                    </footer>
                </div><!--! end of #container -->
            </body>
        </html>
    </xsl:template>

    <!-- identity template -->
    <xsl:template match="@*|node()" mode="html">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" mode="html"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="body" mode="html">
            <xsl:apply-templates mode="html"/>
    </xsl:template>

    <xsl:template name="page-title">
        <h1><xsl:value-of select="/resource/head/title"/></h1>
    </xsl:template>

    <xsl:template name="page-date">
        <h2 class="date"><xsl:value-of select="/resource/head/meta[@name='dcterms.Date']/@content"/></h2>
    </xsl:template>

    <xsl:template name="page-creator">
        <h2 class="creator"><xsl:value-of select="/resource/head/meta[@name='dcterms.Creator']/@content"/></h2>
    </xsl:template>

    <xsl:template match="em">
        <em style="color:#ff0000"><xsl:apply-templates/></em>
    </xsl:template>

    <!-- swallow comments -->
    <xsl:template match="comment()"/>
</xsl:stylesheet>

