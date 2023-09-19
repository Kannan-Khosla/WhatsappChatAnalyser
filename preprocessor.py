import re
import pandas as pd

def preprocess(data):
    pattern = r'\[\d{4}-\d{2}-\d{2}, \d{2}:\d{2}:\d{2} [APap][Mm]\]'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
# convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='[%Y-%m-%d, %I:%M:%S %p]')
    um=[]
    for i in df['user_message']:
        i.strip()
        um.append(i)
    df['user_message_new'] = um  
    
    users = []
    messages = []
    for message in df['user_message_new']:
        user, message_content = message.split(':', 1)
        user = user.strip()  # Remove leading and trailing whitespace
        message_content = message_content.strip()  # Remove leading and trailing whitespace
        messages.append(message_content)
        if user=='INDSA Events & Updates 🇮🇳':
            users.append('group_notification')
        else:
            users.append(user)
    
    df['user'] = users
    df['message'] = messages
    df['only_date'] = df['message_date'].dt.date
    df.drop(columns=['user_message_new'],inplace=True)
    df.drop(columns=['user_message'],inplace=True)
    df['month_num'] = df['message_date'].dt.month
    df['year'] = df['message_date'].dt.year
    df['only_date'] = df['message_date'].dt.date
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['day_name'] = df['message_date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    
    return df
    
        
    

    

