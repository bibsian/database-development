--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: climate_raw_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE climate_raw_table (
    metarecordid integer NOT NULL,
    title text,
    stationid character varying(200),
    year numeric,
    month numeric,
    day numeric,
    avetempobs numeric,
    avetempmeasure character varying(50),
    mintempobs numeric,
    mintempmeasure character varying(50),
    maxtempobs numeric,
    maxtempmeasure character varying(50),
    aveprecipobs numeric,
    aveprecipmeasure character varying(50),
    minprecipobs numeric,
    minprecipmeasure character varying(50),
    maxprecipobs numeric,
    maxprecipmeasure numeric,
    avewindobs numeric,
    avewindmeasure character varying(50),
    minwindobs numeric,
    minwindmeasure character varying(50),
    maxwindobs numeric,
    maxwindmeasure numeric,
    avelightobs numeric,
    avelightmeasure character varying(50),
    minlightobs numeric,
    minlightmeasure character varying(50),
    maxlightobs numeric,
    maxlightmeasure numeric,
    avewatertempobs numeric,
    avewatertempmeasure character varying(50),
    minwatertempobs numeric,
    minwatertempmeasure character varying(50),
    maxwatertempobs numeric,
    maxwatertempmeasure character varying(50),
    avephobs numeric,
    avephmeasure character varying(50),
    minphobs numeric,
    minphmeasure character varying(50),
    maxphobs numeric,
    maxphmeasure numeric,
    avecondobs numeric,
    avecondmeasure character varying(50),
    mincondobs numeric,
    mincondmeasure character varying(50),
    maxcondobs numeric,
    maxcondmeasure character varying(50),
    aveturbidityobs numeric,
    aveturbiditymeasure character varying(50),
    minturbidityobs numeric,
    minturbiditymeasure character varying(50),
    maxturbidityobs numeric,
    maxturbiditymeasure character varying(50),
    covariates text
);


ALTER TABLE climate_raw_table OWNER TO postgres;

--
-- Name: climate_raw_table_metarecordid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE climate_raw_table_metarecordid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE climate_raw_table_metarecordid_seq OWNER TO postgres;

--
-- Name: climate_raw_table_metarecordid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE climate_raw_table_metarecordid_seq OWNED BY climate_raw_table.metarecordid;


--
-- Name: climate_station_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE climate_station_table (
    stationid character varying(200) NOT NULL,
    lterid character varying(10),
    lat numeric,
    lng numeric,
    descript text
);


ALTER TABLE climate_station_table OWNER TO postgres;

--
-- Name: lter_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE lter_table (
    lterid character varying(10) NOT NULL,
    lter_name text,
    currently_funded character varying(50),
    pi character varying(200),
    pi_contact_email character varying(200),
    alt_contact_email character varying(200),
    homepage character varying(200)
);


ALTER TABLE lter_table OWNER TO postgres;

--
-- Name: main_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE main_table (
    lter_proj_site integer NOT NULL,
    metarecordid integer,
    title text,
    samplingunits character varying(50),
    samplingprotocol character varying(50),
    structured character varying(50),
    studystartyr numeric,
    studyendyr numeric,
    siteid character varying(200),
    sitestartyr numeric,
    siteendyr numeric,
    samplefreq text,
    totalobs numeric,
    studytype character varying(50),
    community character varying(50),
    uniquetaxaunits numeric,
    sp_rep1_ext numeric,
    sp_rep1_ext_units character varying(200),
    sp_rep1_label character varying(200),
    sp_rep1_uniquelevels numeric,
    sp_rep2_ext numeric,
    sp_rep2_ext_units character varying(200),
    sp_rep2_label character varying(200),
    sp_rep2_uniquelevels numeric,
    sp_rep3_ext numeric,
    sp_rep3_ext_units character varying(200),
    sp_rep3_label character varying(200),
    sp_rep3_uniquelevels numeric,
    sp_rep4_ext numeric,
    sp_rep4_ext_units character varying(200),
    sp_rep4_label character varying(200),
    sp_rep4_uniquelevels numeric,
    authors text,
    authors_contact character varying(200),
    metalink character varying(200),
    knbid character varying(200)
);


