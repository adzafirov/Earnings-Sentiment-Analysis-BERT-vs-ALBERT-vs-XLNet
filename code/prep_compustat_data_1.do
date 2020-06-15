
clear
import delimited "C:\Users\canth\Dropbox\UCLA\A3 NLP\project\compustat\7cad0e7e8517cde6.csv"

keep if fqtr==1 
drop consol popsrc costat indfmt consol popsrc datafmt curcdq fqtr niq

duplicates drop  gvkey fyearq, force
tsset gvkey fyearq 

* Authors' notes:
*In our context, we label an earnings announcement as “positive” (and thus likely to contain “positive”
*language or tone within the text of the announcement) whenever the year-on-year percentage
*change in a company’s quarterly sales is above the sample median for that calendar quarter.
* “positive” = 1, "negative" = 0

gen sales_yoy = revtq/L.revtq-1
drop if missing(sales_yoy)
drop if missing(datacqtr)

sort datacqtr
by datacqtr: egen median_sales_yoy  = median(sales_yoy)

gen sales_sentiment = 0
replace sales_sentiment = 1 if sales_yoy > median_sales_yoy


drop revtq median_sales_yoy gvkey


gen stock_exchange = ""
replace stock_exchange ="OTC" if exchg==0
replace stock_exchange ="OTC" if exchg==1
replace stock_exchange ="Consolidated Parent or Tracking Stock Company" if exchg==2
replace stock_exchange ="Leveraged Buyout" if exchg==3
replace stock_exchange ="Additional Company Record-PreSFAS 94, ProForma, PreAmended" if exchg==4
replace stock_exchange ="TSX" if exchg==7
replace stock_exchange ="Montreal Stock Exchange" if exchg==8
replace stock_exchange ="Canadian Venture Exchange" if exchg==9
replace stock_exchange ="Alberta Stock Exchange" if exchg==10
replace stock_exchange ="NYSE" if exchg==11
replace stock_exchange ="AMEX" if exchg==12
replace stock_exchange ="OTC" if exchg==13
replace stock_exchange ="NASDAQ" if exchg==14
replace stock_exchange ="Boston Stock Exchange" if exchg==15
replace stock_exchange ="Midwest Exchange (Chicago)" if exchg==16
replace stock_exchange ="Pacific Exchange" if exchg==17
replace stock_exchange ="Philadelphia Exchange" if exchg==18
replace stock_exchange ="OTC" if exchg==19
replace stock_exchange ="OTC" if exchg==20

replace stock_exchange ="Other" if stock_exchange !="TSX" & stock_exchange !="NYSE" & stock_exchange !="AMEX" & stock_exchange !="NASDAQ" & stock_exchange !="OTC"
tab stock_exchange


gen cyear = substr(datacqtr,1,4)
destring cyear, replace 

order cyear tic sales_sentiment conm stock_exchange datadate datacqtr datafqtr fyearq  

export delimited using "C:\Users\canth\Dropbox\UCLA\A3 NLP\project\compustat\compustat_data_cleaned_1.csv", replace

keep cyear tic stock_exchange sales_sentiment conm sales_yoy
ren cyear year 
ren tic ticker
ren conm company_name

order sales_sentiment sales_yoy   company_name stock_exchange  year ticker


export delimited using "C:\Users\canth\Dropbox\UCLA\A3 NLP\project\compustat\compustat_data_lean_1.csv", replace
save  "C:\Users\canth\Dropbox\UCLA\A3 NLP\project\compustat\compustat_data_lean_1.dat", replace




