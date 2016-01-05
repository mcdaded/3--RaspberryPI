"""
Renewal Model - 2016-01-04 - 'client_features.py' created on 1/4/2016 at 5:24 PM

@author: dmcdade
"""

__author__ = 'dmcdade'

import pandas as pd
import numpy as np
from __utils import DevBox


class ClientFeatures(DevBox):
    """
    Get list of clients for data aggregation. Inherits from parent MDM dev box connector/controller.

    Parameters
    ----------

    Attributes
    ---------

    """
    def __init__(self):
        DevBox.__init__(self)
        self.client_data = pd.DataFrame()
        self.client_features = pd.DataFrame()

    def get_client_data(self):
        """
        Get the customers and their aggregate account metadata information. We will also retrieve the primary metric
        of interest here, weather the client renewed or churned.

        Parameters
        ----------

        Returns
        -------
        customer_df: pandas DataFrame of .
        """
        query_str = """
        SELECT DISTINCT
            main_client.id AS ClientId ,
            main_client.abbreviation AS AccountNumber ,
            account.id AS AccountId ,
            account.name AS AccountName ,
            account.type AS AccountType ,
            opp.id AS OpportunityId ,
            CASE WHEN account.current_crm_system_c = 'Salesforce.com' THEN 'SFDC'
                 WHEN account.current_crm_system_c IN ('Bullhorn', 'Sendouts', 'MaxHire', 'Bulhorn') THEN 'Staffing'
                 WHEN account.current_crm_system_c IN ('Jobscience', 'Akken', 'PC Recruiter') THEN 'Sunset'
                 WHEN opp.loss_reason_c = 'Retired Product' THEN 'Sunset'
            ELSE 'Sunset' END AS Product ,
            opp.close_date AS CloseDate ,
            LAST_DAY(opp.contract_start_c) AS ContractStart ,
            LAST_DAY(DATE_ADD(opp.contract_end_c, INTERVAL -1 MONTH)) as ContractEnd ,
            opp.stage_name StageName ,
            account.number_of_employees ,
            opp.loss_reason_c AS LossReason ,
            opp.amount * COALESCE(fx.conversion_rate, 1.0) AS Amount_USD ,
            line_item.list_price ,
            line_item.quantity ,
            line_item.unit_price ,
            line_item.months_c ,
            line_item.list_price * line_item.quantity * line_item.months_c * COALESCE(fx.conversion_rate, 1.0) AS ListPrice_USD ,
            line_item.unit_price * line_item.quantity * line_item.months_c * COALESCE(fx.conversion_rate, 1.0) AS UnitPrice_USD ,
            opp.type as OpportunityType ,
            CASE WHEN opp.early_termination_date_c IS NULL THEN 0 ELSE 1 END AS EarlyTerm
        FROM insightsquared.main_client main_client
        JOIN insightsquared_is2.sfdc_warehouse_Account account
            ON account.account_number = main_client.abbreviation AND account.type IN ('Customer', 'Customer Churned')
        INNER JOIN insightsquared_is2.sfdc_warehouse_Opportunity opp
            ON opp.account_id = account.id
        LEFT JOIN insightsquared_is2.sfdc_warehouse_OpportunityLineItem line_item ON line_item.opportunity_id = opp.id
        LEFT JOIN insightsquared_is2.sfdc_warehouse_CurrencyType fx ON fx.iso_code = opp.currency_iso_code
        WHERE opp.contract_start_c IS NOT NULL AND opp.contract_end_c IS NOT NULL
        AND opp.type <> 'Cross Sell'
        ORDER BY 1, 2, 3, 9, 10
        """
        customer_df = self.query(query_str)
        customer_df['ContractStart'] = customer_df['ContractStart'].apply(lambda x: pd.to_datetime(x).date())
        customer_df['ContractEnd'] = customer_df['ContractEnd'].apply(lambda x: pd.to_datetime(x).date())
        customer_df['Amount_USD'] = customer_df['Amount_USD'].fillna(0).astype(float)
        customer_df['ListPrice_USD'] = customer_df['ListPrice_USD'].fillna(0).astype(float)
        customer_df['UnitPrice_USD'] = customer_df['UnitPrice_USD'].fillna(0).astype(float)
        self.client_data = customer_df
        return customer_df

    def get_client_features(self, data):
        """
        Transform the raw salesforce/product client data into a usable feature set for the renewal model.

        Parameters
        ----------
        data:

        Returns
        -------

        """
        new_business = data[data.OpportunityType == 'New Business']
        upsell = data[data.OpportunityType == 'Upsell']
        renewal = data[data.OpportunityType == 'Renewal']
        contract = data[data.OpportunityType.isin(['New Business', 'Renewal'])]
        client_feature_df = pd.DataFrame()
        self.client_features = client_feature_df
        # iterate over the new business and renewal contracts. append upsells (if any)
        # and determine overall average price per seat
        return client_feature_df