ALTER TABLE main_table OWNER TO postgres;

--
-- Name: main_table_lter_proj_site_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE main_table_lter_proj_site_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE main_table_lter_proj_site_seq OWNER TO postgres;

--
-- Name: main_table_lter_proj_site_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE main_table_lter_proj_site_seq OWNED BY main_table.lter_proj_site;


--
-- Name: raw_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE raw_table (
    sampleid integer NOT NULL,
    taxaid integer,
    lter_proj_site integer,
    year numeric,
    month numeric,
    day numeric,
    spt_rep1 character varying(50),
    spt_rep2 character varying(50),
    spt_rep3 character varying(50),
    spt_rep4 character varying(50),
    structure character varying(50),
    individ character varying(50),
    unitobs numeric,
    covariates text
);


ALTER TABLE raw_table OWNER TO postgres;

--
-- Name: raw_table_sampleid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE raw_table_sampleid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE raw_table_sampleid_seq OWNER TO postgres;

--
-- Name: raw_table_sampleid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE raw_table_sampleid_seq OWNED BY raw_table.sampleid;


--
-- Name: site_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE site_table (
    siteid character varying(200) NOT NULL,
    lterid character varying(10),
    lat numeric,
    lng numeric,
    descript text
);


ALTER TABLE site_table OWNER TO postgres;

--
-- Name: taxa_table; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE taxa_table (
    taxaid integer NOT NULL,
    lter_proj_site integer,
    sppcode character varying(100),
    kingdom character varying(100),
    phylum character varying(100),
    clss character varying(100),
    "order" character varying(100),
    family character varying(100),
    genus character varying(100),
    species character varying(100),
    authority character varying(100)
);


ALTER TABLE taxa_table OWNER TO postgres;

--
-- Name: taxa_table_taxaid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE taxa_table_taxaid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taxa_table_taxaid_seq OWNER TO postgres;

--
-- Name: taxa_table_taxaid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE taxa_table_taxaid_seq OWNED BY taxa_table.taxaid;


--
-- Name: metarecordid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY climate_raw_table ALTER COLUMN metarecordid SET DEFAULT nextval('climate_raw_table_metarecordid_seq'::regclass);


--
-- Name: lter_proj_site; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY main_table ALTER COLUMN lter_proj_site SET DEFAULT nextval('main_table_lter_proj_site_seq'::regclass);


--
-- Name: sampleid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY raw_table ALTER COLUMN sampleid SET DEFAULT nextval('raw_table_sampleid_seq'::regclass);


--
-- Name: taxaid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxa_table ALTER COLUMN taxaid SET DEFAULT nextval('taxa_table_taxaid_seq'::regclass);


--
-- Data for Name: climate_raw_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY climate_raw_table (metarecordid, title, stationid, year, month, day, avetempobs, avetempmeasure, mintempobs, mintempmeasure, maxtempobs, maxtempmeasure, aveprecipobs, aveprecipmeasure, minprecipobs, minprecipmeasure, maxprecipobs, maxprecipmeasure, avewindobs, avewindmeasure, minwindobs, minwindmeasure, maxwindobs, maxwindmeasure, avelightobs, avelightmeasure, minlightobs, minlightmeasure, maxlightobs, maxlightmeasure, avewatertempobs, avewatertempmeasure, minwatertempobs, minwatertempmeasure, maxwatertempobs, maxwatertempmeasure, avephobs, avephmeasure, minphobs, minphmeasure, maxphobs, maxphmeasure, avecondobs, avecondmeasure, mincondobs, mincondmeasure, maxcondobs, maxcondmeasure, aveturbidityobs, aveturbiditymeasure, minturbidityobs, minturbiditymeasure, maxturbidityobs, maxturbiditymeasure, covariates) FROM stdin;
\.


