
def test_site_in_study_table(
        Table_Builder_Director, site_in_project_userinput,
        dataset_test_1, Site_In_Project_Table_Builder):
    sitelevels = dataset_test_1['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(raw_userinput)
    face_input = facade._inputs[raw_userinput.name]
    site_in_studybuilder = Site_In_Project_Table_Builder()
    assert (isinstance(site_in_studybuilder, Site_In_Project_Table_Builder)) is True

    director = Table_Builder_Director()
    assert (isinstance(director, Table_Builder_Director)) is True
    director.set_user_input(face_input)
    director.set_builder(site_in_studybuilder)
    director.set_data(dataset_test_1)
    director.set_globalid(2)
    director.set_siteid('site')
    director.set_sitelevels(sitelevels)
    site_in_studydf = director.get_database_table()
    showsite_in_study = site_in_studydf._availdf
    print('finished site_in_study: ', showsite_in_study)
    assert isinstance(showsite_in_study, DataFrame) is True
    assert (len(showsite_in_study) == len(sitelevels)) is True

@pytest.fixture
def taxa_user_input_raw():
    taxalned = OrderedDict((
        ('sppcode', 'SP_CODE'),
        ('kingdom', 'TAXON_KINGDOM'),
        ('phylum', 'TAXON_PHYLUM'),
        ('clss', 'TAXON_CLASS'),
        ('ordr', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', True),
        ('kingdom', True),
        ('phylum', True),
        ('clss', True),
        ('ordr', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= hlp.extract(taxalned, available),
        checks=taxacreate)
    return taxaini


@pytest.fixture
def metahandle_raw():
    lentry = {
        'globalid': 4,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.15'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def filehandle_raw():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            '/Users/bibsian/Desktop/git/database-development/' +
            'poplerGUI/Metadata_and_og_data/' +
            'cover_all_years_20140902.csv' ))
    return fileinput

@pytest.fixture
def sitehandle_raw():
    lned = {'siteid': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

def test_taxatable_build_raw_data(
        TaxaTableBuilder, TableDirector, taxa_user_input_raw,
        filehandle_raw, metahandle_raw, sitehandle_raw):
    facade = face.Facade()
    facade.input_register(metahandle_raw)
    facade.input_register(filehandle_raw)
    dfraw = facade.load_data()
    
    sitelevels = dfraw['SITE'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade.register_site_levels(sitelevels)
    facade.input_register(sitehandle_raw)
    facade.input_register(taxa_user_input_raw)
    
    face_input = facade._inputs[taxa_user_input_raw.name]
    taxabuilder = TaxaTableBuilder()
    assert (isinstance(taxabuilder, TaxaTableBuilder)) is True

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(taxabuilder)
    director.set_data(dfraw)
    director.set_globalid(2)
    director.set_siteid('SITE')
    director.set_sitelevels(sitelevels)
    
    taxatable = director.get_database_table()
    showtaxa = taxatable._availdf
    assert isinstance(showtaxa,DataFrame)    
    print(showtaxa)

    testphylum = list(set(showtaxa['phylum'].values.tolist()))
    testphylum.sort()
#    print('test phylum:', testphylum)
    testorder = list(set(showtaxa['ordr'].values.tolist()))
    testorder.sort()
    testspecies = list(set(showtaxa['species'].values.tolist()))
    testspecies.sort()
    print('test species: ', testspecies)

    truephylum = list(set(dfraw['TAXON_PHYLUM'].values.tolist()))
    truephylum.sort()
#    print('true phylum: ', truephylum)
    trueorder = list(set(dfraw['TAXON_ORDER'].values.tolist()))
    trueorder.sort()
    truespecies = list(set(dfraw['TAXON_SPECIES'].values.tolist()))
    truespecies.sort()
    print('true species: ', truespecies)

    assert (testphylum == truephylum) is True
    assert (testorder == trueorder) is True    
    assert (testspecies == truespecies) is True

    taxamade = facade.make_table('taxainfo')
    taxamade = taxamade._availdf
    testmadespecies = list(set(taxamade['species'].values.tolist()))
    testmadespecies.sort()
    print(testmadespecies)
    assert (testmadespecies == truespecies) is True
    


@pytest.fixture
def climate_user_input():
    lned = OrderedDict((
        ('avetempobs', ''),
        ('aveprecipobs', '2'),
        ('avewindobs', ''),
        ('avewindobs', ''),
        ('avelightobs', ''),
        ('avewatertempobs', ''),
        ('avephobs', ''),
        ('avecondobs', ''),
        ('aveturbidityobs', ''),
        ('maxtempobs', ''),
        ('maxprecipobs', ''),
        ('maxwindobs', ''),
        ('maxwindobs', ''),
        ('maxlightobs', ''),
        ('maxwatertempobs', ''),
        ('maxphobs', ''),
        ('maxcondobs', ''),
        ('maxturbidityobs', ''),
        ('mintempobs', ''),
        ('minprecipobs', ''),
        ('minwindobs', ''),
        ('minwindobs', ''),
        ('minlightobs', ''),
        ('minwatertempobs', ''),
        ('minphobs', ''),
        ('mincondobs', ''),
        ('minturbidityobs', '')
    ))

    cks = OrderedDict((
        ('avetempobs', True),
        ('aveprecipobs', False),
        ('avewindobs', True),
        ('avewindobs', True),
        ('avelightobs', True),
        ('avewatertempobs', True),
        ('avephobs', True),
        ('avecondobs', True),
        ('aveturbidityobs', True),
        ('maxtempobs', True),
        ('maxprecipobs', True),
        ('maxwindobs', True),
        ('maxwindobs', True),
        ('maxlightobs', True),
        ('maxwatertempobs', True),
        ('maxphobs', True),
        ('maxcondobs', True),
        ('maxturbidityobs', True),
        ('mintempobs', True),
        ('minprecipobs', True),
        ('minwindobs', True),
        ('minwindobs', True),
        ('minlightobs', True),
        ('minwatertempobs', True),
        ('minphobs', True),
        ('mincondobs', True),
        ('minturbidityobs', True)
    ))

    user_input = ini.InputHandler(
        name='siteinfo', tablename='climaterawtable', lnedentry=lned,
        checks=cks
    )
    return user_input

@pytest.fixture
def all_units():
    lnedunits = OrderedDict((
        ('avetempobsmeasure', ''),
        ('aveprecipobsmeasure', 'cm'),
        ('avewindobsmeasure', ''),
        ('avewindobsmeasure', ''),
        ('avelightobsmeasure', ''),
        ('avewatertempobsmeasure', ''),
        ('avephobsmeasure', ''),
        ('avecondobsmeasure', ''),
        ('aveturbidityobsmeasure', ''),
        ('maxtempobsmeasure', ''),
        ('maxprecipobsmeasure', ''),
        ('maxwindobsmeasure', ''),
        ('maxwindobsmeasure', ''),
        ('maxlightobsmeasure', ''),
        ('maxwatertempobsmeasure', ''),
        ('maxphobsmeasure', ''),
        ('maxcondobsmeasure', ''),
        ('maxturbidityobsmeasure', ''),
        ('mintempobsmeasure', ''),
        ('minprecipobsmeasure', ''),
        ('minwindobsmeasure', ''),
        ('minwindobsmeasure', ''),
        ('minlightobsmeasure', ''),
        ('minwatertempobsmeasure', ''),
        ('minphobsmeasure', ''),
        ('mincondobsmeasuremeasure', ''),
        ('minturbidityobsmeasure', '')
    ))
    return lnedunits

@pytest.fixture
def cov_lned():
    lnedcovs = OrderedDict((
        ('covavg', ''),
        ('covmin', ''),
        ('covmax', '')
    ))
    return lnedcovs

@pytest.fixture
def cov_ck():
    ckcovs = OrderedDict((
        ('covavg', True),
        ('covmin', True),
        ('covmax', True)
    ))
    return ckcovs

@pytest.fixture
def cov_units():
    lnedunitscov = OrderedDict((
        ('covavgmeasure', ''),
        ('covminmeasure', ''),
        ('covmaxmeasure', '')
    ))
    return lnedunitscov

@pytest.fixture
def climatedf():
    return read_table((
        rootpath + 
        'Datasets_manual_test/climate_precip.txt'
    ), header=-1, engine='c')

@pytest.fixture
def ClimateTableBuilder(AbstractTableBuilder):
    class ClimateTableBuilder(AbstractTableBuilder):
        '''
        Concrete table builder for climate data.
        '''
        def get_dataframe(
                self, dataframe, acols, nullcols, dbcol,
                globalid, siteid, sitelevels):

            col_booleans = list(self._inputs.checks.values())
            col_names = list(self._inputs.checks.keys())
            acols = [
                x.rstrip() for x,y in zip(acols, col_booleans)
                if y is False]
            acols_rename = [
                x.rstrip() for x,y in zip(col_names, col_booleans)
                if y is False]
            nullcols = [
                x.rstrip() for x,y in zip(col_names, col_booleans)
                if y is True]
            dbcol.remove('stationid')

            for i in dbcol:
                if i not in nullcols:
                    nullcols.append(i)
                else:
                    pass
            
            
            print('siteid: ', siteid)
            print('col bools: ', col_booleans)
            print('avaialable cols: ', acols)
            print('null cols: ', nullcols)
            print('db cols: ', dbcol)
            
            print('dataframe climate build: ', dataframe)
            
            try:
                dataframe[acols]
            except:
                print('could not find column, trying numeric index')
                acols = [int(x) for x in acols]

            finally:
                acols.append(siteid)
                
            uniquesubset = dataframe[acols]
            nullsubset = hlp.produce_null_df(
                ncols=len(nullcols),
                colnames=nullcols,
                dflength=len(uniquesubset),
                nullvalue='NA')
            print('uq subset build: ', uniquesubset)
            _concat =  concat(
                [uniquesubset, nullsubset], axis=1).reset_index(
                    )
            final = _concat.reset_index() 

            try:
                print('build siteid: ', siteid)
                acols_rename.append('stationid')
                for i,item in enumerate(acols_rename):
                    final.rename(
                        columns={acols[i]:item}, inplace=True)

                print('final build class: ', final.columns)
                return final
            
            except Exception as e:
                print(str(e))
                raise AttributeError('Column renaming error')

    return ClimateTableBuilder


def test_climate_obs(
        TableDirector, climatedf, climate_user_input,
        ClimateTableBuilder, all_units, cov_lned, cov_ck, cov_units):    

    climatedf['site_a'] = 'site_a'
    print(climatedf)
    sitelevels = climatedf[
        'site_a'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(climate_user_input)
    face_input = facade._inputs[climate_user_input.name]
    climatebuilder = ClimateTableBuilder()

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(climatebuilder)
    director.set_data(climatedf)
    director.set_globalid(1)
    director.set_siteid('site_a')
    director.set_sitelevels(sitelevels)
    updatedf = director.get_database_table()
    showupdate = updatedf._availdf
    print(showupdate['stationid'])
    assert isinstance(showupdate, DataFrame) is True
    assert (len(showupdate) == len(climatedf)) is True

@pytest.fixture
def climate_user_input2():
    lned = OrderedDict((
        ('avetempobs', 'Temperature'),
        ('aveprecipobs', ''),
        ('avewindobs', ''),
        ('avewindobs', ''),
        ('avelightobs', ''),
        ('avewatertempobs', ''),
        ('avephobs', ''),
        ('avecondobs', ''),
        ('aveturbidityobs', ''),
        ('maxtempobs', ''),
        ('maxprecipobs', ''),
        ('maxwindobs', ''),
        ('maxwindobs', ''),
        ('maxlightobs', ''),
        ('maxwatertempobs', ''),
        ('maxphobs', ''),
        ('maxcondobs', ''),
        ('maxturbidityobs', ''),
        ('mintempobs', ''),
        ('minprecipobs', ''),
        ('minwindobs', ''),
        ('minwindobs', ''),
        ('minlightobs', ''),
        ('minwatertempobs', ''),
        ('minphobs', ''),
        ('mincondobs', ''),
        ('minturbidityobs', '')
    ))

    cks = OrderedDict((
        ('avetempobs', False),
        ('aveprecipobs', True),
        ('avewindobs', True),
        ('avewindobs', True),
        ('avelightobs', True),
        ('avewatertempobs', True),
        ('avephobs', True),
        ('avecondobs', True),
        ('aveturbidityobs', True),
        ('maxtempobs', True),
        ('maxprecipobs', True),
        ('maxwindobs', True),
        ('maxwindobs', True),
        ('maxlightobs', True),
        ('maxwatertempobs', True),
        ('maxphobs', True),
        ('maxcondobs', True),
        ('maxturbidityobs', True),
        ('mintempobs', True),
        ('minprecipobs', True),
        ('minwindobs', True),
        ('minwindobs', True),
        ('minlightobs', True),
        ('minwatertempobs', True),
        ('minphobs', True),
        ('mincondobs', True),
        ('minturbidityobs', True)
    ))

    user_input = ini.InputHandler(
        name='siteinfo', tablename='climaterawtable', lnedentry=lned,
        checks=cks
    )
    return user_input

@pytest.fixture
def all_units2():
    lnedunits = OrderedDict((
        ('avetempobsmeasure', 'F'),
        ('aveprecipobsmeasure', ''),
        ('avewindobsmeasure', ''),
        ('avewindobsmeasure', ''),
        ('avelightobsmeasure', ''),
        ('avewatertempobsmeasure', ''),
        ('avephobsmeasure', ''),
        ('avecondobsmeasure', ''),
        ('aveturbidityobsmeasure', ''),
        ('maxtempobsmeasure', ''),
        ('maxprecipobsmeasure', ''),
        ('maxwindobsmeasure', ''),
        ('maxwindobsmeasure', ''),
        ('maxlightobsmeasure', ''),
        ('maxwatertempobsmeasure', ''),
        ('maxphobsmeasure', ''),
        ('maxcondobsmeasure', ''),
        ('maxturbidityobsmeasure', ''),
        ('mintempobsmeasure', ''),
        ('minprecipobsmeasure', ''),
        ('minwindobsmeasure', ''),
        ('minwindobsmeasure', ''),
        ('minlightobsmeasure', ''),
        ('minwatertempobsmeasure', ''),
        ('minphobsmeasure', ''),
        ('mincondobsmeasuremeasure', ''),
        ('minturbidityobsmeasure', '')
    ))
    return lnedunits

@pytest.fixture
def cov_lned2():
    lnedcovs = OrderedDict((
        ('covavg', ''),
        ('covmin', ''),
        ('covmax', '')
    ))
    return lnedcovs

@pytest.fixture
def cov_ck2():
    ckcovs = OrderedDict((
        ('covavg', True),
        ('covmin', True),
        ('covmax', True)
    ))
    return ckcovs

@pytest.fixture
def cov_units2():
    lnedunitscov = OrderedDict((
        ('covavgmeasure', ''),
        ('covminmeasure', ''),
        ('covmaxmeasure', '')
    ))
    return lnedunitscov

@pytest.fixture
def climatedf2():
    return read_table((
        rootpath + 
        'Datasets_manual_test/climate_temp_test.txt'
    ), header='infer', engine='c', delimiter=',')

def test_climate_2_obs(
        TableDirector, climatedf2, climate_user_input2,
        ClimateTableBuilder, all_units2, cov_lned2,
        cov_ck2, cov_units2):    

    climatedf2['site_a'] = 'site_a'
    print(climatedf2)
    sitelevels = climatedf2[
        'site_a'].drop_duplicates().values.tolist()
    sitelevels.sort()
    facade = face.Facade()
    facade.input_register(climate_user_input2)
    face_input = facade._inputs[climate_user_input2.name]
    climatebuilder = ClimateTableBuilder()

    director = TableDirector()
    assert (isinstance(director, TableDirector)) is True
    director.set_user_input(face_input)
    director.set_builder(climatebuilder)
    director.set_data(climatedf2)
    director.set_globalid(1)
    director.set_siteid('site_a')
    director.set_sitelevels(sitelevels)
    updatedf = director.get_database_table()
    showupdate = updatedf._availdf
    print(showupdate.columns)
    print(showupdate)
    assert isinstance(showupdate, DataFrame) is True
    assert (len(showupdate) == len(climatedf2)) is True
