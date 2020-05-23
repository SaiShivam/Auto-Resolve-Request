""" Data extraction for internal sites get modefy access"""
import re
import pandas as pd
import numpy as np

class InternalSitesGetModifyAccess():
    """
        Class intermal sites  get modify access.
    """
    def __init__(self):
        self.URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|info|)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil)\b/?(?!@)))"""
        self.email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    def data_extraction(self,validation_data):
        """ Extracting users , urls and sitename from the description"""
        users = []
        user = []
        urls = []
        sitename = []
        validation_data.nourldata = validation_data.Description.apply(lambda x: re.sub(r'(https?://\S+)', '', x))
        for line in validation_data.nourldata:
            valid_user = re.sub(self.URL_REGEX,'', line)
            raw_user = re.findall(self.email_regex, valid_user)
            for each in raw_user:
                user_ = each.split('@')
                user.append(user_[0])
            user_clean = re.sub("@\S+", "", valid_user)
            if len(user) != 0:
                users.append(list(set(user)))
            else:
               users.append(list(set(validation_data['Created By'])))
        for line in validation_data.Description:
            link = re.findall(self.URL_REGEX, line)
            urls.append(list(set(link)))
        validation_data['URL'] = pd.DataFrame({'col1': urls})
        validation_data['Users'] = pd.DataFrame({'col2': users})
        validation_data['URL'] = validation_data['URL'].apply(lambda x: ', '.join(x))
        validation_data['Users'] = validation_data['Users'].apply(lambda x: ', '.join(x))
        validation_data['SiteName'] = pd.DataFrame({'col3': sitename})
        validation_data['SiteName'] = validation_data['URL'].apply(lambda x: (str(x).split(r'/')[-2] if str(x).endswith("/")  else str(x).split(r'/')[-1] ) if x else '')
        validation_data['SiteName'] = validation_data['SiteName']
        validation_data['Users'] = validation_data['Users'].replace("", np.nan)
        validation_data.Users.fillna(validation_data['Created By'], inplace=True)
        validation_data['Automation Recommendation'] = ''
        cols = ['Automation Recommendation','Recommendation', 'Application', 'Users', 'SiteName', 'IsSupported', 'Confidence']
        validation_data = validation_data[cols]
        validation_data.rename(columns={'Recommendation':'Intent','Users':'UserEnterpriseId'},inplace=True)
        validation_data = validation_data[['Automation Recommendation','Application','Confidence','Intent','IsSupported','SiteName','UserEnterpriseId']]
        return validation_data