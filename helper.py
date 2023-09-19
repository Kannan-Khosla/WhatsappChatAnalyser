from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re
import nltk.corpus
from nltk.corpus import stopwords

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    temp = df[df['user'] != 'INDSA Events & Updates 🇮🇳']
    x = temp['user'].value_counts().head()
    
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def most_frequent_words(df,selected_user):
    if selected_user == 'Overall':
        # df = df[df['user'] == selected_user]
        word_counts = Counter()
        f = open('stop_hinglish.txt','r')
        stop_words_1 = f.read()
        stop_words = set(stopwords.words('english'))
        
        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
        dataset = temp['message']
        most_frequent_words = {
        'pm': 1235, 'group': 517, 'link': 497, 'using': 449, 'invite': 439, 'joined': 431,
        'omitted': 355, 'image': 306 }
        
        ew = list(most_frequent_words.keys())

        
        for text in dataset:
            words = re.findall(r'\w+', text.lower())  # Tokenize and convert to lowercase
            words = [word for word in words if word not in stop_words and not word.isdigit() and word not in ew and word not in stop_words_1 ]  # Remove stopwords and numbers
            word_counts.update(words)
        
        most_common_words = word_counts.most_common(10)
        
        
        df_most_common = pd.DataFrame(most_common_words, columns=['Word', 'Count'])
        
        return df_most_common
    
    
    # most_frequent_words_df = count_most_frequent_words(df, num_words=20)
    
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap















