import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import helper
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

st.title("WhatsApp Chat Analyzer")


st.write("Welcome to the WhatsApp Chat Analyzer! This tool allows you to analyze WhatsApp chat data.")
st.write("To get started, follow these steps:")


st.write("1. Upload a WhatsApp chat file using the 'Choose a file' button in the sidebar.")
st.write("2. Select a user to view the analysis for or choose 'Overall' to see group-level analysis.")
st.write("3. Click the 'Show Analysis' button to perform the analysis.")


st.markdown("---")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        # st.dataframe(df)
    
        
        

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
            
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig) 
        
         # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
          # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
           


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        
        most_common_df = helper.most_frequent_words(df, selected_user)

        if most_common_df is not None:
            if 'Word' in most_common_df.columns and 'Count' in most_common_df.columns:
                col1, col2 = st.columns(2)
            
                with col1:
                    st.title('Most Used Words')
                    
                    fig1, ax1 = plt.subplots()
                    ax1.bar(most_common_df['Word'], most_common_df['Count'], color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig1)

                with col2:
                    st.title('Most Common Words DataFrame')
                    st.dataframe(most_common_df)
            else:
                st.write("The DataFrame does not contain the necessary columns.")
        else:
            st.write("No data available for displaying most common words.")

        # Emoji Analysis    
        emoji_df=helper.emoji_helper(selected_user,df)
        if most_common_df is not None:  
            st.title('Emoji Analysis')
            col1, col2 = st.columns(2)
            with col1:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
            
                
            with col2:    
                st.dataframe(emoji_df)
            
    
    st.markdown("---")
    st.markdown("Copyright © 2023 Kannan Khosla. All rights reserved.")
        
            

        
        




