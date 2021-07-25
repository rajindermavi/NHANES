import pandas as pd
import json 
from functools import reduce

class NHANES(object):
  
    def __init__(self):  
        self.repo_vars = json.load(open('config/repo_vars.json', 'r'))
        self.year_letter = json.load(open('config/year_letter.json', 'r'))
        self.df = None
        
    def get_xpt(self,dataset,cycle,cycle_code):
    
        path = cycle+'/'+dataset+'_'+cycle_code+'.XPT' 
        url = 'https://wwwn.cdc.gov/Nchs/Nhanes/'
        link = url+path
        print(link)
        xpt_df = pd.read_sas(link,index='SEQN')

        return xpt_df
    
    def get_vars(self,xpt_df,kept_vars):
    
        cols = set(xpt_df.columns.to_list()).intersection(kept_vars)
    
        return xpt_df[cols]    
        
    def construct_cycle_df(self,cycle,letter):
        
        df_repos_list = []
        for dataset, kept_vars in self.repo_vars.items():
            xpt_df = self.get_xpt(dataset,cycle,letter)
            df_repos_list.append(self.get_vars(xpt_df,kept_vars))

        return reduce(lambda x,y: pd.merge(x,y,on='SEQN',how='outer'),df_repos_list)
    
    def get(self):
        print('Fetching repos ... ') 
        for year, letter in self.year_letter.items():
            year = int(year)
            cycle = str(year)+'-'+str(year+1)
            cycle_df = self.construct_cycle_df(cycle, letter)
            
            self.df = cycle_df if self.df is None else pd.concat([self.df,cycle_df])
                  
if __name__ == '__main__':
    
    nhanes = NHANES()
    nhanes.get()