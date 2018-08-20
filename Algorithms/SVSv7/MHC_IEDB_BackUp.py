#/usr/bin/python
import sys

import requests
import pandas as pd

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

class MHC_IEDB():           #IEDB = Immune Epitope Database
    """
    Class: uses IEDB REST API to retrieve MHC-peptide binding information
    Source: http://tools.iedb.org/main/tools-api/
        -describes how to use different REST requests and how to make those requests
    """

    def __init__( self, mhc_alleles, length, pred_method ):
        """
        Args:
            -mhc_alleles = string that is the alleles to be evaluated,  where multiple should be separated by comma (,).
            -length = string that is length of the neoepitope, where multiple should be separated by comma (,). There needs to be the same number as 'mhc_alleles'
            -pred_method = string that is MHC class I binding prediction methods. Some methods are: recommended, consensus, netmhcpan, ann, smmpmbec, smm, comblib_sidney2008, netmhccons, pickpocket, netmhcstabpan --> "recommended" is default
                -ann = artificial neural network
        """
        # self.url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/" 
        self.url_mhci = "http://tools-cluster-interface.iedb.org/tools_api/mhci/"           #this tool will take in an amino acid sequence, or set of sequences and determine each subsequence's ability to bind to a specific MHC class I molecule.
        self.url_proc = "http://tools-cluster-interface.iedb.org/tools_api/processing/"     #this combines predictors of proteasomal processing, TAP transport, and MHC binding to produce an overall score for each peptide's intrinsic potential of being a T cell epitope.
        self.mhc_alleles = mhc_alleles
        self.length = length
        self.pred_method = pred_method

    #MAY DELETE - REPLACED BY retrieve_epitope_analysis()
    # def retrieve_epitope_affinity( self, peptide_seq ):
    #     """
    #     Evaluates peptide affinity to alleles defined in 
    #     Args:
    #         -peptide_seq = string that is the peptide sequence that will be evaluated
    #     Returns: returns a pandas dataframe that contains the peptide-binding affinity to a given MHC. It has the following columns: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
    #         -percentile = the percentile rank -> a percentile rank is generated by comparing the peptide's IC50 against those of a set of random peptides from SWISSPROT database. A small numbered percentile rank indicates high affinity. For the 'consensus' and 'IEDB recommended' methods, the median percentile rank of the methods used is reported as the representative percentile rank.
    #     """
    #     hash_data = {
    #     "method": self.pred_method,
    #     "sequence_text": peptide_seq,
    #     "allele": self.mhc_alleles,
    #     "length": self.length
    #     }

    #     r = requests.post( self.url, data = hash_data )
    #     if not r.ok:
    #         print "MHC_IEDB.retrieve_epitope_affinity() Error:"
    #         return pd.DataFrame( {'A' : []} )       #return empty dataframe

    #     file_io = StringIO( r.content )
    #     df_aff = pd.read_csv( file_io, sep = '\t', header = 0 )         #df_aff = DataFrame Affinity (affinity of peptide to MHC alleles), columns are: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
    #     if df_aff.empty:
    #         return pd.DataFrame( {'A' : []} )       #return empty dataframe

    #     #make sure columns are floats
    #     df_aff[['ic50']] = df_aff[['ic50']].astype( float )
    #     df_aff[['percentile']] = df_aff[['percentile']].astype( float )

    #     #evaluate affinity, where, as a rough guideline, peptides with IC50 values <50 nM are considered high affinity, <500 nM intermediate affinity and <5000 nM low affinity --> Source: http://tools.iedb.org/mhci/help/
    #     def eval_aff( row ):
    #         """
    #         evaluate affinity, where, as a rough guideline, peptides with IC50 values <50 nM are considered high affinity, <500 nM intermediate affinity and <5000 nM low affinity --> Source: http://tools.iedb.org/mhci/help/
    #         """
    #         if row['ic50'] <= 50:
    #             return "HIGH"
    #         elif (row['ic50'] > 50) & (row['ic50'] <= 500):
    #             return "MID"
    #         elif (row['ic50'] > 500) & (row['ic50'] <= 5000):
    #             return "LOW"
    #         else:
    #             return "none"

    #     df_aff['aff_cat'] = "none"
    #     df_aff['aff_cat'] = df_aff.apply( eval_aff, axis = 1)

    #     return df_aff

    # def compare_epitope_affinity( self, pep1, pep2 ):
    #     """
    #     A simple comparison betweeen peptide sequence 1 & peptide sequence 2.
    #     Args:
    #         -pep1 & pep2 = string that is amino acid sequence to be evaluated for affinity towards MHC alleles of interest. Usually pep1 is the original epitope & pep2 is the mutated epitope
    #     """
    #     ##TEST::
    #     print "pep1 = ", pep1
    #     print "pep2 = ", pep2

    #     #NOTE: columns in dataframes are: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
    #     df_pep1 = self.retrieve_epitope_affinity( pep1 )
    #     df_pep2 = self.retrieve_epitope_affinity( pep2 )

    #     ##TEST::
    #     print "df_pep1:"
    #     print df_pep1
    #     print "df_pep2:"
    #     print df_pep2

    #     if df_pep1.empty or df_pep2.empty:
    #         return pd.DataFrame( {'A' : []} )       #return empty dataframe

    #     df_all = pd.merge( df_pep1, df_pep2, on = ['allele', 'start', 'end'], suffixes = ("_1", "_2") )
    #     #create a new column to compare the affinity between peptide 1 & peptide 2. delta_aff = change in affinity from pep1 to pep2, where a lower value in 'ic50' will be a stronger affinity, and a lower 'percentile' (percentile_rank) means a higher affinity for MHC allele
    #     def calc_delta_aff( row ):
    #         """
    #         determine if the new epitope '_2' (usually the mutated epitope) has a higher affinity to MHC allele than '_1' (usually the original epitope)
    #         """
    #         if row['ic50_2'] < row['ic50_1']:
    #             return "higher"
    #         elif row['ic50_2'] > row['ic50_1']:
    #             return "lower"
    #         else:
    #             return "equal"

    #     df_all['delta_aff'] = df_all.apply( calc_delta_aff, axis = 1 )

    #     return df_all

    """
    Functions: Analysis of peptides - either affinity to MHC or antigen processing
    """  
    def retrieve_epitope_analysis( self, peptide_seq, analysis_type = 1 ):
        """
        Evaluates peptide processing through the proteasome
        Args:
            -peptide_seq = string that is the peptide sequence that will be evaluated
            -analysis_type = integer with the following meaning
                -1 = perform analysis of peptide affinity to MHC
                -2 = perform analysis of peptide processing with proteasome, TAP, & MHC
        Returns: returns an array where [0] = integer that is status of request & [1] = a pandas dataframe that contains the peptide-binding affinity to a given MHC. It has the following columns: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
            -[0] values:
                - -1 = request error
                -0 = request not ok (r.ok is False)
                -1 = request is ok
            -[1] values:
                -percentile = the percentile rank -> a percentile rank is generated by comparing the peptide's IC50 against those of a set of random peptides from SWISSPROT database. A small numbered percentile rank indicates high affinity. For the 'consensus' and 'IEDB recommended' methods, the median percentile rank of the methods used is reported as the representative percentile rank.
        """
        if analysis_type == 1:
            url = self.url_mhci
            ic50 = "ic50"
        elif analysis_type == 2:
            url = self.url_proc
            ic50 = "ic50_score"

        hash_data = {
        "method": self.pred_method,
        "sequence_text": peptide_seq,
        "allele": self.mhc_alleles,
        "length": self.length
        }

        ##TEST:: print "MHC_IEDB.retrieve_epitope_analysis: url = ", url, " & hash_data = ", hash_data

        try:
            r = requests.post( url, data = hash_data )
        except requests.exceptions.RequestException as e:
            print "IEDB Request Error with url ", url, " & hash_data = ", hash_data, " --> ", e
            return [ -1, pd.DataFrame({'A' : []}) ]
        
        if not r.ok:
            print "MHC_IEDB.retrieve_epitope_analysis() Error: ", url, " & hash_data = ", hash_data
            return [ 0, pd.DataFrame( {'A' : []} ) ]      #return empty dataframe

        file_io = StringIO( r.content )
        df_aff = pd.read_csv( file_io, sep = '\t', header = 0 )         #df_aff = DataFrame Affinity (affinity of peptide to MHC alleles), columns are: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
        if df_aff.empty:
            return [ 0, pd.DataFrame( {'A' : []} ) ]      #return empty dataframe

        #make sure columns are floats
        df_aff[[ic50]] = df_aff[[ic50]].astype( float )

        #evaluate affinity, where, as a rough guideline, peptides with IC50 values <50 nM are considered high affinity, <500 nM intermediate affinity and <5000 nM low affinity.
        def eval_aff( row ):
            """
            evaluate affinity, where, as a rough guideline, peptides with IC50 values <50 nM are considered high affinity, <500 nM intermediate affinity and <5000 nM low affinity --> --> Source: http://tools.iedb.org/mhci/help/
            """
            if row[ic50] <= 50:
                return "HIGH"
            elif (row[ic50] > 50) & (row[ic50] <= 500):
                return "MID"
            elif (row[ic50] > 500) & (row[ic50] <= 5000):
                return "LOW"
            else:
                return "none"

        df_aff['aff_cat'] = "none"
        df_aff['aff_cat'] = df_aff.apply( eval_aff, axis = 1)

        return [1, df_aff]

    ##THIS HAS NOT BEEN TESTED YET
    #Q: Is this the same as def compare_epitope_processing_all()??
    def retrieve_epitope_analysis_all( self, peptide_seq ):
        """
        combines information for both peptide processing (proteasome, TAP, MHC affinity) & peptide affinity to MHC allele by calling def retrieve_epitope_analysis() for all "analysis_type"
        NOTE: for IEDB, the peptide processing & MHC allele both print the "ic50" column: peptide_processing column name = "ic50_score", & peptide_affinity column name = "ic50"
        NOTE: if need to add multiple DataFrames, look at Method 2 in post "##17.9.13 - Pandas: Dataframe - merge more than 2 dataframes"
        Returns: returns an array where [0] = integer that is status of request & [1] = a pandas dataframe that contains the peptide-binding affinity to a given MHC. It has the following columns: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
            -[0] values:
                - -1 = request error
                -0 = request not ok (r.ok is False)
                -1 = request is ok
        """
        [rstat_1, df_1] = self.retrieve_epitope_analysis( peptide_seq, 1 )
        [rstat_2, df_2] = self.retrieve_epitope_analysis( peptide_seq, 2 )

        # if df_1.empty or df_2.empty:
        #     return pd.DataFrame( {'A' : []} )       #return empty dataframe

        if df_1.empty:
            return [rstat_1, pd.DataFrame( {'A' : []} )]       #return empty dataframe
        if df_2.empty:
            return [rstat_2, pd.DataFrame( {'A' : []} )]      #return empty dataframe

        #merges df_1 (MHC-affinity Only) and df_2 (Proteasome, TAP, & MHC), and matches entries based on 'allele' (MHC allele), 'start' (start position of peptide), 'end' (end position of peptide), & 'length' (length of peptide)
        df_all = pd.merge( df_1, df_2, on = ['allele', 'start', 'end', 'length'] )
        return [1, df_all]


    def compare_epitope_processing( self, pep1, pep2, analysis_type = 1 ):
        """
        A simple comparison betweeen peptide sequence 1 & peptide sequence 2 for antigen processing (proteasome, TAP, & MHC_1 binding)
        Args:
            -pep1 & pep2 = string that is amino acid sequence to be evaluated for affinity towards MHC alleles of interest. Usually pep1 is the original epitope & pep2 is the mutated epitope
            -analysis_type = integer with the following meaning
                -1 = perform analysis of peptide affinity to MHC
                -2 = perform analysis of peptide processing with proteasome, TAP, & MHC
        Returns: returns an array where [0] = integer that is status of request & [1] = a pandas dataframe that contains the peptide-binding affinity to a given proteasome & TAP. It has the following columns: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
            -[0] values:
                - -1 = request error
                -0 = request not ok (r.ok is False)
                -1 = request is ok 
        """
        if analysis_type == 1:
            ic50 = "ic50"
        elif analysis_type == 2:
            ic50 = "ic50_score"

        ##TEST::
        # print "pep1 = ", pep1
        # print "pep2 = ", pep2

        #NOTE: columns in dataframes are: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
        [rstat_1, df_pep1] = self.retrieve_epitope_analysis( pep1, analysis_type )
        [rstat_2, df_pep2] = self.retrieve_epitope_analysis( pep2, analysis_type )

        ##TEST::
        # print "df_pep1:"
        # print df_pep1
        # print "df_pep2:"
        # print df_pep2

        # if df_pep1.empty or df_pep2.empty:
        #     return pd.DataFrame( {'A' : []} )       #return empty dataframe
        if df_pep1.empty:
            return [rstat_1, pd.DataFrame( {'A' : []} )]       #return empty dataframe
        if df_pep2.empty:
            return [rstat_2, pd.DataFrame( {'A' : []} )]       #return empty dataframe

        df_all = pd.merge( df_pep1, df_pep2, on = ['allele', 'start', 'end', 'length'], suffixes = ("_1", "_2") )
        #create a new column to compare the affinity between peptide 1 & peptide 2. delta_aff = change in affinity from pep1 to pep2, where a lower value in 'ic50' will be a stronger affinity, and a lower 'percentile' (percentile_rank) means a higher affinity for MHC allele
        def calc_delta_aff( row, col_name, bool_inverse ):
            """
            determine if the new epitope '_2' (usually the mutated epitope) has a higher affinity to MHC allele than '_1' (usually the original epitope)
            Args:
                -row = each row from the dataframe
                -col_name = the prefix of the column name that will be compared
                -bool_inverse = boolean used for comparison between col_2 & col_1 (a comparison between numbers that are usually conveying some sort of affinity score). Note that '_2' is usually the after-effect (e.g. mutation) & '_1' is the original state (e.g. original nucleotide sequenced)
                    -True = means if col_2 > col_1, then the after-state affinity (col_2) is lower than the original state (col_1) & if col_2 < col_1, then the after-state affinity (col_2) is higher than the original (col_1).
                        -This is true for -1*IC50 (e.g. -log(IC50)) or a percentile rank where the lower the percentile the higher the affinity, basically anything where the lower the value, the higher it's concentration/affinity/performance/etc. (Use it for MHC_score & TAP score)
                    -False = means if col_2 > col_1, then the after-state affinity (col_2) is higher than the original state & if col_2 < col_1, then the after-state affinity (col_2) is lower than the original (col_1).
                        -This is true for when the value is larger, the concentration/affinity/etc. is also larger.
            """
            col_1 = col_name + '_1'
            col_2 = col_name + '_2'
            if row[col_2] > row[col_1]:
                return "lower" if bool_inverse else "higher"
            elif row[col_2] < row[col_1]:
                return "higher" if bool_inverse else "lower"
            else:
                return "equal"

        #NOTE: according to IEDB API (bottom of link: http://tools.iedb.org/processing/help/), the scores (proteasome, TAP, MHC) have been calculated so the higher the score, the higher the concentration (proteasome) or affinity (TAP & MHC, both use -log(IC50)). 
        #As they use MHC = -log( IC50 ): higher the peptide affinity for MHC allele -> higher the -log( IC50 ) -> the lower the IC50
        #As they use MHC = -log( IC50 ): lower the peptide affinity for MHC allele -> lower the -log( IC50 ) -> the higher the IC50
        if analysis_type == 1:
            #bool_inverse = True for this because the higher the IC50 value, the more concentration needed for the peptide to bind to the MHC allele (i.e. peptide has lower affinity to MHC allele)
            df_all['delta_aff'] = df_all.apply( calc_delta_aff, axis = 1, args = ('ic50',True,) )
        elif analysis_type == 2:
            #bool_inverse = False for all of these because if col_2 > col_1 value (col_2 = altered peptide, col_1 = non-altered peptide), this means higher concentration (proteasome) or higher affinity (TAP & MHC)
            df_all['delta_mhc_score'] = df_all.apply( calc_delta_aff, axis = 1, args = ('mhc_score',False,) )
            df_all['delta_proteasome_score'] = df_all.apply( calc_delta_aff, axis = 1, args = ('proteasome_score',False,) )
            df_all['delta_TAP_score'] = df_all.apply( calc_delta_aff, axis = 1, args = ('tap_score',False,) )

        return [1, df_all]

    #Q: Is this the same as "def retrieve_epitope_analysis_all()"
    def compare_epitope_processing_all( self, pep1, pep2 ):
        """
        A simple comparison betweeen peptide sequence 1 & peptide sequence 2 for antigen processing (proteasome, TAP, & MHC_1 binding)
        Args:
            -pep1 & pep2 = string that is amino acid sequence to be evaluated for affinity towards MHC alleles of interest. Usually pep1 is the original epitope & pep2 is the mutated epitope
            -analysis_type = integer with the following meaning
                -1 = perform analysis of peptide affinity to MHC
                -2 = perform analysis of peptide processing with proteasome, TAP, & MHC
            -bool_merge = boolean where,
                -True = will merge the comparison between both peptides 'pep1' & 'pep2'
                -False = will NOT merge the comparison between both peptides 'pep1' & 'pep2'
        Returns: Returns: returns an array where [0] = integer that is status of request & [1] = a pandas dataframe that contains the peptide-binding affinity to a given proteasome, TAP, & MHC. It has the following columns: allele, seq_num, start, end, length, peptide, ic50, percentile, rank
        -[0] values:
            - -1 = request error
            -0 = request not ok (r.ok is False)
            -1 = request is ok 
        """
        [rstat_1, df_1] = self.compare_epitope_processing( pep1, pep2, 1 )
        [rstat_2, df_2] = self.compare_epitope_processing( pep1, pep2, 2 )

        # if df_1.empty or df_2.empty:
        #     return pd.DataFrame( {'A' : []} )       #return empty dataframe
        if df_1.empty:
            return [rstat_1, pd.DataFrame( {'A' : []} )]       #return empty dataframe
        if df_2.empty:
            return [rstat_2, pd.DataFrame( {'A' : []} )]       #return empty dataframe   

        df_all = pd.merge( df_1, df_2, on = ['allele', 'start', 'end', 'length'] )
        return [1, df_all]

