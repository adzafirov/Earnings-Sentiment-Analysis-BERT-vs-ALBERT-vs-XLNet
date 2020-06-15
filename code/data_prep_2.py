
import os, nltk, re
import pandas as pd
from nltk.tokenize import sent_tokenize


raw_file_dir = "C://Users//canth//Dropbox//UCLA//A3 NLP//project//factiva queries 2"
separate_files_dir = "C://Users//canth//Dropbox//UCLA//A3 NLP//project//separate files 2"
final_dir = "C://Users//canth//Dropbox//UCLA//A3 NLP//project"
invalid = '<>:"/\|?*'
#for i in range(1990, 2020): os.mkdir(separate_files_dir + "//" + str(i))

raw_files = os.listdir(raw_file_dir)

# Initialize
#cols = {'year': ['year'],        'ticker': ['ticker'],        'exchange': ['exchange'],        'text': ['text']        }
df = pd.DataFrame([], columns = ['year', 'ticker', 'exchange', 'text'])

for raw_file in raw_files:

    filepath = raw_file_dir + "//" + raw_file
    year = raw_file[0:4]
    text_file = open(filepath, "r", errors='ignore').read()

    if text_file.find('Document BWR') > -1:
        files = text_file.split("Document BWR")
    elif text_file.find('Document bwr') > -1:
        files = text_file.split("Document bwr")
    else:
        raise Exception("DZ: Split error 1")


    for i in range(0, files.__len__()-1):

        if i == 0:
            new_file = files[0].split("Skip to main content\nDow Jones Factiva\nDow Jones\n")[1]
        else:
            length = files[i].__len__()
            new_file = files[i][25:length]

        split_file = new_file.split("\n")

        title = split_file[0]
        date = split_file[2]

        if text_file.find('BUSINESS WIRE)') > 0:
            split_str = 'BUSINESS WIRE\)'
        elif text_file.find('Business Wire)') > 0:
            split_str = 'Business Wire\)'
        elif text_file.find('Business Wire. All Rights Reserved.') > 0:
            split_str = 'Business Wire. All Rights Reserved.'
        else: raise Exception("DZ: Split error 2")


        text = re.split(split_str, new_file, flags=re.IGNORECASE)
        text = text[text.__len__()-1]
        sentences = sent_tokenize(text)

        # Keep first 10 sentences, exclude tables
        count = 0
        sample_text = []
        for j in range(0,sentences.__len__()):
            #print(str(j+1)+": "+sentences[j])
            if sentences[j].count(' ') < 100: # excludes tables
                sample_text.append(sentences[j])
                count += 1
            if count >= 10: break

        if sentences.__len__() >= 5: # at least 5 sentences
            sample_text = sentences[0:9]

            temp = re.findall('\(.*?:.*?\)', text)

            if temp.__len__()>0:
                if temp[0].__len__() < 30:
                    temp = temp[0].replace('(', '').replace(')', '').replace(' ', '').replace('/', '_')
                    temp = re.split(":", temp, flags=re.IGNORECASE)
                    exchange = temp[0]
                    ticker = temp[1]

                    if re.search("NASDAQ", exchange, re.IGNORECASE): exchange = "NASDAQ"
                    elif re.search("NYSE", exchange, re.IGNORECASE): exchange = "NYSE"
                    elif re.search("AMEX", exchange, re.IGNORECASE): exchange = "AMEX"
                    elif re.search("OTC", exchange, re.IGNORECASE): exchange = "OTC"
                    elif re.search("TSX", exchange, re.IGNORECASE): exchange = "TSX"
                    elif re.search("TSE", exchange, re.IGNORECASE): exchange = "TSX"
                    else: exchange = "Other"

                    print("exchange: ", exchange, ". ticker: ", ticker)

                    for char in invalid: ticker = ticker.replace(char, '')
                    for char in invalid: exchange = exchange.replace(char, '')
                    for char in invalid: title = title.replace(char, '')


                    file = open(separate_files_dir + "//" + year + "//" + "(" + exchange + ")" + ticker + "_" + year + ".txt", "w")
                    body = ""
                    for h in range (0,sample_text.__len__()):
                        file.write(sample_text[h])
                        body += sample_text[h]
                    file.close()

                    df = df.append({'year':int(year), 'ticker':ticker, 'exchange':exchange, 'text':body}, ignore_index=True)


                else: print("cannot find ticker 2: " + title[0:200])
            else: print("cannot find ticker 1: " + title[0:200])


    print(filepath)
    print(year)

df.to_csv(final_dir + '//final_texts.csv', index=False)

df_sales = pd.read_csv(r"C:\Users\canth\Dropbox\UCLA\A3 NLP\project\compustat\compustat_data_lean_1.csv")

new_df = pd.merge( df_sales, df, how='left', left_on=['year','ticker','stock_exchange'], right_on = ['year','ticker','exchange'])
new_df = new_df.dropna(how='any', subset=['sales_sentiment', 'text'])

new_df.to_pickle(final_dir + "//final_merged_sample.pkl")

lean_df = new_df[['sales_sentiment','text']]
lean_df.to_pickle(final_dir + "//final_lean_sample.pkl")


#test = pd.read_pickle(final_dir + "//final_merged_sample.pkl")