--
-- Name: climate_raw_table_metarecordid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('climate_raw_table_metarecordid_seq', 1, false);


--
-- Data for Name: climate_station_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY climate_station_table (stationid, lterid, lat, lng, descript) FROM stdin;
\.


--
-- Data for Name: lter_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY lter_table (lterid, lter_name, currently_funded, pi, pi_contact_email, alt_contact_email, homepage) FROM stdin;
AND	Andrew Forest LTER	1	Michael Nelson	mpnelson@oregonstate.edu	hjafacilities@fsl.orst.edu	http://andrewsforest.oregonstate.edu/
ARC	Arctic LTER	1	Gaius Shaver	gshaver@mbl.edu	dscanlon@mbl.edu	http://ecosystems.mbl.edu/ARC/
BES	Baltimore Ecosystem Study	1	Steward Pickett	PickettS@ecostudies.org	BeyarH@caryinstitute.org	http://www.beslter.org/
BNZ	Bonanaza Creek LTER	1	Roger Ruess	rwruess@alaska.edu	jhollingsworth@alaska.edu	http://www.lter.uaf.edu/
CCE	California Current Ecosystem LTER	1	Mark Ohman	mohman@ucsd.edu	mohman@ucsd.edu	http://cce.lternet.edu/
CDR	Cedar Creek Ecosystem Science Reserve	1	Eric Seabloom	seabloom@umn.edu	retilman@umn.edu	http://cedarcreek.umn.edu/
CAP	Central Arizon - Phoneix LTER	1	Nancy Grimm	nbgrimm@asu.edu	caplter@asu.edu	https://sustainability.asu.edu/caplter/
CWT	Coweeta LTER	1	Ted Gragson	tgragson@uga.edu	tgragson@uga.edu	http://coweeta.uga.edu/
FCE	Florida Coastal Everglades LTER	1	Evelyn Gaiser	gaisere@flu.edu	fcelter@fiu.edu	http://fce.lternet.edu/
GCE	Georgia Coastal Ecosystems LTER	1	Merryl Alber	malber@uga.edu	gcelter@uga.edu	http://gce-lter.marsci.uga.edu/
HFR	Harvard Forest LTER	1	David Foster	drfoster@fas.harvard.edu	drfoster@fas.harvard.edu	http://harvardforest.fas.harvard.edu/
HBR	Hubbard Brook LTER	1	Charles Driscoll	ctdrisco@syr.edu	ihalm@fs.fed.us	http://hbr.lternet.edu/
JRN	Jornada Basin LTER	1	Deb Peters	debpeter@nmsu.edu	debpeter@nmsu.edu	http://jornada.nmsu.edu/lter
KBS	Kellogg Biological Station LTER	1	Phil Robertson	robert30@msu.edu	lter.data.manager@kbs.msu.edu	http://lter.kbs.msu.edu/
KNZ	Konza Prairie LTER	1	John Blair	jblair@ksu.edu	knzlter@ksu.edu	http://www.konza.ksu.edu/Splash/default.aspx
NCO	LTER Network Communications Office	1	Frank Davis	frank.davis@nceas.ucsb.edu	downs@nceas.ucsb.edu	https://www.nceas.ucsb.edu/lter-network-communications-office
LNO	LTER Network Office	1	Robert Waide	rwaide@lternet.edu	 rwaide@lternet.edu	http://www.lternet.edu/sites/lno
LUQ	Luquillo LTER	1	Jess Zimmerman	jesskz@ites.upr.edu	jesskz@ites.upr.edu	http://luq.lternet.edu/
MCM	McMurdo Dry Valleys LTER	1	Mike Gooseff	michael.gooseff@colorado.edu	mcmlter@lternet.edu	http://mcm.lternet.edu/
MCR	Moorea Coral Reef LTER	1	Russell Schmitt	russ.schmitt@lifesci.ucsb.edu	brooks@msi.ucsb.edu	http://mcr.lternet.edu/
NWT	Niwot Ridge LTER	1	Katharine Suding	suding@colorado.edu	lternwt@colorado.edu	http://culter.colorado.edu/NWT/
NTL	North Temperate Lakes LTER	1	Emily Stanley	ehstanley@wisc.edu	oferrell@wesc.edu	https://lter.limnology.wisc.edu/
PAL	Palmer Antarctica LTER	1	Hugh Ducklow	hducklow@Ideo.columbia.edu	hducklow@Ideo.columbia.edu	http://pal.lternet.edu/
PIE	Plum Island Ecosystems LTER	1	Anne Giblin	agiblin@mbl.edu	agiblin@mbl.edu	http://pie-lter.ecosystems.mbl.edu/
SBC	Santa Barbar Coastal LTER	1	Dan Reed	dan.reed@lifesci.ucsb.edu	sbclter@msi.ucsb.edu	http://sbc.lternet.edu/
SEV	Sevilleta LTER 	1	Will Pockman	pockman@unm.edu	webmaster@sevilleta.unm.edu	http://sev.lternet.edu/
SGS	Shortgrass Steppe	0	John Moore	jcmoore@nrel.colostate.edu	ECODATA_NREL@colostate.edu	http://sgslter.colostate.edu/
VCR	Virginia Coastal Reserve LTER	1	Karen McGlathery	kjm4k@virginia.edu	JPorter@lternet.edu	http://www.vcrlter.virginia.edu/home1/index.php
\.


