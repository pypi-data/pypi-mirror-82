

__all__ = ['ktable']


from Gaugi.messenger.macros import *
from Gaugi.tex import *
from Gaugi import Logger, expandFolders, load
from functools import reduce
import collections, os, glob, json, copy, re
import numpy as np
import pandas as pd

def calc_sp(pd, fa):
    return np.sqrt(np.sqrt(pd*(1-fa))*(0.5*(pd+(1-fa))))

class ktable( Logger ):

    def __init__(self, config_dict): 
        
        '''
        The objective of this class is extract the tuning information from saphyra's output and
        create a pandas DataFrame using then.
        The informations used in this DataFrame are listed in info_dict, but the user can add more
        information from saphyra summary for example.


        Arguments:
        - path_to_task_files: the path to the files that will be used in the extraction

        Ex.: /volume/v1_task/user.mverissi.*/* 
        the example above will get all the tuned files in the v1_task folder

        - config_dict: a dictionary contains in keys the measures that user want to check and
        the values need to be a empty list.

        Ex.: info = collections.OrderedDict( {
              
              "max_sp_val"      : 'summary/max_sp_val',
              "max_sp_pd_val"   : 'summary/max_sp_pd_val#0',
              "max_sp_fa_val"   : 'summary/max_sp_fa_val#0',
              "max_sp_op"       : 'summary/max_sp_op',
              "max_sp_pd_op"    : 'summary/max_sp_pd_op#0',
              "max_sp_fa_op"    : 'summary/max_sp_fa_op#0',
              'tight_pd_ref'    : "reference/tight_cutbased/pd_ref#0",
              'tight_fa_ref'    : "reference/tight_cutbased/fa_ref#0",
              'tight_pd_ref_passed'     : "reference/tight_cutbased/pd_ref#1",
              'tight_fa_ref_passed'     : "reference/tight_cutbased/fa_ref#1",
              'tight_pd_ref_total'      : "reference/tight_cutbased/pd_ref#2",
              'tight_fa_ref_total'      : "reference/tight_cutbased/fa_ref#2",
              'tight_pd_val_passed'     : "reference/tight_cutbased/pd_val#1",
              'tight_fa_val_passed'     : "reference/tight_cutbased/fa_val#1",
              'tight_pd_val_total'      : "reference/tight_cutbased/pd_val#2",
              'tight_fa_val_total'      : "reference/tight_cutbased/fa_val#2",
              'tight_pd_op_passed'      : "reference/tight_cutbased/pd_op#1",
              'tight_fa_op_passed'      : "reference/tight_cutbased/fa_op#1",
              'tight_pd_op_total'       : "reference/tight_cutbased/pd_op#2",
              'tight_fa_op_total'       : "reference/tight_cutbased/fa_op#2",

              } )

              kt = ktable( path_to_tunings, info, tag = 'v8' )

        - tag: a tag for the tuning

        '''
        Logger.__init__(self)
        self.__config_dict = config_dict
        self.pandas_table = None
        # Check wanted key type 
        if type(config_dict) is not collections.OrderedDict:
          MSG_FATAL( self ,"The wanted key must be an collection.OrderedDict to preserve the order inside of the dataframe.")
        #self.__fill_table( path )



    #
    # Fill the main dataframe with values from the tuning files and convert to pandas dataframe
    #
    def fill(self, basepath, tag):
        '''
        This method will fill the information dictionary and convert then into a pandas DataFrame.
        '''
        paths = expandFolders( basepath )
       
        MSG_INFO(self, "Reading file for %s tag...", tag )

        # Creating the dataframe
        dataframe = collections.OrderedDict({
                              'train_tag'      : [],
                              'et_bin'         : [],
                              'eta_bin'        : [],
                              'model_idx'      : [],
                              'sort'           : [],
                              'init'           : [],
                              'file_name'      : [],
                              'tuned_idx'      : [],
                          })

        # Complete the dataframe for each varname in the config dict
        for varname in self.__config_dict.keys():
            dataframe[varname] = []

        MSG_INFO(self, 'There are %i files for this task...' %(len(paths)))
        MSG_INFO(self, 'Filling the table... ')

        for ituned_file_name in paths:
            gfile = load(ituned_file_name)
            tuned_file = gfile['tunedData']
            
            for idx, ituned in enumerate(tuned_file):
                history = ituned['history']
                # get the basic from model
                dataframe['train_tag'].append(tag)
                dataframe['model_idx'].append(ituned['imodel'])
                dataframe['sort'].append(ituned['sort'])
                dataframe['init'].append(ituned['init'])
                dataframe['et_bin'].append(self.get_etbin(ituned_file_name))
                dataframe['eta_bin'].append(self.get_etabin(ituned_file_name))
                dataframe['file_name'].append(ituned_file_name)
                dataframe['tuned_idx'].append( idx )
                # Get the value for each wanted key passed by the user in the contructor args.
                for key, local  in self.__config_dict.items():
                    dataframe[key].append( self.__get_value( history, local ) )
        if self.pandas_table is None:
            self.pandas_table = pd.DataFrame(dataframe)
        else:
            MSG_INFO(self, 'Concatenate the previus Dataframe.')
            self.pandas_table = pd.concat([self.pandas_table, pd.DataFrame(dataframe)], ignore_index=True)
        
        MSG_INFO(self, 'End of fill step, a pandas DataFrame was created...')


    #
    # Get the value using recursive dictionary navigation
    #
    def __get_value(self, history, local):
        '''
        Return the value using recursive navigation
        '''
        # Protection to not override the history since this is a 'mutable' object
        var = copy.copy(history)
        for key in local.split('/'):
            var = var[key.split('#')[0]][int(key.split('#')[1])] if '#' in key else var[key]
        return var


    def get_etbin(self, job):
        '''
        A simple method to get the et bin in for a task.
        Arguments:
        -job: A item of tuned_file_list
        '''
        #print(re.findall(r'et[a]?[0-9]', job))
        #return int(re.findall(r'et[a]?[0-9]', job.split('/')[-2])[0][-1])
        return int(  re.findall(r'et[a]?[0-9]', job)[0][-1] )


    def get_etabin(self, job):
        '''
        A simple method to get the eta bin in for a task.
        Arguments:
        -job: A item of tuned_file_list
        '''
        #print(re.findall(r'et[a]?[0-9]', job))
        #return int(re.findall(r'et[a]?[0-9]', job.split('/')[-2])[1][-1])
        return int( re.findall(r'et[a]?[0-9]',job)[1] [-1] )




    #
    # Get the pandas dataframe
    #
    def get_pandas_table(self):
        '''
        Return the pandas table created in fill_table
        '''
        return self.pandas_table


    #
    # Return only best inits
    #
    def filter_inits(self, key):
        '''
        This method will filter the pandas DataFrame in order to get the best initialization for
        each sort. This filter need a key to ordenate the initialization and filter.
        Arguments:
        -key: a measure to use for filter the initializations

        Ex.: 
        # create a table_info
        Example = table_info(my_task_full_name, my_tuned_info, tag='my_flag')
        # fill table
        Example.fill_table()
        # now filter the inits using a max_sp_val
        my_df = Example.filter_inits(key='max_sp_val')

        In this example my_df is a pandas DataFrame with the best intilization sorted by 'max_sp_val'.
        '''
        return self.pandas_table.loc[self.pandas_table.groupby(['train_tag', 'et_bin', 'eta_bin', 'model_idx', 'sort'])[key].idxmax(), :]
   


    #
    # Get the best sorts from best inits table
    #
    def filter_sorts(self, pandas_best_inits, key):
        return pandas_best_inits.loc[pandas_best_inits.groupby(['train_tag', 'et_bin', 'eta_bin', 'model_idx'])[key].idxmax(), :]
 


    #
    # Calculate the mean/std table from best inits table
    #
    def describe(self, pandas_best_inits ):
        '''
        This method will give the mean and std for construct the beamer presentation for each train tag.
        Arguments:
        pandas_best_inits: a pandas Dataframe which contains all information for the best inits.
        '''
        # Create a new dataframe to hold this table
        dataframe = { 'train_tag' : [], 'et_bin' : [], 'eta_bin' : []}
        # Include all wanted keys into the dataframe
        for key in self.__config_dict.keys():
            if 'passed' in key: # Skip counts
                continue
            elif ('op' in key) or ('val' in key):
                dataframe[key+'_mean'] = []; dataframe[key+'_std'] = [];
            else:
                dataframe[key] = []
        
        # Loop over all tuning tags and et/eta bins
        for tag in pandas_best_inits.train_tag.unique():
            for et_bin in pandas_best_inits.et_bin.unique():
                for eta_bin in pandas_best_inits.eta_bin.unique():

                  cv_bin = pandas_best_inits.loc[ (pandas_best_inits.train_tag == tag) & (pandas_best_inits.et_bin == et_bin) & 
                                                  (pandas_best_inits.eta_bin == eta_bin) ]
                  dataframe['train_tag'].append( tag ); dataframe['et_bin'].append( et_bin ); dataframe['eta_bin'].append( eta_bin )
                  for key in self.__config_dict.keys():
                      if 'passed' in key:
                        continue
                      elif ('op' in key) or ('val' in key):
                          dataframe[key+'_mean'].append( cv_bin[key].mean() ); dataframe[key+'_std'].append( cv_bin[key].std() )
                      else:
                          dataframe[key].append( cv_bin[key].unique()[0] )

        # Return the pandas dataframe
        return pd.DataFrame(dataframe)



    #
    # Get tge cross val integrated table from best inits
    #
    def integrate( self, pandas_best_inits, tag ):
        '''
        This method is used to get the integrate information of a given tag.
        Arguments:
        pandas_best_inits: a pandas Dataframe which contains all information for the best inits.
        tag: the training tag that will be integrate.
        '''
        keys = [ key for key in self.__config_dict.keys() if 'passed' in key or 'total' in key]
        table = pandas_best_inits.loc[pandas_best_inits.train_tag==tag].groupby(['sort']).agg(dict(zip( keys, ['sum']*len(keys))))
        for key in keys:
            if 'passed' in key:
                orig_key = key.replace('_passed','')
                values = table[key].div( table[orig_key+'_total'] )
                table[orig_key] = values
                table=table.drop([key],axis=1)
                table=table.drop([orig_key+'_total'],axis=1)  
        
        return table.agg(['mean','std'])



    #
    # Dump all history for each line in the table
    #
    @classmethod
    def dump_all_history( cls, table, output_path , tag):
        '''
        This method will dump the train history. This is a way to get more easy this information when plotting the train evolution.
        Arguments:
        table: a table with the path information.
        output_path: the path to sabe the hitories.
        tag: the train tag.
        '''
        if not os.path.exists( output_path ):
          os.makedirs( output_path )
        for _ , row in table.iterrows():
            if row.train_tag != tag:
              continue
            # Load history
            history = load( row.file_name )['tunedData'][row.tuned_idx]['history']
            history['loc'] = {'et_bin' : row.et_bin, 'eta_bin' : row.eta_bin, 'sort' : row.sort, 'model_idx' : row.model_idx}
            name = 'history_et_%i_eta_%i_model_%i_sort_%i.json' % (row.et_bin,row.eta_bin,row.model_idx,row.sort)
            with open(os.path.join(output_path, '%s' %name), 'w') as fp:
                #json.dump(transform_serialize(history), fp)
                json.dump(str(history), fp)



    #
    # Dump the table to csv format
    #
    @classmethod
    def dump_table( cls, table, output_path, table_name):
        '''
        A method to save the pandas DataFrame created by table_info into a .csv file.
        Arguments:
        - table: the table created (and filtered) by table_info;
        - output_path: the file destination;
        - table_name: the file name;

        Ex.:
        # create a table_info
        Example = table_info(my_task_full_name, my_tuned_info, tag='my_flag')
        # fill table
        Example.fill_table()
        # now filter the inits using a max_sp_val
        my_df = Example.filter_inits(key='max_sp_val')
        # now save my_df
        Example.dump_table(my_df, my_path, 'a_very_meaningful_name')

        In this example, a file containing my_df, called 'a_very_meaningful_name.csv', will be saved in my_path
        '''
        table.to_csv(os.path.join(output_path, table_name+'.csv'), index=False)



    #
    # Dump beamer table
    #
    def dump_beamer_table( self, pandas_best_inits,
                           etbins, etabins, operation_points, doPDF=True,
                           output_file_name='beamer_pdf', tags=None ):
        '''
        This method will use a pandas Dataframe in order to create a beamer presentation which summary the tuning cross-validation.
        Arguments:
        pandas_best_inits: a pandas Dataframe which contains all information for the best inits.
        etbins/etabins: a list with the bins boundaries.
        operation_points: the operation point that will be used.
        doPDF: a flag to compile the pdf or leave it in .tex.
        output_file_name: a name for the pdf
        tags: the training tag that will be used. If None then the tags will be get from the Dataframe.
        '''
        cv_table = self.describe( pandas_best_inits )

        # Prepare the config dict using the operation points and some default keys
        config_dict = {}
        for operation_point in operation_points:
            config_dict[operation_point] = {}
            # reference val/op standard keys
            for key in ['pd_val', 'sp_val', 'fa_val', 'pd_op', 'sp_op', 'fa_op']:
                config_dict[operation_point][ key + '_mean' ] = operation_point + '_' + key + '_mean'
                config_dict[operation_point][ key + '_std' ] = operation_point + '_' + key + '_std'
            # reference keys
            config_dict[operation_point][ 'pd_ref' ] = operation_point + '_pd_ref'
            config_dict[operation_point][ 'sp_ref' ] = operation_point + '_sp_ref'
            config_dict[operation_point][ 'fa_ref' ] = operation_point + '_fa_ref'

        # Create Latex Et bins
        etbins_str = []; etabins_str = []
        for etBinIdx in range(len(etbins)-1):
            etbin = (etbins[etBinIdx], etbins[etBinIdx+1])
            if etbin[1] > 100 :
                etbins_str.append( r'$E_{T}\text{[GeV]} > %d$' % etbin[0])
            else:
                etbins_str.append(  r'$%d < E_{T} \text{[Gev]}<%d$'%etbin )
      
        # Create Latex eta bins
        for etaBinIdx in range( len(etabins)-1 ):
            etabin = (etabins[etaBinIdx], etabins[etaBinIdx+1])
            etabins_str.append( r'$%.2f<\eta<%.2f$'%etabin )
      
        # Default colors
        colorPD = '\\cellcolor[HTML]{9AFF99}'; colorPF = ''; colorSP = ''

        train_tags = cv_table.train_tag.unique() if not tags else tags
      
        # Dictionary to hold all eff values for each operation point, tag and et/eta binning
        summary = {}
        
        # Create the summary with empty values
        for operation_point in config_dict.keys():
            summary[operation_point] = {}
            for tag in train_tags:
                summary[operation_point][tag] = [ [ {} for __ in range(len(etabins)-1) ] for _ in range(len(etbins)-1)]
                for etBinIdx in range(len(etbins)-1):
                    for etaBinIdx in range(len(etabins)-1):
                        for key in config_dict[operation_point]:
                            summary[operation_point][tag][etBinIdx][etaBinIdx][key] = 0.0

        # Fill the summary
        for operation_point in config_dict.keys():
            for tag in train_tags:
                tag_table = cv_table.loc[ cv_table.train_tag == tag]
                for etBinIdx in tag_table.et_bin.unique():
                    for etaBinIdx in tag_table.eta_bin.unique():
                        for key in config_dict[operation_point]:
                            # We have only one line for each tag/et/eta bin
                            summary[operation_point][tag][etBinIdx][etaBinIdx][key] = tag_table.loc[ (tag_table.et_bin==etBinIdx) & 
                                (tag_table.eta_bin==etaBinIdx) ][config_dict[operation_point][key]].values[0]
      

        # Apply beamer
        with BeamerTexReportTemplate1( theme = 'Berlin'
                                 , _toPDF = doPDF
                                 , title = 'Cross Validation Table'
                                 , outputFile = output_file_name
                                 , font = 'structurebold' ):
        
            for operation_point in summary.keys():
                ### Prepare tables
                tuning_names = ['']; tuning_names.extend( train_tags )
                lines1 = []
                lines1 += [ HLine(_contextManaged = False) ]
                lines1 += [ HLine(_contextManaged = False) ]
                lines1 += [ TableLine( columns = ['','','kinematic region'] + reduce(lambda x,y: x+y,[['',s,''] for s in etbins_str]), _contextManaged = False ) ]
                lines1 += [ HLine(_contextManaged = False) ]
                lines1 += [ TableLine( columns = ['Det. Region','Method','Type'] + reduce(lambda x,y: x+y,[[colorPD+r'$P_{D}[\%]$',colorSP+r'$SP[\%]$',colorPF+r'$P_{F}[\%]$'] \
                                      for _ in etbins_str]), _contextManaged = False ) ]
                lines1 += [ HLine(_contextManaged = False) ]
      
                for etaBinIdx in range(len(etabins) - 1):
                    for idx, tag in enumerate( train_tags ):
                        cv_values=[]; ref_values=[]
                        for etBinIdx in range(len(etbins) - 1):
                            d = summary[operation_point][tag][etBinIdx][etaBinIdx]
                            sp = d['sp_val_mean']*100; sp_std = d['sp_val_std']*100
                            pd = d['pd_val_mean']*100; pd_std = d['pd_val_std']*100
                            fa = d['fa_val_mean']*100; fa_std = d['fa_val_std']*100
                            refsp = d['sp_ref']*100; refpd = d['pd_ref']*100; reffa = d['fa_ref']*100
                            cv_values   += [ colorPD+('%1.2f$\pm$%1.2f')%(pd,pd_std),colorSP+('%1.2f$\pm$%1.2f')%(sp,sp_std),colorPF+('%1.2f$\pm$%1.2f')%(fa,fa_std),    ]
                            ref_values  += [ colorPD+('%1.2f')%(refpd), colorSP+('%1.2f')%(refsp), colorPF+('%1.2f')%(reffa)]
                        ### Make summary table
                        if idx > 0:
                            lines1 += [ TableLine( columns = ['', tuning_names[idx+1], 'Cross Validation'] + cv_values   , _contextManaged = False ) ]
                        else:
                            lines1 += [ TableLine( columns = ['\multirow{%d}{*}{'%(len(tuning_names))+etabins_str[etaBinIdx]+'}',tuning_names[idx], 'Reference'] + ref_values   , 
                                                _contextManaged = False ) ]
                            lines1 += [ TableLine( columns = ['', tuning_names[idx+1], 'Cross Validation'] + cv_values    , _contextManaged = False ) ]
      
                    lines1 += [ HLine(_contextManaged = False) ]
                lines1 += [ HLine(_contextManaged = False) ]
      

                ### Calculate the final efficiencies
                lines2 = []
                lines2 += [ HLine(_contextManaged = False) ]
                lines2 += [ HLine(_contextManaged = False) ]
                lines2 += [ TableLine( columns = ['',colorPD+r'$P_{D}[\%]$',colorPF+r'$P_{F}[\%]$'], _contextManaged = False ) ]
                lines2 += [ HLine(_contextManaged = False) ]
                for idx, tag in enumerate( train_tags ):
                    # get the integrate efficiency
                    itable = self.integrate( pandas_best_inits, tag )
                    # we need to use val values
                    pd = itable[operation_point+'_pd_val'].values[0]*100
                    pd_std = itable[operation_point+'_pd_val'].values[1]*100
                    fa = itable[operation_point+'_fa_val'].values[0]*100
                    fa_std = itable[operation_point+'_fa_val'].values[1]*100
                    pdref = itable[operation_point+'_pd_ref'].values[0]*100
                    faref = itable[operation_point+'_fa_ref'].values[0]*100
                    if idx > 0:
                        lines2 += [ TableLine( columns = [tag ,colorPD+('%1.2f$\pm$%1.2f')%(pd,pd_std),colorPF+('%1.2f$\pm$%1.2f')%(fa,fa_std) ], _contextManaged = False ) ]
                    else:
                      lines2 += [ TableLine( columns = ['Ref.' ,colorPD+('%1.2f')%(pdref),colorPF+('%1.2f')%(faref) ], _contextManaged = False ) ]
                      lines2 += [ TableLine( columns = [tag ,colorPD+('%1.2f$\pm$%1.2f')%(pd,pd_std),colorPF+('%1.2f$\pm$%1.2f')%(fa,fa_std) ], _contextManaged = False ) ]


                # Create all tables into the PDF Latex 
                with BeamerSection( name = operation_point.replace('_','\_') ):
                    with BeamerSlide( title = "The Cross Validation Efficiency Values For All Tunings"  ):          
                        with Table( caption = 'The $P_{D}$, $P_{F}$ and $SP $ values for each phase space for each method.') as table:
                            with ResizeBox( size = 1. ) as rb:
                                with Tabular( columns = '|lcc|' + 'ccc|' * len(etbins_str) ) as tabular:
                                    tabular = tabular
                                    for line in lines1:
                                        if isinstance(line, TableLine):
                                            tabular += line
                                        else:
                                            TableLine(line, rounding = None)

                    with BeamerSlide( title = "The General Efficiency"  ):          
                        with Table( caption = 'The general efficiency for the cross validation method for each method.') as table:
                            with ResizeBox( size = 0.7 ) as rb:
                                with Tabular( columns = 'lc' + 'c' * 2 ) as tabular:
                                    tabular = tabular
                                    for line in lines2:
                                        if isinstance(line, TableLine):
                                            tabular += line
                                        else:
                                            TableLine(line, rounding = None)