@staticmethod
def record_pep_mhc( hash_data, hash_pep_mhc, url_iedb_type = 1 ):
    """
    records the MHC affinity ('ic50') for each MHC 'allele'. Use this function if I just want the peptide sequence for each row & each column is MHC allele affinity
    Args:
        -hash_data = this is the data that should be sent to IEDB server. Example of hash_data
            hash_data = {
            "method": 'netmhcpan',
            "sequence_text": "SLYNTVATLAYSQCKRMNTKENLYE",
            "allele": "HLA-A*23:01,HLA-B*07:02,HLA-B*40:01,HLA-A*24:02",
            "length": "9,9,9,9"
            }
        -hash_pep_mhc = This will record the peptide and the MHC affinities associated with nested hash where k = peptide sequence & v = another hash where k2 = MHC allele & v2 = IC50 affinity
        -url_iedb_type = integer where
            -1 = calculates MHC-affinity only, URL = http://tools-cluster-interface.iedb.org/tools_api/mhci/"
            -2 = calculates proteasome, TAP, & MHC, URL = http://tools-cluster-interface.iedb.org/tools_api/processing/
    """
    url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/" if url_iedb_type == 1 else "http://tools-cluster-interface.iedb.org/tools_api/processing/"

    #retrieve peptide affinity to MHC
    r = requests.post( url, data = hash_data )
    file_strIO = StringIO( r.content )
    df_mhc = pd.read_csv( file_strIO, sep = '\t', header = 0 )

    for name, group in df_mhc.groupby( 'peptide' ):     #name = the peptide sequence, group = information about peptide binding to MHC allele, the following keys are: 'allele', 'seq_num', 'start', 'end', 'length', 'peptide', 'ic50'
        hash_pep_mhc[ name ] = {}
        for i_row, row in group.iterrows():
            hash_pep_mhc[ name ][ row['allele'] ] = row['ic50']

    return hash_pep_mhc