--
-- Data for Name: main_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY main_table (lter_proj_site, metarecordid, title, samplingunits, samplingprotocol, structured, studystartyr, studyendyr, siteid, sitestartyr, siteendyr, samplefreq, totalobs, studytype, community, uniquetaxaunits, sp_rep1_ext, sp_rep1_ext_units, sp_rep1_label, sp_rep1_uniquelevels, sp_rep2_ext, sp_rep2_ext_units, sp_rep2_label, sp_rep2_uniquelevels, sp_rep3_ext, sp_rep3_ext_units, sp_rep3_label, sp_rep3_uniquelevels, sp_rep4_ext, sp_rep4_ext_units, sp_rep4_label, sp_rep4_uniquelevels, authors, authors_contact, metalink, knbid) FROM stdin;
1	7	Test Dataset 1	NA	count	NA	1987	1999	Site1	1999	1999	yr	2	obs	yes	2	NaN	NA	SITE	1	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://and.test.rice.com	knb-lter-sbc.18.18
2	7	Test Dataset 1	NA	count	NA	1987	1999	Site2	1987	1987	yr	2	obs	yes	1	NaN	NA	SITE	1	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://and.test.rice.com	knb-lter-sbc.18.18
3	7	Test Dataset 1	NA	count	NA	1987	1999	Site3	1992	1992	yr	2	obs	yes	2	NaN	NA	SITE	1	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://and.test.rice.com	knb-lter-sbc.18.18
4	8	Test Dataset 2	NA	count	NA	1985	2000	ACL	1999	2000	yr	2	obs	yes	2	NaN	NA	SITE	1	NaN	NA	PLOT	2	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://sbc.test.rice.com	knb-lter-sbc.17.28
5	8	Test Dataset 2	NA	count	NA	1985	2000	HCR	1985	1985	yr	2	obs	yes	2	NaN	NA	SITE	1	NaN	NA	PLOT	2	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://sbc.test.rice.com	knb-lter-sbc.17.28
6	8	Test Dataset 2	NA	count	NA	1985	2000	PIN	1985	1999	yr	2	obs	yes	2	NaN	NA	SITE	1	NaN	NA	PLOT	1	NaN	NA	NA	NaN	NaN	NA	NA	NaN	NA	NA	http://sbc.test.rice.com	knb-lter-sbc.17.28
7	9	Test Dataset 3	NA	biomass	NA	1987	1999	SiteA	1999	1999	monthly	2	obs	no	1	NaN	NA	site	1	NaN	NA	plot	2	NaN	NA	quadrat	1	NaN	NA	NA	NaN	NA	NA	http://sbc.2.test.rice.com	knb-lter-sbc.19.21
8	9	Test Dataset 3	NA	biomass	NA	1987	1999	SiteB	1987	1987	monthly	2	obs	no	1	NaN	NA	site	1	NaN	NA	plot	2	NaN	NA	quadrat	1	NaN	NA	NA	NaN	NA	NA	http://sbc.2.test.rice.com	knb-lter-sbc.19.21
9	9	Test Dataset 3	NA	biomass	NA	1987	1999	SiteC	1992	1992	monthly	2	obs	no	1	NaN	NA	site	1	NaN	NA	plot	2	NaN	NA	quadrat	1	NaN	NA	NA	NaN	NA	NA	http://sbc.2.test.rice.com	knb-lter-sbc.19.21
\.


