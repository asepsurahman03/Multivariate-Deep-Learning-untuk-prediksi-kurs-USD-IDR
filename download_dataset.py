import yfinance as yf
import pandas as pd
import time
import datetime

START_DATE = '2016-06-01'
END_DATE = '2026-06-01'

YF_TICKERS = {
    'USD_IDR': 'USDIDR=X',
    'IHSG': '^JKSE',
    'Gold': 'GC=F',
    'Crude_Oil': 'CL=F',
    'Nasdaq': '^IXIC',
    'SP500': '^GSPC',
    'Dow_Jones': '^DJI',
    'Bitcoin': 'BTC-USD',
    'Brent_Oil': 'BZ=F'
}

def fetch_yfinance_data(tickers, start, end, max_retries=3):
    print("Fetching data from Yahoo Finance...")
    df_list = []
    for name, ticker in tickers.items():
        success = False
        for attempt in range(max_retries):
            try:
                print(f"  -> Downloading {name} ({ticker}) [Attempt {attempt+1}/{max_retries}]...")
                data = yf.download(ticker, start=start, end=end, progress=False)
                if not data.empty:
                    # Handle multi-level columns in recent yfinance versions
                    if isinstance(data.columns, pd.MultiIndex):
                        df = data['Close']
                    else:
                        df = data[['Close']]
                    
                    # Make sure it is a DataFrame and rename the column
                    if isinstance(df, pd.Series):
                        df = df.to_frame()
                    df.columns = [name]
                    df_list.append(df)
                    success = True
                    break
                else:
                    print(f"     Failed to download {name} - Data is empty")
            except Exception as e:
                print(f"     Error downloading {name}: {e}")
            time.sleep(2) # Respect API limits and wait before retry
            
        if not success and name == 'USD_IDR':
            print("CRITICAL: Failed to download target variable USD_IDR. Trying fallback ticker 'IDR=X'...")
            try:
                data = yf.download('IDR=X', start=start, end=end, progress=False)
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        df = data['Close']
                    else:
                        df = data[['Close']]
                    if isinstance(df, pd.Series):
                        df = df.to_frame()
                    df.columns = [name]
                    df_list.append(df)
                    success = True
                else:
                    print("     Fallback failed as well.")
            except Exception as e:
                print(f"     Error with fallback: {e}")
        
    if df_list:
        merged_df = pd.concat(df_list, axis=1)
        if 'USD_IDR' not in merged_df.columns:
            raise ValueError("FATAL ERROR: The target variable 'USD_IDR' could not be downloaded. Please check your internet connection or Yahoo Finance status.")
        return merged_df
    return pd.DataFrame()

df_raw = fetch_yfinance_data(YF_TICKERS, START_DATE, END_DATE)
df_clean = df_raw.ffill().bfill().interpolate(method='linear').dropna()

output_path = 'indonesian_economic_indicators_final.csv'
df_clean.to_csv(output_path)
print(f"Successfully saved clean dataset to {output_path}")
