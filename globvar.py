# global pricecalled
#####Declaring Global variables
global num_of_contries, num_of_markets, irp_time_frame
#List that contains references to sheets of Excel file
global xl_sheet
#Lists to store informations from "InputInterface" sheet
global countries, dossier_submission_date, price_approval_date, price_publication_date, reimbursement_date, volume_pickup_dates, base_prices, pricevol
#Lists to store informations from "PriceOverrideAndProdDiscd" sheet
global priceOverrideAndProdDiscd
#Lists to store informations from "PriceCut" sheet
global priceCut
#At launch data
global multi_single_delay, num_refrence_rule, irp_noirp, reference_rules, multiplier_factor, delay_price, irp_from_date, price_rules, min_contries, max_contries
###List to have discounts
global discountLevel
#Post launch data
global num_refrence_rule_pl, irp_noirp_pl, reference_rules_pl, multiplier_factor_pl, delay_price_pl, irp_from_date_pl
global periodicity, periodicity_date, price_rules_pl, min_contries_pl, max_contries_pl, referencing_period_rule_pl
#Lists to store informations from "Index" sheet
#country participation flag (0/1)
global participation_flag, WACC
#Lists to store fixed irp dates from "MultipleFixedReference" sheet
global fixed_irp_dates
#Lists to store informations from "CountryBasket" sheet
#country basket flag (0/1)
global basket_flag_primary_al, basket_flag_secondary_al, basket_flag_compulsory_al, basket_flag_primary_pl
global basket_flag_secondary_pl, basket_flag_compulsory_pl, volume_dates, base_volume, basedates # basedate
#Lists to store informations from "MultipleDelay" sheet
global multipleDelay
###List to have prices after IRP
global dateprice, netdateprice
#Lists to store informations from "CogsAndRoyalties" sheet
global coggs, royalties
#Lists to store informations from "SimulatedAnnealing" sheet
global dmin, dmax, initdates

#----------------------------------------------------------------------
#####Initializing global varibles
num_of_contries             =0
num_of_markets              =0
irp_time_frame              =0

#List that contains references to sheets of Excel file
xl_sheet                    =[]
datediff                    =[]
#Lists to store informations from "InputInterface" sheet
countries                   =[]
dossier_submission_date     =[]
price_approval_date         =[]
price_publication_date      =[]
reimbursement_date          =[]
volume_pickup_dates         =[]
base_prices                 =[]

#Lists to store informations from "PriceOverrideAndProdDiscd" sheet
priceOverrideAndProdDiscd   =[]

#Lists to store informations from "PriceCut" sheet
priceCut                    =[]

#At launch data
multi_single_delay          =[]
num_refrence_rule           =[]
irp_noirp                   =[]
reference_rules             =[]
multiplier_factor           =[]
delay_price                 =[]
irp_from_date               =[]
price_rules                 =[]
min_contries                =[]
max_contries                =[]

###List to have discounts
discountLevel               =[]

#Post launch data
num_refrence_rule_pl        =[]
irp_noirp_pl                =[]
reference_rules_pl          =[]
multiplier_factor_pl        =[]
delay_price_pl              =[]
irp_from_date_pl            =[]
periodicity                 =[]
periodicity_date            =[]
price_rules_pl              =[]
min_contries_pl             =[]
max_contries_pl             =[]
referencing_period_rule_pl  =[]
#Lists to store informations from "Index" sheet
#country participation flag (0/1)
participation_flag          =[]
WACC                        =0
#Lists to store fixed irp dates from "MultipleFixedReference" sheet
fixed_irp_dates             =[]
#Lists to store informations from "CountryBasket" sheet
#country basket flag (0/1)
basket_flag_primary_al      =[]
basket_flag_secondary_al    =[]
basket_flag_compulsory_al   =[]
basket_flag_primary_pl      =[]
basket_flag_secondary_pl    =[]
basket_flag_compulsory_pl   =[]

volume_dates                =[]
base_volume                 =[]
basedates                   =[]

#Lists to store informations from "MultipleDelay" sheet
multipleDelay               =[]

#Lists to store informations from "MultipleDelay" sheet
priceLevels                 =[]

###List to have prices after IRP
dateprice                   =[]
netdateprice                =[]

#Lists to store informations from "CogsAndRoyalties" sheet
coggs                       =[]
royalties                   =[]

#Lists to store informations from "SimulatedAnnealing" sheet
dmin                       =[]
dmax                       =[]
initdates                  =[]
pricevol                   =[]
#----------------------------------------------------------------------