--
-- Name: main_table_lter_proj_site_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('main_table_lter_proj_site_seq', 9, true);


--
-- Data for Name: raw_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY raw_table (sampleid, taxaid, lter_proj_site, year, month, day, spt_rep1, spt_rep2, spt_rep3, spt_rep4, structure, individ, unitobs, covariates) FROM stdin;
1	1	1	1999	2	1	Site1	NA	NA	NA	NA	NA	25	{'DEPTH': '50'}
2	2	1	1999	2	28	Site1	NA	NA	NA	NA	NA	10	{'DEPTH': '100'}
3	3	2	1987	8	3	Site2	NA	NA	NA	NA	NA	54	{'DEPTH': '20'}
4	3	2	1987	8	3	Site2	NA	NA	NA	NA	NA	82	{'DEPTH': '20'}
5	4	3	1992	10	12	Site3	NA	NA	NA	NA	NA	1	{'DEPTH': '10'}
6	5	3	1992	10	12	Site3	NA	NA	NA	NA	NA	1	{'DEPTH': '10'}
7	6	5	1985	10	22	HCR	1	NA	NA	NA	NA	25	{'DEPTH': '50'}
8	7	5	1985	10	15	HCR	2	NA	NA	NA	NA	10	{'DEPTH': '100'}
9	8	4	1999	2	11	ACL	1	NA	NA	NA	NA	54	{'DEPTH': '20'}
10	9	4	2000	12	12	ACL	2	NA	NA	NA	NA	82	{'DEPTH': '20'}
11	10	6	1985	10	15	PIN	1	NA	NA	NA	NA	1	{'DEPTH': '10'}
12	11	6	1999	2	11	PIN	1	NA	NA	NA	NA	1	{'DEPTH': '10'}
13	12	7	1999	2	NaN	SiteA	A	1	NA	NA	NA	123.23399999999999	{'temp': '7'}
14	12	7	1999	2	NaN	SiteA	B	1	NA	NA	NA	81.459999999999994	{'temp': '4'}
15	13	8	1987	8	NaN	SiteB	NA	1	NA	NA	NA	123.5	{'temp': '-9999'}
16	13	8	1987	8	NaN	SiteB	B	1	NA	NA	NA	64.450000000000003	{'temp': '10'}
17	14	9	1992	10	NaN	SiteC	A	1	NA	NA	NA	972.39999999999998	{'temp': '13'}
18	14	9	1992	10	NaN	SiteC	B	1	NA	NA	NA	124.90000000000001	{'temp': '13'}
\.


--
-- Name: raw_table_sampleid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('raw_table_sampleid_seq', 18, true);


--
-- Data for Name: site_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY site_table (siteid, lterid, lat, lng, descript) FROM stdin;
ACL	SBC	-124.56	22.3	NA
HCR	SBC	-124.33	23.5	NA
PIN	SBC	-123.5	22.5	NA
Site1	AND	110.34	11.4	NA
Site2	AND	109.245	11.5	NA
Site3	AND	108.34	11.7	NA
SiteA	SBC	-101.1	30.5	NA
SiteB	SBC	-101.4	30.23	NA
SiteC	SBC	-101.4	30.53	NA
\.


