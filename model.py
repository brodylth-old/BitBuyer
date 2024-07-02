import xgboost as xgb
import pandas as pd
import json
from datetime import datetime, date, timedelta

df = pd.read_csv('spy_historical.csv')
df.index = pd.to_datetime(df['Date'])
df = df.drop('Date', axis=1)

def create_time_features(df):
    df = df.copy()
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['DOM'] = df.index.day
    df['DOW'] = df.index.dayofweek
    return df

def create_market_features(df):
    df = df.copy()
    df['Gain'] = (df['Close'] > df['Open']).astype(int)
    df['Lagged_Gain'] = df['Gain'].shift(1)
    df['Rolling_Gain'] = df['Gain'].rolling(7).mean()
    df['Difference'] = df['Close'] - df['Open']
    df['Lagged_Difference'] = df['Difference'].shift(1)
    df['Rolling_Difference'] = df['Lagged_Difference'].rolling(7).mean()
    df['Range'] = df['High'] - df['Low']
    df['Lagged_Range'] = df['Range'].shift(1)
    return df

df = create_time_features(df)
df = create_market_features(df)
df = df.dropna()

FEATURES = ['Year', 'Month', 'DOM', 'DOW', 'Lagged_Gain', 'Rolling_Gain', 'Lagged_Difference', 'Rolling_Difference', 'Lagged_Range']
TARGET =  ['Gain']

train_df = df.copy()
X_train = train_df[FEATURES]
y_train = train_df[TARGET]

reg = xgb.XGBClassifier(eval_metric='logloss')
reg.fit(X_train, y_train)

today = date.today()
tomorrow = today + timedelta(days=1)
future_daterange = pd.date_range(tomorrow, tomorrow, freq='D')
future_df = pd.DataFrame(index=future_daterange)
future_df['isfuture'] = True
df['isfuture'] = False
df_and_future = pd.concat([df, future_df])
df_and_future = create_time_features(df_and_future)
df_and_future = create_market_features(df_and_future)
future_with_features = df_and_future.query('isfuture').copy()
future_with_features = future_with_features[FEATURES]

future_with_features['pred'] = reg.predict(future_with_features)
print(int(future_with_features.iloc[0]['pred']))