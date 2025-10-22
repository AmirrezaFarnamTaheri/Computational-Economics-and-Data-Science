
import pandas as pd
import numpy as np
import os

def create_mock_data():
    """Creates mock data files for the notebook to run."""
    if not os.path.exists('data'):
        os.makedirs('data')

    # 1. Create mock Goyal-Welch dataset
    gw_data = {
        'Rfree': np.random.rand(100) * 0.01,
        'CRSP_SPvw': np.random.rand(100) * 0.05,
        'dp': np.random.rand(100),
        'ep': np.random.rand(100),
        'bm': np.random.rand(100),
        'ntis': np.random.rand(100),
        'tbl': np.random.rand(100),
        'svar': np.random.rand(100)
    }
    gw_df = pd.DataFrame(gw_data, index=pd.to_datetime(pd.date_range(start='1950-01-01', periods=100, freq='M')))

    with pd.ExcelWriter('data/PredictorData2021.xlsx') as writer:
        gw_df.to_excel(writer, sheet_name='Monthly')

    # 2. Create mock World Development Indicators dataset
    countries = ['USA', 'CHN', 'JPN', 'DEU', 'GBR']
    indicators = {
        'SP.DYN.LE00.IN': 'LifeExpectancy',
        'NY.GDP.PCAP.KD': 'GDP_per_Capita',
        'SE.PRM.ENRR': 'PrimarySchoolEnrollment'
    }

    wdi_data = []
    for country in countries:
        for code, name in indicators.items():
            wdi_data.append({
                'Country Name': country,
                'Year': 2014,
                'Indicator Code': code,
                'Indicator Name': name,
                'Value': np.random.rand() * 1000
            })

    wdi_df = pd.DataFrame(wdi_data)
    wdi_df.to_csv('data/indicators.csv', index=False)

    print("Mock data files created successfully.")

if __name__ == '__main__':
    create_mock_data()