--
-- Data for Name: taxa_table; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY taxa_table (taxaid, lter_proj_site, sppcode, kingdom, phylum, clss, "order", family, genus, species, authority) FROM stdin;
1	1	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupis	NA
2	1	NA	NA	Chordata	Mammalia	Carnivora	Felidae	felis	catus	NA
3	2	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupis	NA
4	3	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupis angel1	NA
5	3	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupid angel2	NA
6	5	NA	NA	Chordata	Mammalia	Order1	Family1	Genus1	species1	NA
7	5	NA	NA	Chordata	Mammalia	Order2	Family2	unknown thing	spp.	NA
8	4	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	spp.	NA
9	4	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupis	NA
10	6	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupis angel1	NA
11	6	NA	NA	Chordata	Mammalia	Carnivora	Canidae	Canis	lupid angel2	NA
12	7	NA	NA	NA	NA	NA	NA	genus_test3	species_test3	NA
13	8	NA	NA	NA	NA	NA	NA	genus_test3	species_test3	NA
14	9	NA	NA	NA	NA	NA	NA	genus_test3	species_test3	NA
\.


--
-- Name: taxa_table_taxaid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('taxa_table_taxaid_seq', 14, true);


--
-- Name: climate_raw_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY climate_raw_table
    ADD CONSTRAINT climate_raw_table_pkey PRIMARY KEY (metarecordid);


--
-- Name: climate_station_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY climate_station_table
    ADD CONSTRAINT climate_station_table_pkey PRIMARY KEY (stationid);


--
-- Name: lter_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY lter_table
    ADD CONSTRAINT lter_table_pkey PRIMARY KEY (lterid);


--
-- Name: main_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY main_table
    ADD CONSTRAINT main_table_pkey PRIMARY KEY (lter_proj_site);


--
-- Name: raw_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY raw_table
    ADD CONSTRAINT raw_table_pkey PRIMARY KEY (sampleid);


--
-- Name: site_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY site_table
    ADD CONSTRAINT site_table_pkey PRIMARY KEY (siteid);


--
-- Name: taxa_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY taxa_table
    ADD CONSTRAINT taxa_table_pkey PRIMARY KEY (taxaid);


--
-- Name: climate_raw_table_stationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY climate_raw_table
    ADD CONSTRAINT climate_raw_table_stationid_fkey FOREIGN KEY (stationid) REFERENCES climate_station_table(stationid) ON DELETE CASCADE;


--
-- Name: climate_station_table_lterid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY climate_station_table
    ADD CONSTRAINT climate_station_table_lterid_fkey FOREIGN KEY (lterid) REFERENCES lter_table(lterid);


--
-- Name: main_table_siteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY main_table
    ADD CONSTRAINT main_table_siteid_fkey FOREIGN KEY (siteid) REFERENCES site_table(siteid);


--
-- Name: raw_table_lter_proj_site_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY raw_table
    ADD CONSTRAINT raw_table_lter_proj_site_fkey FOREIGN KEY (lter_proj_site) REFERENCES main_table(lter_proj_site) ON DELETE CASCADE;


--
-- Name: raw_table_taxaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY raw_table
    ADD CONSTRAINT raw_table_taxaid_fkey FOREIGN KEY (taxaid) REFERENCES taxa_table(taxaid) ON DELETE CASCADE;


--
-- Name: site_table_lterid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY site_table
    ADD CONSTRAINT site_table_lterid_fkey FOREIGN KEY (lterid) REFERENCES lter_table(lterid);


--
-- Name: taxa_table_lter_proj_site_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxa_table
    ADD CONSTRAINT taxa_table_lter_proj_site_fkey FOREIGN KEY (lter_proj_site) REFERENCES main_table(lter_proj_site) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: bibsian
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM bibsian;
GRANT ALL ON SCHEMA public TO bibsian;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

